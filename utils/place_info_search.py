import os
import requests
from langchain_tavily import TavilySearch

class FoursquarePlaceSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://places-api.foursquare.com/places/search"  # CHANGED
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",  # CHANGED
            "X-Places-Api-Version": "2025-06-17"  # ADDED
        }

    def _search(self, query: str, place: str, limit: int = 10) -> str:
        """
        Generic Foursquare search helper. Uses 'near' for the place name
        and 'query' for the category/keyword.
        """
        params = {
            "query": query,
            "near": place,
            "limit": limit
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return f"No results found for '{query}' near {place}."
        formatted = []
        for r in results:
            name = r.get("name", "Unknown")
            categories = ", ".join(c.get("name", "") for c in r.get("categories", []))
            address = r.get("location", {}).get("formatted_address", "Address not available")
            formatted.append(f"- {name} ({categories}) — {address}")
        return "\n".join(formatted)

    def google_search_attractions(self, place: str) -> dict:
        """Kept method name for compatibility with existing calling code."""
        return self._search("tourist attractions", place)

    def google_search_restaurants(self, place: str) -> dict:
        return self._search("restaurants", place)

    def google_search_activity(self, place: str) -> dict:
        return self._search("activities", place)

    def google_search_transportation(self, place: str) -> dict:
        return self._search("transportation", place)


class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
