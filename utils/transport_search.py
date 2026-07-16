"""
utils/transport_search.py
--------------------------
Core logic for the new "transport options" feature:
  1. Build direct search links to real booking sites (flights, trains, buses)
     for a given origin -> destination -> date, so the user can check live
     prices themselves.
  2. Use Tavily (already used elsewhere in this project for place search
     fallback) to fetch an approximate price range from the web, so the
     agent can quote a rough number in the itinerary.

This mirrors the pattern used by utils/currency_convertor.py and
utils/weather_info.py in this project: a plain class with simple methods,
no LangChain-specific code — the LangChain @tool wrapping happens in
tools/transport_search_tool.py.
"""

import os
from urllib.parse import quote_plus

from langchain_community.tools.tavily_search import TavilySearchResults


class TransportSearch:
    """
    Builds booking-site links and fetches an estimated price range for
    travel between two cities by a given mode of transport.
    """

    def __init__(self, tavily_api_key: str | None = None):
        # Reuses the same TAVILY_API_KEY already required by this project.
        self.tavily_api_key = tavily_api_key or os.environ.get("TAVILY_API_KEY")
        if not self.tavily_api_key:
            raise EnvironmentError(
                "TAVILY_API_KEY is not set. Add it to your .env file."
            )
        self._search = TavilySearchResults(
            tavily_api_key=self.tavily_api_key, max_results=5
        )

    # ------------------------------------------------------------------
    # 1. Direct links to booking sites (no API cost, always works)
    # ------------------------------------------------------------------
    def get_booking_links(self, origin: str, destination: str, mode: str) -> dict:
        """
        Return a dict of {site_name: url} of direct search-result links for
        the given mode ("flight", "train", or "bus").
        """
        mode = mode.strip().lower()
        o = quote_plus(origin.strip())
        d = quote_plus(destination.strip())

        if mode == "flight":
            return {
                "Google Flights": f"https://www.google.com/travel/flights?q=Flights%20from%20{o}%20to%20{d}",
                "MakeMyTrip": f"https://www.makemytrip.com/flight/search?itinerary={o}-{d}",
                "Skyscanner": f"https://www.skyscanner.co.in/transport/flights/{o}/{d}/",
            }
        elif mode == "train":
            return {
                "IRCTC": "https://www.irctc.co.in/nget/train-search",
                "ixigo Trains": f"https://www.ixigo.com/search/result/train/{o}/{d}",
                "RailYatri": f"https://www.railyatri.in/trains-between-stations/{o}-to-{d}",
            }
        elif mode == "bus":
            return {
                "RedBus": f"https://www.redbus.in/search?fromCityName={o}&toCityName={d}",
                "AbhiBus": f"https://www.abhibus.com/bus_tickets/{o}-to-{d}",
                "ixigo Buses": f"https://www.ixigo.com/search/result/bus/{o}/{d}",
            }
        else:
            raise ValueError("mode must be one of: 'flight', 'train', 'bus'")

    # ------------------------------------------------------------------
    # 2. Estimated price range via Tavily web search
    # ------------------------------------------------------------------
    def get_estimated_price_range(self, origin: str, destination: str, mode: str) -> str:
        """
        Use Tavily to search for typical fares and return the raw search
        snippets. The calling tool/agent (which has the LLM) is responsible
        for summarizing these into an approximate range — this method just
        fetches source material, it does not fabricate a number itself.
        """
        mode = mode.strip().lower()
        query = f"{mode} ticket price {origin} to {destination} approximate fare"
        results = self._search.invoke({"query": query})

        if not results:
            return "No pricing information found via web search."

        snippets = []
        for r in results[:5]:
            content = r.get("content", "").strip()
            url = r.get("url", "")
            if content:
                snippets.append(f"- {content[:300]} (source: {url})")

        return "\n".join(snippets) if snippets else "No pricing information found."