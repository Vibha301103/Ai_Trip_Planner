# 🌍 AI Trip Planner

An AI-powered travel planning agent that generates complete, detailed trip itineraries — including attractions, restaurants, activities, transportation, weather forecasts, and cost breakdowns — using a LangGraph agent backed by Groq's LLM.

**🔗 Live Demo:** [aitripplanner.streamlit.app](https://aitripplanner-fk5v5eqqhe3gkcmwgmhqsc.streamlit.app)

---

##  Screenshots
<img width="1695" height="846" alt="Screenshot 2026-07-08 090941" src="https://github.com/user-attachments/assets/c78d4a9d-a708-49d2-a017-b4ca062d12ca" />
<img width="1497" height="871" alt="Screenshot 2026-07-08 091024" src="https://github.com/user-attachments/assets/6a6c5991-5e60-461d-883c-3369a4bfdd8a" />
<img width="1380" height="837" alt="Screenshot 2026-07-08 091036" src="https://github.com/user-attachments/assets/1a121cd4-09d8-4ee5-88e0-a187880353d3" />
<img width="1135" height="827" alt="Screenshot 2026-07-08 091046" src="https://github.com/user-attachments/assets/1001810a-b088-42f3-88b1-1fff0b0355d7" />



---

## ✨ Features

- 🗺️ Complete day-by-day travel itineraries for any destination
- 🏨 Hotel recommendations with approximate per-night costs
- 🍽️ Restaurant suggestions with price ranges
- 🎯 Local attractions and activities
- 🚕 Transportation options for the destination
- 🌦️ Real-time weather forecasts
- 💱 Currency conversion for cost estimates
- 💰 Detailed expense breakdown and daily budget suggestions
- 🔁 Automatic fallback search (Tavily) if primary place-search API is unavailable

---

## Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Agent Framework:** [LangGraph](https://www.langchain.com/langgraph) + [LangChain](https://www.langchain.com/)
- **LLM Provider:** [Groq](https://groq.com/) (`llama-3.3-70b-versatile`)
- **Backend (optional API):** [FastAPI](https://fastapi.tiangolo.com/)

### APIs Used
| Service | Purpose |
|---|---|
| [Groq](https://console.groq.com/) | LLM inference |
| [Tavily](https://tavily.com/) | Real-time web search (place info fallback) |
| [Foursquare Places API](https://foursquare.com/developers/) | Attractions, restaurants, activities, transportation |
| [OpenWeatherMap](https://openweathermap.org/api) | Current weather & forecasts |
| [ExchangeRate-API](https://www.exchangerate-api.com/) | Currency conversion |

---

## Getting Started (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/Vibha301103/Ai_Trip_Planner.git
cd Ai_Trip_Planner
```

### 2. Create a virtual environment
```bash
python -m venv env
env\Scripts\activate      # Windows
source env/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root (this file is gitignored and should **never** be committed):
```env
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
FOURSQUARE_API_KEY=your_key_here
OPENWEATHERMAP_API_KEY=your_key_here
EXCHANGE_RATE_API_KEY=your_key_here
```

### 5. Run the app
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## Deployment

This app is deployed for free on **[Streamlit Community Cloud](https://share.streamlit.io/)**.

To deploy your own copy:
1. Push this repo to your own GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch `master`, and main file `streamlit_app.py`.
4. Under **Advanced settings → Secrets**, add your API keys in TOML format (same keys as the `.env` file above).
5. Click **Deploy**.

---

## Project Structure

```
Ai_Trip_Planner/
├── agent/                  # LangGraph agent workflow
├── config/                 # LLM provider configuration
├── prompt_library/         # System prompt for the travel agent
├── tools/                  # LangChain tools (weather, places, currency, expenses)
├── utils/                  # Core service logic (API calls, model loading)
├── streamlit_app.py        # Streamlit frontend (main entry point)
├── main.py                 # Optional FastAPI backend
└── requirements.txt        # Python dependencies
```

---

## Notes

- The Foursquare integration uses their newer **Service API Key** system (`places-api.foursquare.com`), not the legacy v3 API.
- If Foursquare search fails for any reason, the app automatically falls back to Tavily search.
- Free-tier API keys (Groq, OpenWeatherMap, etc.) have rate limits — heavy or rapid usage may occasionally hit these limits.

---

## Author

**Vibha Gupta**
GitHub: [@Vibha301103](https://github.com/Vibha301103)
