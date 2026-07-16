"""
scripts/build_vector_store.py
--------------------------------
Builds the FAISS vector store from TWO sources:
  1. Hand-curated files in data/travel_guides/ (*.md, *.txt) — your own
     writing, use this for anything you want extra control/detail over.
  2. Wikivoyage articles for every destination listed in
     data/popular_destinations.txt — auto-fetched, gives broad coverage
     without writing everything by hand.

Also writes vectorstore/covered_destinations.json, a small registry of
which destinations are already indexed. utils/rag_retriever.py checks
this registry at query time to decide whether it can answer locally or
needs to fetch a destination live (see utils/rag_retriever.py).

Usage:
    python scripts/build_vector_store.py

Run this once, and again any time you:
  - add/edit files in data/travel_guides/
  - add destinations to data/popular_destinations.txt
"""

import glob
import json
import os
import time

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from utils.wikivoyage_client import fetch_wikivoyage_article

DATA_DIR = "guides"
POPULAR_DESTINATIONS_FILE = os.path.join("guides", "popular_destinations.txt")
VECTORSTORE_PATH = os.path.join("vectorstore", "travel_guides_index")
REGISTRY_PATH = os.path.join("vectorstore", "covered_destinations.json")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def normalize(name: str) -> str:
    return name.strip().lower()


def load_curated_files():
    """Load hand-written .md/.txt files from data/travel_guides/."""
    file_paths = glob.glob(os.path.join(DATA_DIR, "*.md")) + glob.glob(
        os.path.join(DATA_DIR, "*.txt")
    )
    documents = []
    covered = set()
    for path in file_paths:
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        destination_name = os.path.splitext(os.path.basename(path))[0]
        for doc in docs:
            doc.metadata["source"] = f"curated:{destination_name}"
        documents.extend(docs)
        covered.add(normalize(destination_name))
    print(f"Loaded {len(documents)} curated document(s) from {DATA_DIR}/")
    return documents, covered


def load_wikivoyage_destinations():
    """Fetch Wikivoyage articles for every destination in the popular list."""
    if not os.path.exists(POPULAR_DESTINATIONS_FILE):
        print(f"No {POPULAR_DESTINATIONS_FILE} found — skipping Wikivoyage preload.")
        return [], set()

    with open(POPULAR_DESTINATIONS_FILE, "r", encoding="utf-8") as f:
        destinations = [line.strip() for line in f if line.strip()]

    documents = []
    covered = set()
    for destination in destinations:
        print(f"Fetching Wikivoyage article for '{destination}'...")
        article_text = fetch_wikivoyage_article(destination)
        if article_text:
            documents.append(
                Document(
                    page_content=article_text,
                    metadata={"source": f"wikivoyage:{destination}"},
                )
            )
            covered.add(normalize(destination))
        else:
            print(f"  -> no Wikivoyage article found for '{destination}', skipping.")
        time.sleep(0.5)  # be polite to the free public API

    print(f"Fetched {len(documents)} Wikivoyage article(s).")
    return documents, covered


def build():
    curated_docs, curated_covered = load_curated_files()
    wikivoyage_docs, wikivoyage_covered = load_wikivoyage_destinations()

    all_docs = curated_docs + wikivoyage_docs
    if not all_docs:
        print("No documents found from either source — nothing to build.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(all_docs)
    print(f"Split into {len(chunks)} chunks total.")

    print("Loading embedding model (first run downloads it, ~90MB)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"Saved vector store to {VECTORSTORE_PATH}/")

    covered_destinations = sorted(curated_covered | wikivoyage_covered)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(covered_destinations, f, indent=2)
    print(f"Saved registry of {len(covered_destinations)} covered destination(s) "
          f"to {REGISTRY_PATH}")


if __name__ == "__main__":
    build()