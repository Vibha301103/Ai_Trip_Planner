"""
utils/rag_retriever.py
------------------------
Core RAG logic for the travel-guide knowledge base — hybrid design:

  1. Check the local registry (vectorstore/covered_destinations.json) to
     see if this destination is already pre-loaded.
  2. If yes -> similarity search against the local FAISS index (fast).
  3. If no -> fetch the destination LIVE from Wikivoyage, add it to the
     index and registry for next time (so the second person asking about
     the same place gets the fast local path), then answer from it.
  4. If Wikivoyage has no article for it either -> fall back to a live
     Tavily web search as a last resort (not cached, since general web
     search results are lower and more variable quality than a
     Wikivoyage article).

This means the knowledge base effectively covers ANY destination, not
just the ones pre-loaded by scripts/build_vector_store.py — it just
answers pre-loaded ones faster.
"""

import json
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from utils.wikivoyage_client import fetch_wikivoyage_article

VECTORSTORE_PATH = os.path.join("vectorstore", "travel_guides_index")
REGISTRY_PATH = os.path.join("vectorstore", "covered_destinations.json")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def normalize(name: str) -> str:
    return name.strip().lower()


class TravelGuideRetriever:
    """
    Answers destination queries from a local FAISS index when available,
    and transparently fetches + caches new destinations on demand
    otherwise.
    """

    def __init__(self, vectorstore_path: str = VECTORSTORE_PATH):
        self.vectorstore_path = vectorstore_path
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

        if os.path.exists(vectorstore_path):
            self.vectorstore = FAISS.load_local(
                vectorstore_path,
                self.embeddings,
                allow_dangerous_deserialization=True,  # safe: we build this index ourselves
            )
        else:
            # No pre-built index yet — that's fine, the live-fallback path
            # will build one up over time as destinations get queried.
            self.vectorstore = None

        self.covered = self._load_registry()

    def _load_registry(self) -> set:
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()

    def _save_registry(self):
        os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(sorted(self.covered), f, indent=2)

    def _add_to_index(self, destination: str, text: str, source_label: str):
        """Chunk new content, add it to the FAISS index, and persist both
        the index and the registry so future queries hit the fast path."""
        doc = Document(page_content=text, metadata={"source": source_label})
        chunks = self.splitter.split_documents([doc])

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vectorstore.add_documents(chunks)

        os.makedirs(os.path.dirname(self.vectorstore_path), exist_ok=True)
        self.vectorstore.save_local(self.vectorstore_path)

        self.covered.add(normalize(destination))
        self._save_registry()

    def search(self, destination: str, topic: str = "general travel guide", k: int = 3) -> str:
        """
        Get curated info about `destination`, focused on `topic` (e.g.
        "offbeat spots", "local culture and etiquette", "best time to
        visit"). Handles the hybrid lookup described in the module
        docstring, transparently, and labels the source of the answer.
        """
        query = f"{destination} {topic}"
        norm_destination = normalize(destination)

        # 1. Fast path: already indexed locally.
        if norm_destination in self.covered and self.vectorstore is not None:
            return self._format_results(
                self.vectorstore.similarity_search(query, k=k),
                note="from pre-loaded knowledge base",
            )

        # 2. Live fallback: try Wikivoyage first.
        article_text = fetch_wikivoyage_article(destination)
        if article_text:
            self._add_to_index(
                destination, article_text, source_label=f"wikivoyage:{destination}"
            )
            return self._format_results(
                self.vectorstore.similarity_search(query, k=k),
                note="freshly fetched from Wikivoyage and cached for next time",
            )

        # 3. Final fallback: live Tavily web search (not cached — general
        #    web results vary too much in quality to treat as a stable
        #    knowledge-base entry the way a Wikivoyage article is).
        return self._tavily_fallback(destination, topic)

    def _format_results(self, docs, note: str) -> str:
        if not docs:
            return f"No relevant information found ({note})."
        formatted = [
            f"(from {doc.metadata.get('source', 'unknown')}, {note}):\n"
            f"{doc.page_content.strip()}"
            for doc in docs
        ]
        return "\n\n---\n\n".join(formatted)

    def _tavily_fallback(self, destination: str, topic: str) -> str:
        try:
            from langchain_community.tools.tavily_search import TavilySearchResults

            tavily_api_key = os.environ.get("TAVILY_API_KEY")
            if not tavily_api_key:
                return (
                    f"No curated or Wikivoyage info found for '{destination}', "
                    f"and TAVILY_API_KEY is not set for a web-search fallback."
                )

            search = TavilySearchResults(tavily_api_key=tavily_api_key, max_results=3)
            results = search.invoke({"query": f"{destination} {topic} travel guide"})
            if not results:
                return f"No information found for '{destination}' from any source."

            snippets = [
                f"- {r.get('content', '').strip()[:300]} (source: {r.get('url', '')})"
                for r in results
                if r.get("content")
            ]
            snippet_text = "\n".join(snippets)
            return (
                f"(from live web search — no curated or Wikivoyage guide exists "
                f"yet for '{destination}'; treat this as general web info, not a "
                f"vetted travel guide):\n{snippet_text}"
            )
        except Exception:
            return f"No information found for '{destination}' from any source."