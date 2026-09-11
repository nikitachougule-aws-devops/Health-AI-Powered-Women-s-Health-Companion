import streamlit as st
from datetime import datetime, timedelta

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
# Basic RAG-style knowledge
# --------------------------------------------------

health_knowledge = {
    "period cramps": (
        "Period cramps are common and are often caused by contractions "
        "of the uterus. Gentle activity, warmth, rest and adequate sleep "
        "may help some people. If the pain is severe, suddenly worse, "
        "or regularly interferes with daily activities, consider speaking "
        "with a healthcare professional."
    ),

    "menstrual": (
        "Menstrual cycles can vary between people and from month to month. "
        "Tracking your cycle can help you understand your personal pattern. "
        "Significant or persistent changes should be discussed with a "
        "healthcare professional."
    ),

    "pregnancy": (
        "Pregnancy symptoms can vary widely. A missed period can have "
        "different causes, and a pregnancy test may help determine whether "
        "pregnancy is possible. For pregnancy-related concerns, consult "
        "a qualified healthcare professional."
    ),

    "pcos": (
        "PCOS is a common hormonal condition that can affect menstrual "
        "cycles, ovulation, skin and hair. Symptoms vary between people. "
        "A healthcare professional can evaluate symptoms and provide "
        "appropriate diagnosis and treatment."
    ),

    "headache": (
        "Headaches can have many causes including dehydration, stress, "
        "lack of sleep and other conditions. Rest, hydration and regular "
        "sleep may help some mild headaches. Severe or unusual headaches "
        "should be evaluated by a healthcare professional."
    ),

    "default": (
        "I can provide general women's health information, but I cannot "
        "diagnose medical conditions. Please consult a qualified healthcare "
        "professional for personal medical advice, diagnosis or treatment."
    ),
}


def retrieve_answer(query):
    """
    Simple keyword-based retrieval.

    This is the first RAG layer:
    Query -> find relevant knowledge -> return context.
    """

    query_lower = query.lower()

    # Check specific topics
    if "cramp" in query_lower or "period pain" in query_lower:
        return health_knowledge["period cramps"]

    if "period" in query_lower or "menstrual" in query_lower:
        return health_knowledge["menstrual"]

    if "pregnan" in query_lower:
        return health_knowledge["pregnancy"]

    if "pcos" in query_lower:
        return health_knowledge["pcos"]

    if "headache" in query_lower or "head pain" in query_lower:
        return health_knowledge["headache"]

    return health_knowledge["default"]


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

    # Retrieve relevant information
    answer = retrieve_answer(question)

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
# Women's Health Education
# --------------------------------------------------

st.markdown(
    """
    <div class="section-title">📚 Women's Health Education</div>
    <div class="section-subtitle">
        Explore simple educational information about periods, PMS, hygiene,
        healthy habits, and when to seek care.
    </div>
    """,
    unsafe_allow_html=True,
)

education_topics = [
    {
        "emoji": "🩸",
        "title": "Menstrual Cycle Basics",
        "summary": "Understand the basic stages of the menstrual cycle.",
        "content": (
            "The menstrual cycle is typically counted from the first day of "
            "one period to the first day of the next, and averages about "
            "28 days, though anywhere from 21 to 35 days is common.\n\n"
            "**The main phases are:**\n"
            "- **Menstrual phase** – the uterine lining sheds (the period itself), usually lasting 3-7 days.\n"
            "- **Follicular phase** – hormone levels rise and the body prepares an egg for release; this overlaps with the period and continues after it.\n"
            "- **Ovulation** – an egg is released, generally around the midpoint of the cycle.\n"
            "- **Luteal phase** – the time between ovulation and the next period, when PMS symptoms can occur.\n\n"
            "Cycle length and symptoms can vary from person to person and month to month, and that variation is usually normal."
        ),
    },
    {
        "emoji": "🌸",
        "title": "Period Pain",
        "summary": "Learn about common cramps and when pain needs attention.",
        "content": (
            "Cramps (medically called dysmenorrhea) happen when the uterus "
            "contracts to help shed its lining. Mild to moderate cramping "
            "in the lower abdomen or back is common, especially in the "
            "first couple of days of a period.\n\n"
            "**Things that may offer comfort:**\n"
            "- A heating pad or warm bath\n"
            "- Gentle movement or stretching\n"
            "- Adequate rest and hydration\n"
            "- Over-the-counter pain relief, used as directed\n\n"
            "**Consider speaking with a healthcare professional if:**\n"
            "- Pain is severe or suddenly much worse than usual\n"
            "- Pain regularly stops you from going about daily activities\n"
            "- Pain doesn't improve with usual comfort measures\n"
            "- You notice new symptoms alongside the pain"
        ),
    },
    {
        "emoji": "💗",
        "title": "PMS",
        "summary": "Learn about common symptoms before a period.",
        "content": (
            "Premenstrual syndrome (PMS) refers to physical and emotional "
            "symptoms that can appear in the days or weeks before a period, "
            "typically easing once the period starts.\n\n"
            "**Common symptoms include:**\n"
            "- Mood changes, irritability, or feeling low\n"
            "- Bloating or breast tenderness\n"
            "- Fatigue or trouble sleeping\n"
            "- Food cravings\n"
            "- Headaches\n\n"
            "Keeping a simple symptom diary can help you notice your own "
            "patterns. If symptoms feel severe or significantly affect your "
            "daily life or relationships, it's worth discussing with a "
            "healthcare professional, as more intensive support is available."
        ),
    },
    {
        "emoji": "🧼",
        "title": "Menstrual Hygiene",
        "summary": "Simple habits for comfortable period management.",
        "content": (
            "Good menstrual hygiene supports comfort and helps reduce the "
            "risk of infection.\n\n"
            "**General guidance:**\n"
            "- Change pads, tampons, or empty a menstrual cup regularly, "
            "generally every 4-8 hours depending on the product and flow\n"
            "- Wash hands before and after changing period products\n"
            "- Rinse or wash the genital area with plain water during a "
            "shower; harsh soaps or douches aren't necessary and can cause irritation\n"
            "- Choose breathable, cotton underwear where possible\n"
            "- Follow the product instructions for tampons or cups, and be "
            "aware of guidance around toxic shock syndrome (TSS) if using tampons\n\n"
            "Everyone's flow and preferences differ, so it's fine to try "
            "different products to see what feels most comfortable."
        ),
    },
    {
        "emoji": "🥗",
        "title": "Healthy Habits",
        "summary": "Everyday habits that support general wellbeing.",
        "content": (
            "A few everyday habits can support overall menstrual and general "
            "health, though they aren't a substitute for medical care when needed.\n\n"
            "**Habits that may help:**\n"
            "- Eating a balanced diet with iron-rich foods, especially during and after your period\n"
            "- Staying hydrated\n"
            "- Getting regular, moderate exercise\n"
            "- Prioritizing consistent, adequate sleep\n"
            "- Managing stress through activities that work for you\n"
            "- Tracking your cycle to understand your own patterns\n\n"
            "Small, sustainable habits tend to be more helpful over time than "
            "drastic short-term changes."
        ),
    },
    {
        "emoji": "🚨",
        "title": "When to Seek Medical Care",
        "summary": "Know when symptoms should not simply be ignored.",
        "content": (
            "Most period-related symptoms are common and manageable, but "
            "some signs are worth discussing with a healthcare professional "
            "rather than managing alone.\n\n"
            "**Consider seeking care if you experience:**\n"
            "- Very heavy bleeding (soaking through a pad or tampon every hour for several hours)\n"
            "- Periods lasting longer than about 7 days\n"
            "- Severe pain that isn't relieved by usual measures\n"
            "- Bleeding between periods or after sex\n"
            "- Periods that suddenly become irregular after being regular\n"
            "- Missed periods when pregnancy is possible\n"
            "- Symptoms of infection, such as unusual discharge, odor, fever, or itching\n"
            "- Any symptom that worries you or feels different from your normal pattern\n\n"
            "When in doubt, it's always reasonable to check in with a doctor, "
            "nurse, or other qualified healthcare provider — they can properly "
            "evaluate your specific situation."
        ),
    },
]

for topic in education_topics:
    with st.expander(f"{topic['emoji']}  **{topic['title']}** — {topic['summary']}"):
        st.markdown(topic["content"])


# --------------------------------------------------
# Information section
# --------------------------------------------------

st.markdown(
    """
    <div class="info-box">
        <strong>About HerHealth AI</strong><br>
        This application provides general women's health information.
        It is not a replacement for professional medical advice.
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        HerHealth AI · Women's Health Companion
    </div>
    """,
    unsafe_allow_html=True,
)