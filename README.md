<img width="1920" height="1020" alt="Screenshot 2026-07-16 161310" src="https://github.com/user-attachments/assets/0015074c-5d83-4a34-b6b3-3066ce49a4c1" /># 🌍 AI Trip Planner

An AI-powered travel planning agent that generates complete, detailed trip itineraries — including attractions, restaurants, activities, transportation, weather forecasts, and cost breakdowns — using a LangGraph agent backed by Groq's LLM. Now with live transport pricing, a Wikivoyage-powered knowledge base for off-beat destination guides, and follow-up Q&A so you can ask questions about your plan after it's generated.

**🔗 Live Demo:** [aitripplanner.streamlit.app](https://aitripplanner-fk5v5eqqhe3gkcmwgmhqsc.streamlit.app)

---

##  Screenshots
<img width="1695" height="846" alt="Screenshot 2026-07-08 090941" src="https://github.com/user-attachments/assets/c78d4a9d-a708-49d2-a017-b4ca062d12ca" />
<img width="1497" height="871" alt="Screenshot 2026-07-08 091024" src="https://github.com/user-attachments/assets/6a6c5991-5e60-461d-883c-3369a4bfdd8a" />
<img width="1920" height="1020" alt="Screenshot 2026-07-16 162002" src="https://github.com/user-attachments/assets/6e54924f-469a-4b30-acd9-ea81aaa24e41" />
<img width="1920" height="1020" alt="Screenshot 2026-07-16 162009" src="https://github.com/user-attachments/assets/98d2e47d-e314-48f7-a736-5a1649276e99" />
<img width="1920" height="1020" alt="Screenshot 2026-07-16 161332" src="https://github.com/user-attachments/assets/b161ff5b-2b37-4c6c-8386-14655ed056c4" />
<img width="1920" height="1020" alt="Screenshot 2026-07-16 161310" src="https://github.com/user-attachments/assets/649a2711-2c5a-4b23-b269-28666c830b0e" />





---

## Features

- 🗺️ Complete day-by-day travel itineraries for any destination, with separate tracks for generic tourist spots and off-beat locations
- 🏨 Hotel recommendations with approximate per-night costs
- 🍽️ Restaurant suggestions with price ranges
- 🎯 Local attractions and activities
- ✈️ Transport cost estimates (flight/train/bus) between an origin and destination, with direct booking links (Google Flights, MakeMyTrip, IRCTC, ixigo, RedBus, and more) so you can check live prices yourself
- 📚 Off-beat destination knowledge base (RAG) — pulls detailed local guides (offbeat spots, culture/etiquette, best time to visit) from Wikivoyage for any destination worldwide, with instant answers for pre-loaded popular destinations and automatic live fetch + caching for anywhere else
- 💬 Follow-up Q&A — ask questions about your generated plan in a chat box, with full conversation memory
- 🌦️ Real-time weather forecasts
- 💱 Currency conversion for cost estimates
- 💰 Detailed expense breakdown and daily budget suggestions
- 🔁 Automatic fallback search (Tavily) if primary place-search API is unavailable
- 🔄 Automatic retry on transient tool-calling failures from the LLM provider

---

## Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Agent Framework:** [LangGraph](https://www.langchain.com/langgraph) + [LangChain](https://www.langchain.com/)
- **LLM Provider:** [Groq](https://groq.com/) (`llama-3.3-70b-versatile`)
- **Backend (optional API):** [FastAPI](https://fastapi.tiangolo.com/)
- **Vector store (RAG):** [FAISS](https://github.com/facebookresearch/faiss), with local [sentence-transformers](https://www.sbert.net/) embeddings (no extra API key required)

### APIs Used
| Service | Purpose |
|---|---|
| [Groq](https://console.groq.com/) | LLM inference |
| [Tavily](https://tavily.com/) | Real-time web search (place info fallback, transport price estimates, off-beat guide fallback) |
| [Foursquare Places API](https://foursquare.com/developers/) | Attractions, restaurants, activities, transportation |
| [OpenWeatherMap](https://openweathermap.org/api) | Current weather & forecasts |
| [ExchangeRate-API](https://www.exchangerate-api.com/) | Currency conversion |
| [Wikivoyage API](https://en.wikivoyage.org/w/api.php) | Off-beat destination guides for the RAG knowledge base (free, no key required) |

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
(Wikivoyage needs no API key — it's a free public API.)

### 5. (Optional) Pre-build the RAG knowledge base
Pre-loads popular destinations from Wikivoyage so they answer instantly instead of needing a live fetch the first time someone asks:
```bash
python scripts/build_vector_store.py
```
This is optional — the app works without it, since any destination not yet indexed is fetched live and cached automatically the first time it's asked about.

### 6. Run the app
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

Note: Streamlit Community Cloud's filesystem resets on redeploys, so any destinations cached live during a session won't persist across redeploys unless `vectorstore/` is committed or the build script runs as part of your deploy step.

---

## Project Structure

```
Ai_Trip_Planner/
├── agent/                  # LangGraph agent workflow
├── config/                 # LLM provider configuration
├── guides/                 # Hand-written destination guides (optional) + popular_destinations.txt for RAG pre-loading
├── prompt_library/         # System prompt for the travel agent
├── scripts/
│   └── build_vector_store.py   # One-time/optional script to pre-build the RAG vector store
├── tools/                  # LangChain tools (weather, places, currency, expenses, transport, RAG)
├── utils/                  # Core service logic (API calls, model loading, RAG retrieval, Wikivoyage client, retry wrapper)
├── vectorstore/             # Generated FAISS index (gitignored, not committed)
├── streamlit_app.py        # Streamlit frontend (main entry point) — includes follow-up Q&A chat
├── main.py                 # Optional FastAPI backend
└── requirements.txt        # Python dependencies
```

---

## How the RAG Knowledge Base Works

1. **Pre-loaded destinations** (listed in `guides/popular_destinations.txt`) answer instantly from a local FAISS index.
2. **Any other destination** is fetched live from Wikivoyage the first time it's asked about, then cached into the index so it's instant for everyone after that.
3. **If Wikivoyage has no article** for a destination, the app falls back to a live Tavily web search, clearly labeled as general web info rather than a vetted guide.

This means off-beat itinerary suggestions work for effectively any destination worldwide, not just a fixed list.

---

## Notes

- The Foursquare integration uses their newer **Service API Key** system (`places-api.foursquare.com`), not the legacy v3 API.
- If Foursquare search fails for any reason, the app automatically falls back to Tavily search.
- Transport prices shown are **estimates** based on web search, not guaranteed fares — booking links are provided so you can check live prices before purchasing.
- Free-tier API keys (Groq, OpenWeatherMap, etc.) have rate limits — heavy or rapid usage may occasionally hit these limits.
- Groq's Llama models occasionally produce a malformed tool call under heavy multi-tool use; the app automatically retries these specific failures rather than surfacing an error immediately.

---

## Author

**Vibha Gupta**
GitHub: [@Vibha301103](https://github.com/Vibha301103)
