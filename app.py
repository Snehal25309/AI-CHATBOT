import streamlit as st
import pickle
from groq import Groq
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# LOAD MODEL + DATASET
# =========================================================

vectorizer = pickle.load(
    open("tfidf_vectorizer.pkl", "rb")
)

dataset = pickle.load(
    open("chatbot_model.pkl", "rb")
)

question_vectors = vectorizer.transform(
    dataset["question"]
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# DATASET SEARCH
# =========================================================

def search_dataset(question):

    user_vector = vectorizer.transform([question])

    similarity = cosine_similarity(
        user_vector,
        question_vectors
    )

    index = similarity.argmax()
    score = similarity.max()

    if score >= 0.90:
        answer = dataset.iloc[index]["answer"]
        return answer, score

    return None, score


def ask_cloud_ai(question):

    try:
        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a helpful AI assistant.
Give simple, clear and accurate answers.
If the question is technical, explain it step by step when useful.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AI Error: {e}"
# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=80
    )

    st.title("AI Chatbot")

    st.write("---")

    st.markdown("### 📋 Menu")

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.session_state.page = "Home"

    if st.button(
        "💬 New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.page = "New Chat"

    if st.button(
        "📜 Chat History",
        use_container_width=True
    ):
        st.session_state.page = "History"

    if st.button(
        "⚙ Settings",
        use_container_width=True
    ):
        st.session_state.page = "Settings"

    if st.button(
        "ℹ About",
        use_container_width=True
    ):
        st.session_state.page = "About"

    st.write("---")

    st.success("🟢 Online")


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    st.markdown(
        """
        <h1 style="
            font-size:42px;
            font-weight:800;
            color:#172554;
            margin-bottom:0;
        ">
            🤖 AI Chatbot
        </h1>

        <p style="
            font-size:18px;
            color:#64748B;
            margin-top:5px;
        ">
            Your Smart AI Assistant
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")


    # =====================================================
    # DASHBOARD CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💬 Chats",
            len(st.session_state.messages)
        )

    with col2:
        st.metric(
            "📚 Dataset",
            f"{len(dataset)}+"
        )

    with col3:
        st.metric(
            "🤖 AI Model",
            "GPT-OSS 20B"
        )

    with col4:
        st.metric(
            "⚡ Status",
            "Online"
        )

    st.write("")


  


    # =====================================================
    # CHAT AREA
    # =====================================================

    st.subheader("💬 Conversation")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask Anything...",
        key="home_chat_input"
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        dataset_answer, score = search_dataset(prompt)

        if dataset_answer is not None:

            answer = dataset_answer

            source = (
                f"📚 Dataset "
                f"(Similarity: {score:.2f})"
            )

        else:

            with st.spinner(
                "🤖 AI is thinking..."
            ):

                answer = ask_cloud_ai(prompt)

            source = "☁️ Cloud AI - Groq"

        final_answer = (
            answer
            + "\n\n---\n"
            + source
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final_answer
            }
        )

        st.rerun()


# =========================================================
# NEW CHAT PAGE
# =========================================================

elif st.session_state.page == "New Chat":

    st.title("💬 New Chat")

    st.caption(
        "Start a new conversation with your AI Assistant"
    )

    st.divider()


    # =====================================================
# FEATURE CARDS
# =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:
     st.markdown(
        """
        <div style="
            background:#EFF6FF;
            padding:22px;
            border-radius:18px;
            text-align:center;
            border:1px solid #BFDBFE;
        ">
            <div style="font-size:45px;">🐍</div>
            <h3 style="color:#1E3A8A;">Python</h3>
            <p style="color:#64748B;">Learn Python programming</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col2:
     st.markdown(
        """
        <div style="
            background:#EEF2FF;
            padding:22px;
            border-radius:18px;
            text-align:center;
            border:1px solid #C7D2FE;
        ">
            <div style="font-size:45px;">🤖</div>
            <h3 style="color:#1E3A8A;">Artificial Intelligence</h3>
            <p style="color:#64748B;">Explore AI concepts</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with col3:
     st.markdown(
        """
        <div style="
            background:#F0FDF4;
            padding:22px;
            border-radius:18px;
            text-align:center;
            border:1px solid #BBF7D0;
        ">
            <div style="font-size:45px;">📊</div>
            <h3 style="color:#166534;">Machine Learning</h3>
            <p style="color:#64748B;">Understand ML concepts</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:25px;
        color:#64748B;
        font-size:16px;
    ">
        💡 Tip: Try asking
        <b>"What is Python?"</b>
        or
        <b>"Explain Machine Learning"</b>
    </div>
    """,
    unsafe_allow_html=True
)

    st.write("")


    # =====================================================
    # DISPLAY PREVIOUS MESSAGES
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])


    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Ask Anything...",
        key="new_chat_input"
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        dataset_answer, score = search_dataset(prompt)

        if dataset_answer is not None:

            answer = dataset_answer

            source = (
                f"📚 Dataset "
                f"(Similarity: {score:.2f})"
            )

        else:

            with st.spinner(
                "🤖 AI is thinking..."
            ):

                answer = ask_cloud_ai(prompt)

            source = "☁️ Cloud AI - Groq"

        final_answer = (
            answer
            + "\n\n---\n"
            + source
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": final_answer
            }
        )

        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

elif st.session_state.page == "History":

    st.title("📜 Chat History")

    st.write("")

    if len(st.session_state.messages) == 0:

        st.info(
            "No chat history found."
        )

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                st.markdown(
                    f"**👤 You:** {message['content']}"
                )

            else:

                st.markdown(
                    f"**🤖 Bot:** {message['content']}"
                )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.title("⚙ Settings")

    st.write("")

    st.subheader("🤖 AI Model")

    st.info(
        "Current Model: Llama 3.2"
    )

    st.subheader("📚 Dataset")

    st.info(
        f"Questions available: {len(dataset)}"
    )

    st.subheader(
        "🎯 Dataset Similarity Threshold"
    )

    st.info(
        "Current threshold: 0.90"
    )


# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "About":

    st.title("ℹ About")

    st.write("")

    with st.container(border=True):

        st.subheader("🤖 AI Chatbot")

        st.write(
            """
This AI Chatbot is developed using:

- Python
- Streamlit
- NLP
- TF-IDF
- Cosine Similarity
- Scikit-learn
- Ollama
- Llama 3.2

### How it works

1. User enters a question.
2. TF-IDF converts the question into numerical features.
3. Cosine Similarity compares it with the dataset.
4. If the similarity is high enough, the dataset answer is displayed.
5. Otherwise, Ollama generates an AI response.
"""
        )


# =========================================================
# FOOTER
# =========================================================

st.write("---")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Dataset",
        f"{len(dataset)}+"
    )

with c2:
    st.metric(
        "Status",
        "Online"
    )

with c3:
    st.metric(
        "Version",
        "2.0"
    )

st.markdown(
    """
    <div class="footer">
        © 2026 AI Chatbot | Built with Streamlit + Ollama
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MODERN UI CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background: linear-gradient(
            135deg,
            #EFF6FF 0%,
            #F8FAFC 50%,
            #EEF2FF 100%
        );
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554 0%,
            #1E3A8A 50%,
            #2563EB 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 25px;
        font-weight: 700;
    }


    /* Headings */

    h1 {
        font-weight: 800 !important;
    }

    h2 {
        color: #1E3A8A !important;
    }

    h3 {
        color: #1E40AF !important;
    }


    /* Metric cards */

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.92);
        border: 1px solid #DBEAFE;
        border-radius: 18px;
        padding: 18px;
        box-shadow:
            0 4px 15px rgba(30,64,175,0.08);
        transition: 0.3s;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow:
            0 8px 25px rgba(30,64,175,0.15);
    }

    div[data-testid="stMetricValue"] {
        color: #1E3A8A;
        font-weight: 800;
    }


    /* Buttons */

    .stButton > button {
        background: linear-gradient(
            90deg,
            #2563EB,
            #4F46E5
        );

        color: white !important;
        border: none;
        border-radius: 12px;
        height: 45px;
        font-size: 15px;
        font-weight: 600;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 5px 15px rgba(37,99,235,0.30);

        color: white !important;
    }


    /* Welcome cards */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.88);
        border: 1px solid #DBEAFE;
        border-radius: 20px;
        box-shadow:
            0 5px 20px rgba(30,64,175,0.08);
    }


    /* Chat messages */

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.82);
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #E0E7FF;
    }


    /* Chat input */

    [data-testid="stChatInput"] {
        background: white;
        border-radius: 18px;
        border: 2px solid #BFDBFE;
        box-shadow:
            0 5px 20px rgba(37,99,235,0.10);
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #2563EB;
        box-shadow:
            0 0 0 3px rgba(37,99,235,0.12);
    }


    /* Alerts */

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: none;
    }


    /* Divider */

    hr {
        border-color: #DBEAFE;
    }


    /* Text */

    p {
        color: #334155;
    }


    /* Footer */

    .footer {
        text-align: center;
        padding: 20px;
        color: #64748B;
        font-size: 14px;
    }


    /* Scrollbar */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #EFF6FF;
    }

    ::-webkit-scrollbar-thumb {
        background: #93C5FD;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #2563EB;
    }

    </style>
    """,
    unsafe_allow_html=True
)
