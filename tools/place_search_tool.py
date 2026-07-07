import os
from utils.place_info_search import FoursquarePlaceSearchTool, TavilyPlaceSearchTool
from typing import List, Optional
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")
        self.foursquare_places_search = FoursquarePlaceSearchTool(self.foursquare_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""

        @tool
        def search_attractions(place: Optional[str] = None, location: Optional[str] = None, city: Optional[str] = None) -> str:
            """Search attractions of a place"""
            place = place or location or city
            if not place:
                return "No place specified for attraction search."
            try:
                attraction_result = self.foursquare_places_search.google_search_attractions(place)
                if attraction_result:
                    return f"Following are the attractions of {place} as suggested by Foursquare: {attraction_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Foursquare cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"

        @tool
        def search_restaurants(place: Optional[str] = None, location: Optional[str] = None, city: Optional[str] = None) -> str:
            """Search restaurants of a place"""
            place = place or location or city
            if not place:
                return "No place specified for restaurant search."
            try:
                restaurants_result = self.foursquare_places_search.google_search_restaurants(place)
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by Foursquare: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Foursquare cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"

        @tool
        def search_activities(place: Optional[str] = None, location: Optional[str] = None, city: Optional[str] = None) -> str:
            """Search activities of a place"""
            place = place or location or city
            if not place:
                return "No place specified for activity search."
            try:
                activities_result = self.foursquare_places_search.google_search_activity(place)
                if activities_result:
                    return f"Following are the activities in and around {place} as suggested by Foursquare: {activities_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Foursquare cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"

        @tool
        def search_transportation(place: Optional[str] = None, location: Optional[str] = None, city: Optional[str] = None) -> str:
            """Search transportation of a place"""
            place = place or location or city
            if not place:
                return "No place specified for transportation search."
            try:
                transport_result = self.foursquare_places_search.google_search_transportation(place)
                if transport_result:
                    return f"Following are the modes of transportation available in {place} as suggested by Foursquare: {transport_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Foursquare cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"

        return [search_attractions, search_restaurants, search_activities, search_transportation]