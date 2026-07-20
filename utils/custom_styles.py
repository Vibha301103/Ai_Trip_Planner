"""
utils/custom_styles.py
-------------------------
Flat white "dashboard" theme (Option B from the mockup comparison) —
uppercase mini-labels, icon badges, grid-based feature cards, no photo
background. Matches mockups/option_b_flat_dashboard.html.

Import and inject once near the top of streamlit_app.py:

    st.markdown(get_custom_css(), unsafe_allow_html=True)
    st.markdown(get_hero_banner_html(title, subtitle), unsafe_allow_html=True)
    st.markdown(get_feature_cards_html(), unsafe_allow_html=True)
"""


def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* ---- Flat, soft neutral page background — no photo ---- */
    [data-testid="stAppViewContainer"] {
        background: #f4f2f0;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* ---- Force readable, warm-dark text on labels/markdown everywhere ---- */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stMarkdownContainer"] p,
    label, .stMarkdown, .stMarkdown p {
        color: #4a2c2a !important;
    }

    /* ---- Hero banner ---- */
    .hero-banner {
        background: linear-gradient(120deg, #ff7e5f 0%, #feb47b 45%, #ff6a88 100%);
        border-radius: 14px;
        padding: 1.9rem 1.8rem;
        margin-bottom: 1.4rem;
    }

    .hero-banner h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    .hero-banner p {
        color: #fff4ee;
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    /* ---- Feature cards grid ---- */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-bottom: 1.4rem;
    }

    .feature-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #f0e5da;
    }

    .feature-card .icon-badge {
        width: 30px; height: 30px; border-radius: 50%;
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 14px; margin-bottom: 8px;
    }

    .feature-card .label {
        font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
        color: #b0693f; font-weight: 700; margin-bottom: 6px;
    }

    .feature-card .desc {
        font-size: 12px; color: #6b5a52; line-height: 1.4;
    }

    /* ---- Section headers ---- */
    h2, h3 {
        color: #d9534f;
        font-weight: 700;
    }

    /* ---- Expander (Plan a trip) — flat white card, uppercase header ---- */
    [data-testid="stExpander"] {
        background: #ffffff !important;
        border-radius: 14px;
        border: 1px solid #f0e5da;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    [data-testid="stExpander"] summary {
        background: transparent !important;
        border-radius: 10px;
    }

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {
        color: #b0693f !important;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-size: 0.85rem;
    }

    /* ---- Chat messages ---- */
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border-radius: 12px;
        border: 1px solid #f0e5da;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }

    /* ---- Text inputs & selectboxes: light cream fill, dark text ---- */
    .stTextInput>div>div>input,
    .stSelectbox>div>div,
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 1.5px solid #f0d9c8 !important;
        background: #fdf6f0 !important;
        color: #2e2320 !important;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea textarea::placeholder {
        color: #b8a89e !important;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea textarea:focus {
        border: 1.5px solid #ff7e5f !important;
        box-shadow: 0 0 0 1px #ff7e5f !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: #fdf6f0 !important;
        border-radius: 8px !important;
        border: 1.5px solid #f0d9c8 !important;
    }

    .stSelectbox [data-baseweb="select"] * {
        color: #2e2320 !important;
    }

    /* ---- Buttons ---- */
    .stButton>button, .stFormSubmitButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.3rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-size: 0.85rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton>button:hover, .stFormSubmitButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 126, 95, 0.35);
        color: white;
    }

    /* ---- Chat input box ---- */
    [data-testid="stChatInput"] textarea {
        border-radius: 8px !important;
        border: 1.5px solid #f0d9c8 !important;
        background: #fdf6f0 !important;
    }

    hr {
        border-top: 2px solid #f0d9c8;
    }
    </style>
    """


def get_hero_banner_html(title: str, subtitle: str) -> str:
    """Returns the HTML for the gradient hero banner, to replace st.title()."""
    return f"""
    <div class="hero-banner">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """


def get_feature_cards_html() -> str:
    """
    The 9-card features-overview grid from the approved mockup
    (mockups/option_b_flat_dashboard.html) — a static visual summary of
    what the app can do. NOT live data; purely decorative/informational,
    shown once near the top of the page.
    """
    cards = [
        ("🌦️", "Weather", "Real-time forecasts for your destination"),
        ("💰", "Budget", "Daily expense breakdown & cost estimates"),
        ("✈️", "Transport", "Flight/train/bus estimates + booking links"),
        ("🏨", "Hotels", "Recommendations with per-night pricing"),
        ("🍽️", "Food", "Restaurant picks with price ranges"),
        ("🎯", "Attractions", "Top sights & activities nearby"),
        ("💱", "Currency", "Live conversion for cost estimates"),
        ("📚", "Off-beat Guide", "Local culture & hidden spots via RAG"),
        ("💬", "Ask Follow-ups", "Chat about your plan after it's generated"),
    ]

    card_html = "".join(
        f'<div class="feature-card">'
        f'<div class="icon-badge">{icon}</div>'
        f'<div class="label">{label}</div>'
        f'<div class="desc">{desc}</div>'
        f'</div>'
        for icon, label, desc in cards
    )

    return f'<div class="feature-grid">{card_html}</div>'