
"""
tools/rag_tool.py
--------------------
Exposes TravelGuideRetriever (utils/rag_retriever.py) to the LangGraph
agent as a LangChain tool, following the same pattern as this project's
other tools: a class holding a list of @tool-decorated methods in
self.rag_tool_list.

Purpose: Retrieve destination guide content — offbeat spots, local
culture/etiquette, best time to visit, local transport norms — that
real-time APIs like Foursquare/weather don't provide. This works for ANY
destination, not just pre-loaded ones: pre-loaded places answer instantly
from the local index, anything else is fetched live from Wikivoyage (and
cached for next time), with a web-search fallback if even Wikivoyage
doesn't have it.

Exposed Functions:
  search_travel_guide(destination: str, topic: str) -> str
"""

from langchain.tools import tool

from utils.rag_retriever import TravelGuideRetriever


class TravelGuideRAGTool:
    def __init__(self):
        self.retriever = TravelGuideRetriever()
        self.rag_tool_list = self._setup_tools()

    def _setup_tools(self):
        @tool
        def search_travel_guide(destination: str, topic: str = "general travel guide") -> str:
            """
            Get detailed destination-guide information: off-beat spots,
            local culture and etiquette, best time to visit, local
            transport norms — the kind of texture general web/API results
            don't cover. Works for ANY destination worldwide, not just a
            fixed list — covers it live if it isn't already cached.
            `destination` should be a place name, e.g. "Jaipur". `topic`
            narrows the focus, e.g. "offbeat spots" or "best time to
            visit" — defaults to a general overview if omitted.
            """
            return self.retriever.search(destination, topic)

        return [search_travel_guide]