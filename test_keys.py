import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    try:
        from langchain_openai import ChatOpenAI
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            return "❌ OPENAI_API_KEY not found in .env"
        llm = ChatOpenAI(model_name="o4-mini", api_key=key)
        response = llm.invoke("Say hello in one word")
        return f"✅ OpenAI key works — response: {response.content}"
    except Exception as e:
        return f"❌ OpenAI failed: {e}"

def test_groq():
    try:
        from langchain_groq import ChatGroq
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            return "❌ GROQ_API_KEY not found in .env"
        llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=key)
        response = llm.invoke("Say hello in one word")
        return f"✅ Groq key works — response: {response.content}"
    except Exception as e:
        return f"❌ Groq failed: {e}"

def test_google_api():
    # Used for Google AI Studio (Gemini) models — not currently called
    # anywhere in your app, but testable via a simple request.
    import requests
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        return "❌ GOOGLE_API_KEY not found in .env"
    resp = requests.get(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    )
    return "✅ Google API key works" if resp.status_code == 200 else f"❌ Google API failed: {resp.status_code} - {resp.text[:200]}"

def test_gplaces():
    import requests
    key = os.environ.get("GPLACES_API_KEY")
    if not key:
        return "❌ GPLACES_API_KEY not found in .env"
    resp = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={"query": "restaurants in Manali", "key": key}
    )
    if resp.status_code == 200 and resp.json().get("status") == "OK":
        return "✅ Google Places key works"
    return f"❌ Google Places failed: {resp.status_code} - {resp.text[:200]}"

def test_foursquare():
    import requests
    key = os.environ.get("FOURSQUARE_API_KEY")
    if not key:
        return "❌ FOURSQUARE_API_KEY not found in .env"
    resp = requests.get(
        "https://places-api.foursquare.com/places/search",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {key}",
            "X-Places-Api-Version": "2025-06-17"
        },
        params={"query": "restaurants", "near": "Manali", "limit": 1}
    )
    return "✅ Foursquare key works" if resp.status_code == 200 else f"❌ Foursquare failed: {resp.status_code} - {resp.text[:200]}"

def test_tavily():
    try:
        from langchain_tavily import TavilySearch
        key = os.environ.get("TAVILY_API_KEY")
        if not key:
            return "❌ TAVILY_API_KEY not found in .env"
        os.environ["TAVILY_API_KEY"] = key
        tavily_tool = TavilySearch(topic="general")
        result = tavily_tool.invoke({"query": "test query"})
        return "✅ Tavily key works"
    except Exception as e:
        return f"❌ Tavily failed: {e}"

def test_openweather():
    import requests
    key = os.environ.get("OPENWEATHERMAP_API_KEY")
    if not key:
        return "❌ OPENWEATHERMAP_API_KEY not found in .env"
    resp = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": "Manali", "appid": key}
    )
    return "✅ OpenWeatherMap key works" if resp.status_code == 200 else f"❌ OpenWeatherMap failed: {resp.status_code} - {resp.text[:200]}"

def test_exchangerate():
    import requests
    key = os.environ.get("EXCHANGE_RATE_API_KEY")
    if not key:
        return "❌ EXCHANGE_RATE_API_KEY not found in .env"
    resp = requests.get(f"https://v6.exchangerate-api.com/v6/{key}/latest/USD")
    return "✅ ExchangeRate key works" if resp.status_code == 200 else f"❌ ExchangeRate failed: {resp.status_code} - {resp.text[:200]}"

def test_langchain():
    import requests
    key = os.environ.get("LANGCHAIN_API_KEY")
    if not key:
        return "❌ LANGCHAIN_API_KEY not found in .env"
    resp = requests.get(
        "https://api.smith.langchain.com/info",
        headers={"x-api-key": key}
    )
    return "✅ LangChain/LangSmith key works" if resp.status_code == 200 else f"❌ LangSmith failed: {resp.status_code} - {resp.text[:200]}"

if __name__ == "__main__":
    print(test_openai())
    print(test_groq())
    print(test_google_api())
    print(test_gplaces())
    print(test_foursquare())
    print(test_tavily())
    print(test_openweather())
    print(test_exchangerate())
    print(test_langchain())