import streamlit as st
import os
import requests
import numpy as np
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="HerHealth AI",
    page_icon="🌸",
    layout="centered",
)

# --------------------------------------------------
# Custom styling — glassmorphic, gradient-mesh redesign
# --------------------------------------------------

st.markdown(
    """
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif;
        }

        /* ---------- Animated gradient-mesh background ---------- */
        .stApp {
            background: radial-gradient(circle at 15% 20%, #ffe0ef 0%, transparent 45%),
                        radial-gradient(circle at 85% 15%, #e3d9ff 0%, transparent 45%),
                        radial-gradient(circle at 50% 90%, #d9ecff 0%, transparent 50%),
                        linear-gradient(160deg, #fdf7fb 0%, #f6f3fc 55%, #f2f8fb 100%);
            background-attachment: fixed;
        }

        /* ---------- Hero ---------- */
        .hero {
            text-align: center;
            padding: 46px 14px 26px 14px;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.65);
            border: 1px solid rgba(182,122,176,0.25);
            backdrop-filter: blur(10px);
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #8d5fa8;
            margin-bottom: 18px;
            box-shadow: 0 4px 18px rgba(150,100,180,0.12);
        }

        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 50px;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(100deg, #6d3fa0 0%, #b6539b 45%, #e08a6f 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 6px;
            line-height: 1.1;
        }

        .hero-subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 19px;
            font-weight: 600;
            color: #4b3b57;
            margin-bottom: 10px;
        }

        .hero-description {
            font-size: 15px;
            color: #7a7086;
            max-width: 440px;
            margin: 0 auto;
        }

        /* ---------- Glass panel helper ---------- */
        .glass-panel {
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.7);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(120,90,150,0.10);
            padding: 22px 24px;
        }

        /* ---------- Chat bubbles ---------- */
        .chat-row {
            display: flex;
            gap: 10px;
            margin: 14px 0;
            align-items: flex-end;
        }

        .chat-row.user {
            flex-direction: row-reverse;
        }

        .avatar {
            width: 34px;
            height: 34px;
            min-width: 34px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            font-weight: 700;
            color: white;
            box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        }

        .avatar.user-avatar {
            background: linear-gradient(135deg, #7b5cf0, #b6539b);
        }

        .avatar.ai-avatar {
            background: linear-gradient(135deg, #6dc9c0, #8d6fb8);
        }

        .chat-user {
            background: linear-gradient(135deg, #7b5cf0, #b6539b);
            color: white;
            border-radius: 18px 18px 4px 18px;
            padding: 12px 17px;
            max-width: 78%;
            box-shadow: 0 6px 18px rgba(123,92,240,0.22);
            font-size: 14.5px;
            line-height: 1.5;
        }

        .chat-ai {
            background: rgba(255,255,255,0.75);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(200,190,220,0.5);
            border-radius: 18px 18px 18px 4px;
            padding: 12px 17px;
            max-width: 78%;
            box-shadow: 0 6px 18px rgba(120,90,150,0.08);
            font-size: 14.5px;
            line-height: 1.5;
            color: #3a2f42;
        }

        .bubble-label {
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.75;
            margin-bottom: 4px;
        }

        /* ---------- Section headers ---------- */
        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 25px;
            font-weight: 700;
            color: #362c40;
            margin-top: 46px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .section-subtitle {
            font-size: 14px;
            color: #83788e;
            margin-bottom: 20px;
        }

        /* ---------- Result cards ---------- */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 18px;
        }

        .stat-card {
            background: rgba(255,255,255,0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.8);
            border-radius: 16px;
            padding: 16px 12px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(120,90,150,0.08);
        }

        .stat-card .stat-icon {
            font-size: 22px;
            margin-bottom: 6px;
        }

        .stat-card .stat-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #9c8fab;
            margin-bottom: 4px;
        }

        .stat-card .stat-value {
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #3a2f42;
        }

        .stat-card.highlight {
            background: linear-gradient(145deg, #7b5cf0, #b6539b);
            border: none;
        }

        .stat-card.highlight .stat-label,
        .stat-card.highlight .stat-value {
            color: white;
        }

        /* ---------- Cycle wheel ---------- */
        .wheel-wrap {
            display: flex;
            justify-content: center;
            margin: 10px 0 4px 0;
        }

        .phase-legend {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 14px;
            margin-top: 14px;
            font-size: 12.5px;
            color: #695e75;
        }

        .phase-legend .dot {
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            margin-right: 5px;
        }

        .disclaimer-text {
            font-size: 12.5px;
            color: #948b9e;
            margin-top: 16px;
            line-height: 1.5;
        }

        /* ---------- Footer ---------- */
        .credit-footer-wrap {
            display: flex;
            justify-content: center;
            margin-top: 18px;
        }

        .credit-badge {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255,255,255,0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(200,190,220,0.5);
            padding: 7px 16px 7px 7px;
            border-radius: 999px;
            box-shadow: 0 6px 18px rgba(120,90,150,0.16);
        }

        .credit-avatar {
            width: 32px;
            height: 32px;
            min-width: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #7b5cf0, #b6539b);
            color: white;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .credit-text {
            display: flex;
            flex-direction: column;
            line-height: 1.25;
        }

        .credit-eyebrow {
            font-size: 9.5px;
            font-weight: 600;
            letter-spacing: 0.03em;
            color: #9c8fab;
        }

        .credit-name {
            font-family: 'Outfit', sans-serif;
            font-size: 12.5px;
            font-weight: 700;
            color: #362c40;
        }

        /* ---------- Misc input polish ---------- */
        div[data-testid="stDateInput"] label, div[data-testid="stNumberInput"] label {
            font-weight: 600 !important;
            color: #4b3b57 !important;
            font-size: 13.5px !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #7b5cf0, #b6539b) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 10px 0 !important;
            box-shadow: 0 8px 22px rgba(123,92,240,0.28) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 26px rgba(123,92,240,0.36) !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">🌸 AI Women's Health Companion</div>
        <div class="hero-title">HerHealth AI</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Session state
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# Chat history
# --------------------------------------------------

if st.session_state.messages:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    for message in st.session_state.messages:

        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-row user">
                    <div class="avatar user-avatar">You</div>
                    <div class="chat-user">{message["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.markdown(
                f"""
                <div class="chat-row ai">
                    <div class="avatar ai-avatar">🌸</div>
                    <div class="chat-ai">
                        <div class="bubble-label">HerHealth AI</div>
                        {message["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="glass-panel" style="text-align:center; color:#8b7f97;">
            💬 Ask me anything about periods, PMS, PCOS, pregnancy, or menstrual health.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Question input
# --------------------------------------------------

question = st.chat_input("Ask a health question...")

# --------------------------------------------------
# Knowledge base (chunked for retrieval)
# --------------------------------------------------

knowledge_chunks = [
    {
        "topic": "period cramps",
        "text": (
            "Period cramps are common and are often caused by contractions "
            "of the uterus. Gentle activity, warmth, rest and adequate sleep "
            "may help some people. If the pain is severe, suddenly worse, "
            "or regularly interferes with daily activities, consider speaking "
            "with a healthcare professional."
        ),
    },
    {
        "topic": "menstrual cycle",
        "text": (
            "Menstrual cycles can vary between people and from month to month, "
            "typically ranging from 21 to 35 days. Tracking your cycle can help "
            "you understand your personal pattern. Significant or persistent "
            "changes should be discussed with a healthcare professional."
        ),
    },
    {
        "topic": "pregnancy",
        "text": (
            "Pregnancy symptoms can vary widely, including a missed period, "
            "nausea, fatigue, and breast tenderness. A missed period can have "
            "different causes, and a pregnancy test may help determine whether "
            "pregnancy is possible. For pregnancy-related concerns, consult "
            "a qualified healthcare professional."
        ),
    },
    {
        "topic": "PCOS",
        "text": (
            "PCOS (Polycystic Ovary Syndrome) is a common hormonal condition "
            "that can affect menstrual cycles, ovulation, skin and hair growth. "
            "Symptoms vary between people. A healthcare professional can "
            "evaluate symptoms and provide appropriate diagnosis and treatment."
        ),
    },
    {
        "topic": "headache",
        "text": (
            "Headaches can have many causes including dehydration, stress, "
            "lack of sleep, and hormonal changes around the menstrual cycle. "
            "Rest, hydration and regular sleep may help some mild headaches. "
            "Severe or unusual headaches should be evaluated by a healthcare "
            "professional."
        ),
    },
    {
        "topic": "PMS",
        "text": (
            "Premenstrual syndrome (PMS) refers to physical and emotional "
            "symptoms that can appear in the days before a period, such as "
            "mood changes, bloating, fatigue, and food cravings, typically "
            "easing once the period starts. Severe symptoms affecting daily "
            "life are worth discussing with a healthcare professional."
        ),
    },
    {
        "topic": "menstrual hygiene",
        "text": (
            "Good menstrual hygiene includes changing pads, tampons, or "
            "menstrual cups regularly (roughly every 4-8 hours), washing "
            "hands before and after changing products, and using plain water "
            "for cleaning rather than harsh soaps or douches."
        ),
    },
]

DISCLAIMER = (
    "\n\n*This is general information, not a diagnosis. Please consult a "
    "qualified healthcare professional for personal medical advice.*"
)


# --------------------------------------------------
# Embedding model (loaded once, cached)
# --------------------------------------------------

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def build_knowledge_embeddings(_model):
    texts = [chunk["text"] for chunk in knowledge_chunks]
    embeddings = _model.encode(texts, normalize_embeddings=True)
    return np.array(embeddings)


SIMILARITY_THRESHOLD = 0.35  # below this, treat the query as off-topic/unmatched


def retrieve_context(query, model, chunk_embeddings, top_k=2):
    """
    Real semantic retrieval: embed the query, compare against knowledge
    chunk embeddings using cosine similarity, return the most relevant
    chunks as context for the LLM. Returns an empty list if nothing is
    actually relevant, instead of always forcing the top-k chunks.
    """
    query_embedding = model.encode([query], normalize_embeddings=True)[0]

    # Cosine similarity (embeddings are already normalized, so this is a dot product)
    similarities = chunk_embeddings @ query_embedding

    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Only keep chunks that actually pass the relevance threshold
    retrieved = [
        knowledge_chunks[i]["text"]
        for i in top_indices
        if similarities[i] >= SIMILARITY_THRESHOLD
    ]
    return retrieved


# --------------------------------------------------
# LLM generation (free — via Groq API)
# --------------------------------------------------

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"  # fast, free-tier friendly Groq model


def generate_answer(query, retrieved_context):
    """
    Real generation step: pass retrieved context + the user's question
    to Groq's hosted LLM API (free tier, no local install needed — works
    when deployed online, not just on your own machine).

    If no relevant context was retrieved (e.g. a greeting or an
    off-topic question), the model is told there's no matching topic so
    it can respond naturally instead of forcing an unrelated health answer.
    """
    if retrieved_context:
        context_text = "\n\n".join(retrieved_context)
        system_prompt = (
            "You are HerHealth AI, a friendly women's health information "
            "assistant. Answer the user's question using ONLY the provided "
            "context below. Keep the tone warm, clear, and non-diagnostic. "
            "Never diagnose a condition or prescribe treatment. Always close "
            "by encouraging the user to consult a healthcare professional "
            "for personal medical concerns. Keep answers concise "
            "(3-5 sentences).\n\n"
            f"Context:\n{context_text}"
        )
    else:
        system_prompt = (
            "You are HerHealth AI, a friendly women's health information "
            "assistant. The user's message does not match any topic in "
            "your knowledge base (which currently covers: period cramps, "
            "menstrual cycles, pregnancy, PCOS, headaches, PMS, and "
            "menstrual hygiene). If it's a greeting or small talk, respond "
            "warmly and briefly, and mention you can help with women's "
            "health questions. If it's a real question outside your "
            "knowledge base, say you don't have information on that "
            "specific topic yet and suggest they consult a healthcare "
            "professional. Do NOT invent an answer about an unrelated "
            "topic. Keep it to 1-3 sentences."
        )

    # Prefer Streamlit secrets (used when deployed on Streamlit Cloud),
    # fall back to a local environment variable (used when running locally)
    api_key = st.secrets.get("GROQ_API_KEY", None) if hasattr(st, "secrets") else None
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        if retrieved_context:
            fallback = " ".join(retrieved_context)
            return (
                fallback
                + DISCLAIMER
                + "\n\n*(Live AI generation unavailable — no GROQ_API_KEY set. "
                "See SETUP.md.)*"
            )
        return (
            "Hi! I can help with general women's health questions "
            "(periods, PMS, PCOS, and more). What would you like to know?"
        )

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                "max_tokens": 300,
                "temperature": 0.4,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        if retrieved_context:
            fallback = " ".join(retrieved_context)
            return fallback + DISCLAIMER + f"\n\n*(Note: generation unavailable — {str(e)})*"
        return f"*(Note: generation unavailable — {str(e)})*"


# --------------------------------------------------
# Process question
# --------------------------------------------------

if question:

    # Store user question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Real RAG pipeline:
    # 1. Load embedding model + precomputed knowledge base embeddings
    embed_model = load_embedding_model()
    chunk_embeddings = build_knowledge_embeddings(embed_model)

    # 2. Retrieve the most semantically relevant chunks
    with st.spinner("Thinking..."):
        retrieved_context = retrieve_context(question, embed_model, chunk_embeddings)

        # 3. Generate a natural-language answer grounded in that context
        answer = generate_answer(question, retrieved_context)

    # Store AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    # Refresh page
    st.rerun()


# --------------------------------------------------
# Cycle Tracker
# --------------------------------------------------

st.markdown(
    """
    <div class="section-title">🌷 Cycle Tracker</div>
    <div class="section-subtitle">
        Enter the first day of your most recent period to see your estimated
        cycle map — next period, ovulation, and fertile window.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    last_period_date = st.date_input(
        "Last period date",
        value=None,
        format="DD-MM-YYYY",
    )

with col2:
    cycle_length = st.number_input(
        "Cycle length (days)",
        min_value=15,
        max_value=45,
        value=28,
        step=1,
        help="Average number of days between periods (typically 21-35 days).",
    )

calculate = st.button("✨ Map my cycle", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if calculate:
    if last_period_date is None:
        st.warning("Please enter the first day of your most recent period.")
    else:
        cycle_length = int(cycle_length)
        next_period_date = last_period_date + timedelta(days=cycle_length)
        period_length = 5  # assumed average period length for wheel shading

        # Ovulation is typically estimated ~14 days before the next period
        estimated_ovulation = next_period_date - timedelta(days=14)

        # Fertile window is commonly estimated as ~5 days before to 1 day after ovulation
        fertile_start = estimated_ovulation - timedelta(days=5)
        fertile_end = estimated_ovulation + timedelta(days=1)

        today = datetime.now().date()
        days_since_start = (today - last_period_date).days % cycle_length
        day_in_cycle = days_since_start + 1

        # Determine current phase label
        ov_day = (estimated_ovulation - last_period_date).days % cycle_length
        fert_start_day = (fertile_start - last_period_date).days % cycle_length
        fert_end_day = (fertile_end - last_period_date).days % cycle_length

        if 0 <= days_since_start < period_length:
            phase_label, phase_color = "Menstrual phase", "#e08a6f"
        elif fert_start_day <= days_since_start <= fert_end_day:
            phase_label, phase_color = "Fertile window", "#6dc9c0"
        elif days_since_start < ov_day:
            phase_label, phase_color = "Follicular phase", "#f2c14e"
        else:
            phase_label, phase_color = "Luteal phase", "#8d6fb8"

        # ---------------- Cycle wheel (SVG donut) ----------------
        import math

        def angle_for_day(d):
            return (d / cycle_length) * 360 - 90

        def polar_to_xy(cx, cy, r, angle_deg):
            a = math.radians(angle_deg)
            return cx + r * math.cos(a), cy + r * math.sin(a)

        def arc_path(cx, cy, r, start_day, end_day, total):
            start_angle = angle_for_day(start_day)
            end_angle = angle_for_day(end_day)
            x1, y1 = polar_to_xy(cx, cy, r, start_angle)
            x2, y2 = polar_to_xy(cx, cy, r, end_angle)
            sweep_days = (end_day - start_day) % total
            large_arc = 1 if sweep_days > total / 2 else 0
            return f"M {x1:.1f} {y1:.1f} A {r} {r} 0 {large_arc} 1 {x2:.1f} {y2:.1f}"

        cx, cy, r = 110, 110, 82
        marker_angle = angle_for_day(days_since_start)
        marker_x, marker_y = polar_to_xy(cx, cy, r, marker_angle)

        svg = f"""
        <svg width="220" height="220" viewBox="0 0 220 220">
            <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#f0e8f4" stroke-width="16"/>
            <path d="{arc_path(cx, cy, r, 0, period_length, cycle_length)}"
                  fill="none" stroke="#e08a6f" stroke-width="16" stroke-linecap="round"/>
            <path d="{arc_path(cx, cy, r, fert_start_day, fert_end_day, cycle_length)}"
                  fill="none" stroke="#6dc9c0" stroke-width="16" stroke-linecap="round"/>
            <circle cx="{marker_x:.1f}" cy="{marker_y:.1f}" r="9" fill="{phase_color}" stroke="white" stroke-width="3"/>
            <text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="Outfit, sans-serif"
                  font-size="26" font-weight="800" fill="#362c40">Day {day_in_cycle}</text>
            <text x="{cx}" y="{cy+16}" text-anchor="middle" font-family="Manrope, sans-serif"
                  font-size="12" fill="#83788e">of {cycle_length}-day cycle</text>
        </svg>
        """

        st.markdown(f'<div class="wheel-wrap">{svg}</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="text-align:center; font-weight:700; color:{phase_color}; font-family:'Outfit', sans-serif; font-size:16px;">
                {phase_label}
            </div>
            <div class="phase-legend">
                <span><span class="dot" style="background:#e08a6f;"></span>Period</span>
                <span><span class="dot" style="background:#f2c14e;"></span>Follicular</span>
                <span><span class="dot" style="background:#6dc9c0;"></span>Fertile window</span>
                <span><span class="dot" style="background:#8d6fb8;"></span>Luteal</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="stat-grid">
                <div class="stat-card highlight">
                    <div class="stat-icon">🩸</div>
                    <div class="stat-label">Next period</div>
                    <div class="stat-value">{next_period_date.strftime('%d %b %Y')}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🥚</div>
                    <div class="stat-label">Ovulation</div>
                    <div class="stat-value">{estimated_ovulation.strftime('%d %b %Y')}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🌱</div>
                    <div class="stat-label">Fertile window</div>
                    <div class="stat-value">{fertile_start.strftime('%d %b')} – {fertile_end.strftime('%d %b')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="disclaimer-text">
        This is only an estimate. Menstrual cycles can vary due to stress,
        health conditions, travel, and other factors. This tool does not
        provide medical advice or contraceptive guidance.
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Developer credit (sits in normal page flow, below the tracker)
# --------------------------------------------------

st.markdown(
    """
    <div class="credit-footer-wrap">
        <div class="credit-badge">
            <div class="credit-avatar">NC</div>
            <div class="credit-text">
                <div class="credit-eyebrow">Developed by</div>
                <div class="credit-name">Nikita Chougule</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
