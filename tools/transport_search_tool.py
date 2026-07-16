"""
tools/transport_search_tool.py
--------------------------------
Exposes TransportSearch (utils/transport_search.py) to the LangGraph agent
as a LangChain tool, following the same pattern as this project's existing
tools/currency_conversion_tool.py and tools/weather_info_tool.py: a class
that holds a list of @tool-decorated methods in self.transport_tools.

Purpose: Given an origin, destination, and mode of transport (flight,
train, or bus), returns:
  - An estimated price range (from a Tavily web search, summarized by the
    agent's own LLM reasoning when it writes the itinerary)
  - Direct links to real booking sites so the user can check live,
    up-to-date prices themselves.

Exposed Functions:
  get_transport_options(origin: str, destination: str, mode: str) -> str
"""

from langchain.tools import tool

from utils.transport_search import TransportSearch


class TransportSearchTool:
    def __init__(self):
        self.transport_search = TransportSearch()
        self.transport_search_tool_list = self._setup_tools()

    def _setup_tools(self):
        @tool
        def get_transport_options(origin: str, destination: str, mode: str) -> str:
            """
            Get transport info between two cities for a given mode of
            transport. `mode` must be one of: 'flight', 'train', 'bus'.
            Returns an estimated price range (based on a web search — call
            this out as an ESTIMATE, not a guaranteed fare) plus direct
            booking-site links where the user can check live prices.
            """
            try:
                price_info = self.transport_search.get_estimated_price_range(
                    origin, destination, mode
                )
                links = self.transport_search.get_booking_links(origin, destination, mode)
                links_text = "\n".join(
                    f"- [{name}]({url})" for name, url in links.items()
                )

                return (
                    f"### Transportation Estimate ({mode}, {origin} -> {destination})\n"
                    f"**Estimated price (from web search — NOT a guaranteed fare):**\n"
                    f"{price_info}\n\n"
                    f"### Book Your Tickets\n"
                    f"{links_text}\n\n"
                    f"IMPORTANT: Reproduce the links above exactly as markdown links in "
                    f"your final response. Do not omit or shorten them."
                )
            except ValueError as e:
                return str(e)

        return [get_transport_options]