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
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            background: #fff9fc;
        }

        .hero {
            text-align: center;
            padding: 35px 10px 20px 10px;
        }

        .hero-title {
            font-size: 46px;
            font-weight: 700;
            color: #303044;
            margin-bottom: 8px;
        }

        .hero-subtitle {
            font-size: 22px;
            font-weight: 600;
            color: #6d466d;
            margin-bottom: 10px;
        }

        .hero-description {
            font-size: 16px;
            color: #666;
        }

        .chat-user {
            background: #f6e7ef;
            border: 1px solid #e5ccda;
            border-radius: 14px;
            padding: 14px 18px;
            margin: 12px 0;
        }

        .chat-ai {
            background: #eee8f7;
            border: 1px solid #d9cdea;
            border-radius: 14px;
            padding: 14px 18px;
            margin: 12px 0;
        }

        .label {
            font-weight: 700;
            margin-bottom: 5px;
            color: #51445c;
        }

        .info-box {
            background: #faf5fb;
            border-left: 4px solid #b67ab0;
            padding: 14px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .section-title {
            font-size: 26px;
            font-weight: 700;
            color: #303044;
            margin-top: 40px;
            margin-bottom: 4px;
        }

        .section-subtitle {
            font-size: 15px;
            color: #666;
            margin-bottom: 18px;
        }

        .result-box {
            background: linear-gradient(90deg, #b67ab0, #8d6fb8);
            color: white;
            padding: 18px;
            border-radius: 12px;
            margin-top: 16px;
        }

        .result-box .result-label {
            font-size: 14px;
            opacity: 0.9;
        }

        .result-box .result-date {
            font-size: 22px;
            font-weight: 700;
            margin-top: 4px;
        }

        .disclaimer-text {
            font-size: 13px;
            color: #888;
            margin-top: 10px;
        }

        .footer {
            text-align: center;
            color: #888;
            font-size: 13px;
            margin-top: 40px;
        }

        .credit-badge {
            display: flex;
            align-items: center;
            gap: 12px;
            background: #2b3550;
            border-radius: 12px;
            padding: 12px 18px;
            margin-top: 30px;
        }

        .credit-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #7b5cf0;
            color: white;
            font-weight: 700;
            font-size: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .credit-label {
            color: #a9b2c9;
            font-size: 11px;
            letter-spacing: 0.5px;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 2px;
        }

        .credit-name {
            color: #ffffff;
            font-size: 16px;
            font-weight: 700;
        }

        /* Push chat input up to make room for the fixed credit footer */
        [data-testid="stBottomBlockContainer"] {
            padding-bottom: 34px;
        }

        .fixed-credit-footer {
            position: fixed;
            bottom: 6px;
            left: 50%;
            transform: translateX(-50%);
            font-weight: 700;
            color: #000000;
            font-size: 12px;
            z-index: 999;
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
        <div class="hero-title">🌸 HerHealth AI</div>
        <div class="hero-subtitle">Women's Health Companion</div>
        <div class="hero-description">
            A simple AI-powered women's health information assistant.
        </div>
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

for message in st.session_state.messages:

    if message["role"] == "user":
        st.markdown(
            f"""
            <div class="chat-user">
                <div class="label">You</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            f"""
            <div class="chat-ai">
                <div class="label">HerHealth AI</div>
                {message["content"]}
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
        Enter the first day of your most recent period to get an estimated
        next period date.
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    last_period_date = st.date_input(
        "Last Period Date",
        value=None,
        format="DD-MM-YYYY",
    )

with col2:
    cycle_length = st.number_input(
        "Cycle Length",
        min_value=15,
        max_value=45,
        value=28,
        step=1,
        help="Average number of days between periods (typically 21-35 days).",
    )

if st.button("Calculate Estimated Date", use_container_width=True):
    if last_period_date is None:
        st.warning("Please enter the first day of your most recent period.")
    else:
        next_period_date = last_period_date + timedelta(days=int(cycle_length))

        # Ovulation is typically estimated ~14 days before the next period
        estimated_ovulation = next_period_date - timedelta(days=14)

        # Fertile window is commonly estimated as ~5 days before to 1 day after ovulation
        fertile_start = estimated_ovulation - timedelta(days=5)
        fertile_end = estimated_ovulation + timedelta(days=1)

        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Estimated Next Period</div>
                <div class="result-date">{next_period_date.strftime('%d %B %Y')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-box">
                <strong>Estimated Ovulation:</strong> {estimated_ovulation.strftime('%d %B %Y')}<br>
                <strong>Estimated Fertile Window:</strong>
                {fertile_start.strftime('%d %B')} – {fertile_end.strftime('%d %B %Y')}
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
# Developer credit (fixed at very bottom, below chat input)
# --------------------------------------------------

st.markdown(
    """
    <div class="fixed-credit-footer">
        Created by Nikita Chougule
    </div>
    """,
    unsafe_allow_html=True,
)
