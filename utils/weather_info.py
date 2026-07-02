import os
import requests
from typing import Any, Dict, Optional


class WeatherForecastTool:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENWEATHERMAP_API_KEY is required for WeatherForecastTool. "
                "Set it in your environment or .env file."
            )
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        params["appid"] = self.api_key
        params["units"] = "metric"
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None

    def get_current_weather(self, city: str) -> Optional[Dict[str, Any]]:
        return self._get("weather", {"q": city})

    def get_forecast_weather(self, city: str) -> Optional[Dict[str, Any]]:
        return self._get("forecast", {"q": city})
