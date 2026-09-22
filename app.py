# import streamlit as st
# import pickle
# from groq import Groq
# from sklearn.metrics.pairwise import cosine_similarity


# # =========================================================
# # PAGE CONFIGURATION
# # =========================================================

# st.set_page_config(
#     page_title="AI Chatbot",
#     page_icon="🤖",
#     layout="wide"
# )


# # =========================================================
# # LOAD MODEL + DATASET
# # =========================================================

# vectorizer = pickle.load(
#     open("tfidf_vectorizer.pkl", "rb")
# )

# dataset = pickle.load(
#     open("chatbot_model.pkl", "rb")
# )

# question_vectors = vectorizer.transform(
#     dataset["question"]
# )


# # =========================================================
# # SESSION STATE
# # =========================================================

# if "page" not in st.session_state:
#     st.session_state.page = "Home"

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# # =========================================================
# # DATASET SEARCH
# # =========================================================

# def search_dataset(question):

#     user_vector = vectorizer.transform([question])

#     similarity = cosine_similarity(
#         user_vector,
#         question_vectors
#     )

#     index = similarity.argmax()
#     score = similarity.max()

#     if score >= 0.90:
#         answer = dataset.iloc[index]["answer"]
#         return answer, score

#     return None, score


# def ask_cloud_ai(question):

#     try:
#         client = Groq(
#             api_key=st.secrets["GROQ_API_KEY"]
#         )

#         response = client.chat.completions.create(
#             model="openai/gpt-oss-20b",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
# You are a helpful AI assistant.
# Give simple, clear and accurate answers.
# If the question is technical, explain it step by step when useful.
# """
#                 },
#                 {
#                     "role": "user",
#                     "content": question
#                 }
#             ]
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         return f"❌ AI Error: {e}"
# # =========================================================
# # SIDEBAR
# # =========================================================

# with st.sidebar:

#     st.image(
#         "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
#         width=80
#     )

#     st.title("AI Chatbot")

#     st.write("---")

#     st.markdown("### 📋 Menu")

#     if st.button(
#         "🏠 Home",
#         use_container_width=True
#     ):
#         st.session_state.page = "Home"

#     if st.button(
#         "💬 New Chat",
#         use_container_width=True
#     ):
#         st.session_state.messages = []
#         st.session_state.page = "New Chat"

#     if st.button(
#         "📜 Chat History",
#         use_container_width=True
#     ):
#         st.session_state.page = "History"

#     if st.button(
#         "⚙ Settings",
#         use_container_width=True
#     ):
#         st.session_state.page = "Settings"

#     if st.button(
#         "ℹ About",
#         use_container_width=True
#     ):
#         st.session_state.page = "About"

#     st.write("---")

#     st.success("🟢 Online")


# # =========================================================
# # HOME PAGE
# # =========================================================

# if st.session_state.page == "Home":

#     st.markdown(
#         """
#         <h1 style="
#             font-size:42px;
#             font-weight:800;
#             color:#172554;
#             margin-bottom:0;
#         ">
#             🤖 AI Chatbot
#         </h1>

#         <p style="
#             font-size:18px;
#             color:#64748B;
#             margin-top:5px;
#         ">
#             Your Smart AI Assistant
#         </p>
#         """,
#         unsafe_allow_html=True
#     )

#     st.write("")


#     # =====================================================
#     # DASHBOARD CARDS
#     # =====================================================

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "💬 Chats",
#             len(st.session_state.messages)
#         )

#     with col2:
#         st.metric(
#             "📚 Dataset",
#             f"{len(dataset)}+"
#         )

#     with col3:
#         st.metric(
#             "🤖 AI Model",
#             "GPT-OSS 20B"
#         )

#     with col4:
#         st.metric(
#             "⚡ Status",
#             "Online"
#         )

#     st.write("")


  


#     # =====================================================
#     # CHAT AREA
#     # =====================================================

#     st.subheader("💬 Conversation")

#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     prompt = st.chat_input(
#         "Ask Anything...",
#         key="home_chat_input"
#     )

#     if prompt:

#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         )

#         with st.chat_message("user"):
#             st.write(prompt)

#         dataset_answer, score = search_dataset(prompt)

#         if dataset_answer is not None:

#             answer = dataset_answer

#             source = (
#                 f"📚 Dataset "
#                 f"(Similarity: {score:.2f})"
#             )

#         else:

#             with st.spinner(
#                 "🤖 AI is thinking..."
#             ):

#                 answer = ask_cloud_ai(prompt)

#             source = "☁️ Cloud AI - Groq"

#         final_answer = (
#             answer
#             + "\n\n---\n"
#             + source
#         )

#         st.session_state.messages.append(
#             {
#                 "role": "assistant",
#                 "content": final_answer
#             }
#         )

#         st.rerun()


# # =========================================================
# # NEW CHAT PAGE
# # =========================================================

# elif st.session_state.page == "New Chat":

#     st.title("💬 New Chat")

#     st.caption(
#         "Start a new conversation with your AI Assistant"
#     )

#     st.divider()


#     # =====================================================
# # FEATURE CARDS
# # =====================================================

#     col1, col2, col3 = st.columns(3)

#     with col1:
#      st.markdown(
#         """
#         <div style="
#             background:#EFF6FF;
#             padding:22px;
#             border-radius:18px;
#             text-align:center;
#             border:1px solid #BFDBFE;
#         ">
#             <div style="font-size:45px;">🐍</div>
#             <h3 style="color:#1E3A8A;">Python</h3>
#             <p style="color:#64748B;">Learn Python programming</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     with col2:
#      st.markdown(
#         """
#         <div style="
#             background:#EEF2FF;
#             padding:22px;
#             border-radius:18px;
#             text-align:center;
#             border:1px solid #C7D2FE;
#         ">
#             <div style="font-size:45px;">🤖</div>
#             <h3 style="color:#1E3A8A;">Artificial Intelligence</h3>
#             <p style="color:#64748B;">Explore AI concepts</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     with col3:
#      st.markdown(
#         """
#         <div style="
#             background:#F0FDF4;
#             padding:22px;
#             border-radius:18px;
#             text-align:center;
#             border:1px solid #BBF7D0;
#         ">
#             <div style="font-size:45px;">📊</div>
#             <h3 style="color:#166534;">Machine Learning</h3>
#             <p style="color:#64748B;">Understand ML concepts</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown(
#     """
#     <div style="
#         text-align:center;
#         margin-top:25px;
#         color:#64748B;
#         font-size:16px;
#     ">
#         💡 Tip: Try asking
#         <b>"What is Python?"</b>
#         or
#         <b>"Explain Machine Learning"</b>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

#     st.write("")


#     # =====================================================
#     # DISPLAY PREVIOUS MESSAGES
#     # =====================================================

#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):

#             st.write(message["content"])


#     # =====================================================
#     # CHAT INPUT
#     # =====================================================

#     prompt = st.chat_input(
#         "Ask Anything...",
#         key="new_chat_input"
#     )

#     if prompt:

#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         )

#         dataset_answer, score = search_dataset(prompt)

#         if dataset_answer is not None:

#             answer = dataset_answer

#             source = (
#                 f"📚 Dataset "
#                 f"(Similarity: {score:.2f})"
#             )

#         else:

#             with st.spinner(
#                 "🤖 AI is thinking..."
#             ):

#                 answer = ask_cloud_ai(prompt)

#             source = "☁️ Cloud AI - Groq"

#         final_answer = (
#             answer
#             + "\n\n---\n"
#             + source
#         )

#         st.session_state.messages.append(
#             {
#                 "role": "assistant",
#                 "content": final_answer
#             }
#         )

#         st.rerun()


# # =========================================================
# # CHAT HISTORY
# # =========================================================

# elif st.session_state.page == "History":

#     st.title("📜 Chat History")

#     st.write("")

#     if len(st.session_state.messages) == 0:

#         st.info(
#             "No chat history found."
#         )

#     else:

#         for message in st.session_state.messages:

#             if message["role"] == "user":

#                 st.markdown(
#                     f"**👤 You:** {message['content']}"
#                 )

#             else:

#                 st.markdown(
#                     f"**🤖 Bot:** {message['content']}"
#                 )


# # =========================================================
# # SETTINGS
# # =========================================================

# elif st.session_state.page == "Settings":

#     st.title("⚙ Settings")

#     st.write("")

#     st.subheader("🤖 AI Model")

#     st.info(
#         "Current Model: GPT-OSS 20B"
#     )

#     st.subheader("📚 Dataset")

#     st.info(
#         f"Questions available: {len(dataset)}"
#     )

#     st.subheader(
#         "🎯 Dataset Similarity Threshold"
#     )

#     st.info(
#         "Current threshold: 0.90"
#     )


# # =========================================================
# # ABOUT
# # =========================================================

# elif st.session_state.page == "About":

#     st.title("ℹ About")

#     st.write("")

#     with st.container(border=True):

#         st.subheader("🤖 AI Chatbot")

#         st.write(
#             """
# This AI Chatbot is developed using:

# - Python
# - Streamlit
# - NLP
# - TF-IDF
# - Cosine Similarity
# - Scikit-learn
# - Ollama
# - Llama 3.2

# ### How it works

# 1. User enters a question.
# 2. TF-IDF converts the question into numerical features.
# 3. Cosine Similarity compares it with the dataset.
# 4. If the similarity is high enough, the dataset answer is displayed.
# 5. Otherwise, Ollama generates an AI response.
# """
#         )


# # =========================================================
# # FOOTER
# # =========================================================

# st.write("---")

# c1, c2, c3 = st.columns(3)

# with c1:
#     st.metric(
#         "Dataset",
#         f"{len(dataset)}+"
#     )

# with c2:
#     st.metric(
#         "Status",
#         "Online"
#     )

# with c3:
#     st.metric(
#         "Version",
#         "2.0"
#     )

# st.markdown(
#     """
#     <div class="footer">
#         © 2026 AI Chatbot | Built with Streamlit + Python + NLP + Groq AI
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# # =========================================================
# # MODERN UI CSS
# # =========================================================

# st.markdown(
#     """
#     <style>

#     /* Main background */

#     .stApp {
#         background: linear-gradient(
#             135deg,
#             #EFF6FF 0%,
#             #F8FAFC 50%,
#             #EEF2FF 100%
#         );
#     }


#     /* Sidebar */

#     section[data-testid="stSidebar"] {
#         background: linear-gradient(
#             180deg,
#             #172554 0%,
#             #1E3A8A 50%,
#             #2563EB 100%
#         );
#     }

#     section[data-testid="stSidebar"] * {
#         color: white !important;
#     }

#     section[data-testid="stSidebar"] h1 {
#         font-size: 25px;
#         font-weight: 700;
#     }


#     /* Headings */

#     h1 {
#         font-weight: 800 !important;
#     }

#     h2 {
#         color: #1E3A8A !important;
#     }

#     h3 {
#         color: #1E40AF !important;
#     }


#     /* Metric cards */

#     div[data-testid="metric-container"] {
#         background: rgba(255,255,255,0.92);
#         border: 1px solid #DBEAFE;
#         border-radius: 18px;
#         padding: 18px;
#         box-shadow:
#             0 4px 15px rgba(30,64,175,0.08);
#         transition: 0.3s;
#     }

#     div[data-testid="metric-container"]:hover {
#         transform: translateY(-3px);
#         box-shadow:
#             0 8px 25px rgba(30,64,175,0.15);
#     }

#     div[data-testid="stMetricValue"] {
#         color: #1E3A8A;
#         font-weight: 800;
#     }


#     /* Buttons */

#     .stButton > button {
#         background: linear-gradient(
#             90deg,
#             #2563EB,
#             #4F46E5
#         );

#         color: white !important;
#         border: none;
#         border-radius: 12px;
#         height: 45px;
#         font-size: 15px;
#         font-weight: 600;
#         transition: 0.3s;
#     }

#     .stButton > button:hover {
#         transform: translateY(-2px);

#         box-shadow:
#             0 5px 15px rgba(37,99,235,0.30);

#         color: white !important;
#     }


#     /* Welcome cards */

#     div[data-testid="stVerticalBlockBorderWrapper"] {
#         background: rgba(255,255,255,0.88);
#         border: 1px solid #DBEAFE;
#         border-radius: 20px;
#         box-shadow:
#             0 5px 20px rgba(30,64,175,0.08);
#     }


#     /* Chat messages */

#     [data-testid="stChatMessage"] {
#         background: rgba(255,255,255,0.82);
#         border-radius: 16px;
#         padding: 12px;
#         margin-bottom: 10px;
#         border: 1px solid #E0E7FF;
#     }


#     /* Chat input */

#     [data-testid="stChatInput"] {
#         background: white;
#         border-radius: 18px;
#         border: 2px solid #BFDBFE;
#         box-shadow:
#             0 5px 20px rgba(37,99,235,0.10);
#     }

#     [data-testid="stChatInput"]:focus-within {
#         border-color: #2563EB;
#         box-shadow:
#             0 0 0 3px rgba(37,99,235,0.12);
#     }


#     /* Alerts */

#     div[data-testid="stAlert"] {
#         border-radius: 14px;
#         border: none;
#     }


#     /* Divider */

#     hr {
#         border-color: #DBEAFE;
#     }


#     /* Text */

#     p {
#         color: #334155;
#     }


#     /* Footer */

#     .footer {
#         text-align: center;
#         padding: 20px;
#         color: #64748B;
#         font-size: 14px;
#     }


#     /* Scrollbar */

#     ::-webkit-scrollbar {
#         width: 8px;
#     }

#     ::-webkit-scrollbar-track {
#         background: #EFF6FF;
#     }

#     ::-webkit-scrollbar-thumb {
#         background: #93C5FD;
#         border-radius: 10px;
#     }

#     ::-webkit-scrollbar-thumb:hover {
#         background: #2563EB;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )


import streamlit as st
import pickle
import time
import os
import re
import base64
from datetime import datetime

from groq import Groq
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Chatbot 4.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CONSTANTS
# =========================================================

DATASET_THRESHOLD = 0.90

FEEDBACK_FILE = "data/feedback.csv"

CHAT_LOG_FILE = "data/chat_history.txt"

SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Marathi"
]

AI_MODES = [
    "General Assistant",
    "Study Assistant",
    "Coding Assistant",
    "College Assistant",
    "Summarizer",
    "Document Assistant"
]


# =========================================================
# LOAD MODEL + DATASET
# =========================================================

@st.cache_resource
def load_models():

    with open(
        "tfidf_vectorizer.pkl",
        "rb"
    ) as f:

        vectorizer = pickle.load(f)


    with open(
        "chatbot_model.pkl",
        "rb"
    ) as f:

        dataset = pickle.load(f)


    question_vectors = vectorizer.transform(
        dataset["question"]
    )


    return (
        vectorizer,
        dataset,
        question_vectors
    )


vectorizer, dataset, question_vectors = load_models()


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "page": "Home",

    "messages": [],

    "total_questions": 0,

    "dataset_answers": 0,

    "groq_answers": 0,

    "response_times": [],

    "feedback": [],

    "last_suggestions": [],

    "last_question": "",

    "selected_language": "English",

    "ai_mode": "General Assistant",

    "theme": "Light",

    "document_text": "",

    "document_name": "",

    "chat_sessions": [],

    "current_session_name": "Current Chat",

    "voice_enabled": False,

    "tts_enabled": False

}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# OPTIONAL IMPORTS
# =========================================================

try:

    from pypdf import PdfReader

    PDF_AVAILABLE = True

except Exception:

    PDF_AVAILABLE = False


try:

    import speech_recognition as sr

    SPEECH_AVAILABLE = True

except Exception:

    SPEECH_AVAILABLE = False


try:

    import pyttsx3

    TTS_AVAILABLE = True

except Exception:

    TTS_AVAILABLE = False


# =========================================================
# DIRECTORY
# =========================================================

os.makedirs(
    "data",
    exist_ok=True
)


# =========================================================
# FEEDBACK
# =========================================================

def save_feedback(
    question,
    answer,
    rating
):

    file_exists = os.path.exists(
        FEEDBACK_FILE
    )


    with open(
        FEEDBACK_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        if not file_exists:

            file.write(
                "timestamp,question,answer,rating\n"
            )


        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        question = str(
            question
        ).replace(
            '"',
            '""'
        )


        answer = str(
            answer
        ).replace(
            '"',
            '""'
        )


        file.write(
            f'"{timestamp}",'
            f'"{question}",'
            f'"{answer}",'
            f'"{rating}"\n'
        )


# =========================================================
# DATASET SEARCH
# =========================================================

def search_dataset(question):

    user_vector = vectorizer.transform(
        [question]
    )


    similarity = cosine_similarity(
        user_vector,
        question_vectors
    )


    index = similarity.argmax()

    score = float(
        similarity.max()
    )


    if score >= DATASET_THRESHOLD:

        answer = dataset.iloc[index][
            "answer"
        ]

        return (
            str(answer),
            score
        )


    return (
        None,
        score
    )


# =========================================================
# CLEAN AI RESPONSE
# =========================================================

def clean_response(text):

    if not text:

        return ""


    return str(text).strip()


# =========================================================
# LANGUAGE INSTRUCTION
# =========================================================

def get_language_instruction():

    language = (
        st.session_state.selected_language
    )


    if language == "Hindi":

        return """
Respond in simple Hindi.
Use English technical terms when necessary.
"""


    if language == "Marathi":

        return """
Respond in simple Marathi.
Use English technical terms when necessary.
"""


    return """
Respond in clear and simple English.
"""


# =========================================================
# AI MODE INSTRUCTION
# =========================================================

def get_mode_instruction():

    mode = st.session_state.ai_mode


    if mode == "Study Assistant":

        return """
You are a Study Assistant.
Explain academic concepts clearly.
Use exam-friendly points, definitions,
examples and short conclusions when useful.
"""


    if mode == "Coding Assistant":

        return """
You are a Coding Assistant.
Help with programming concepts,
debugging, algorithms and code.
Explain code clearly and safely.
"""


    if mode == "College Assistant":

        return """
You are a College Assistant.
Help students with college projects,
subjects, presentations, documentation,
assignments and technical concepts.
"""


    if mode == "Summarizer":

        return """
You are a Summarizer.
Convert long content into concise,
clear and useful points.
Preserve important information.
"""


    if mode == "Document Assistant":

        return """
You are a Document Assistant.
Answer questions using the uploaded
document when relevant.
Do not invent information that is not
supported by the document.
"""


    return """
You are a General AI Assistant.
Give useful, accurate and understandable answers.
"""


# =========================================================
# BUILD GROQ CONTEXT
# =========================================================

def build_conversation_context():

    context = []


    recent_messages = (
        st.session_state.messages[-10:]
    )


    for message in recent_messages:

        role = message.get(
            "role"
        )

        content = message.get(
            "content",
            ""
        )


        if "\n\n---\n" in content:

            content = content.split(
                "\n\n---\n"
            )[0]


        if role in [
            "user",
            "assistant"
        ]:

            context.append(
                {
                    "role": role,
                    "content": content
                }
            )


    return context


# =========================================================
# GROQ AI
# =========================================================

def ask_cloud_ai(
    question,
    document_text=""
):

    try:

        client = Groq(
            api_key=st.secrets[
                "GROQ_API_KEY"
            ]
        )


        system_prompt = f"""
You are the AI engine of a professional
student-friendly chatbot.

{get_mode_instruction()}

{get_language_instruction()}

Rules:

- Give accurate answers.
- Be clear and structured.
- Do not unnecessarily repeat information.
- Use examples when useful.
- For academic questions, make answers
  exam-friendly.
- For programming questions, explain
  important parts of the code.
"""


        if document_text:

            # Limit document context
            limited_document = document_text[
                :12000
            ]


            system_prompt += f"""

The user has uploaded a document.

Document content:

----------------
{limited_document}
----------------

Use this document as the primary source
when answering document-related questions.
"""


        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]


        # Add previous conversation
        messages.extend(
            build_conversation_context()
        )


        # Current question
        messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        response = (
            client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=messages,

                temperature=0.4,

                max_tokens=1500
            )
        )


        return clean_response(
            response.choices[
                0
            ].message.content
        )


    except Exception as error:

        return (
            "❌ **Groq AI Error**\n\n"
            f"{error}"
        )


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

def generate_suggestions(question):

    q = question.lower()


    if "python" in q:

        return [
            "What are Python variables?",
            "Explain Python functions",
            "What is a Python list?"
        ]


    if (
        "machine learning" in q
        or "ml" in q
    ):

        return [
            "What is supervised learning?",
            "What is unsupervised learning?",
            "Explain classification and regression"
        ]


    if (
        "artificial intelligence" in q
        or " ai " in f" {q} "
    ):

        return [
            "What is machine learning?",
            "What is deep learning?",
            "What is NLP?"
        ]


    if (
        "software engineering" in q
        or "software" in q
    ):

        return [
            "What is SDLC?",
            "Explain Agile model",
            "What is RAD model?"
        ]


    if (
        "operating system" in q
        or re.search(r"\bos\b", q)
    ):

        return [
            "What is process scheduling?",
            "Explain Round Robin scheduling",
            "What is context switching?"
        ]


    if "college" in q:

        return [
            "How can I prepare a project?",
            "How should I prepare a presentation?",
            "What is an industrial project?"
        ]


    return [
        "Explain this topic with an example",
        "Give me a simple explanation",
        "What are the advantages and disadvantages?"
    ]


# =========================================================
# PROCESS QUESTION
# =========================================================

def process_question(
    prompt,
    force_groq=False
):

    prompt = prompt.strip()


    if not prompt:

        return


    start_time = time.time()


    st.session_state.last_question = prompt

    st.session_state.total_questions += 1


    dataset_answer = None

    score = 0.0


    # =====================================================
    # DATASET SEARCH
    # =====================================================

    if not force_groq:

        dataset_answer, score = (
            search_dataset(prompt)
        )


    # =====================================================
    # DATASET RESPONSE
    # =====================================================

    if dataset_answer is not None:

        answer = dataset_answer

        source = (
            f"📚 Dataset "
            f"(Similarity: {score:.2f})"
        )

        source_type = "Dataset"

        st.session_state.dataset_answers += 1


    # =====================================================
    # GROQ RESPONSE
    # =====================================================

    else:

        with st.spinner(
            "🤖 AI is thinking..."
        ):

            answer = ask_cloud_ai(
                prompt,
                st.session_state.document_text
            )


        source = (
            "☁️ Groq AI - GPT-OSS 20B"
        )

        source_type = "Groq AI"

        st.session_state.groq_answers += 1


    # =====================================================
    # RESPONSE TIME
    # =====================================================

    response_time = (
        time.time() - start_time
    )


    st.session_state.response_times.append(
        response_time
    )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    final_answer = (
        answer
        + "\n\n---\n"
        + source
        + "\n"
        + f"⏱️ Response time: "
        f"{response_time:.2f} seconds"
    )


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        }
    )


    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer,
            "question": prompt,
            "source": source_type,
            "confidence": score,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
    )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.session_state.last_suggestions = (
        generate_suggestions(prompt)
    )


# =========================================================
# CLEAR CHAT
# =========================================================

def clear_chat():

    st.session_state.messages = []

    st.session_state.last_suggestions = []

    st.session_state.last_question = ""

    st.session_state.document_text = ""

    st.session_state.document_name = ""


# =========================================================
# EXPORT CHAT
# =========================================================

def create_chat_text():

    if not st.session_state.messages:

        return "No chat history available."


    lines = []

    lines.append(
        "=" * 60
    )

    lines.append(
        "AI CHATBOT 4.0 - CHAT EXPORT"
    )

    lines.append(
        "=" * 60
    )

    lines.append("")


    for message in (
        st.session_state.messages
    ):

        role = message.get(
            "role"
        )


        content = message.get(
            "content",
            ""
        )


        if role == "user":

            lines.append(
                "👤 USER:"
            )

            lines.append(
                content
            )


        else:

            lines.append(
                "🤖 AI:"
            )

            if "\n\n---\n" in content:

                content = content.split(
                    "\n\n---\n"
                )[0]


            lines.append(
                content
            )


        lines.append("")


    lines.append(
        "=" * 60
    )

    lines.append(
        "Generated by AI Chatbot 4.0"
    )

    lines.append(
        "=" * 60
    )


    return "\n".join(lines)


# =========================================================
# SEARCH CHAT HISTORY
# =========================================================

def search_chat_history(query):

    query = query.lower().strip()


    if not query:

        return st.session_state.messages


    results = []


    for message in (
        st.session_state.messages
    ):

        content = message.get(
            "content",
            ""
        )


        if query in content.lower():

            results.append(
                message
            )


    return results


# =========================================================
# DOCUMENT READER
# =========================================================

def read_uploaded_document(uploaded_file):

    if uploaded_file is None:

        return "", ""


    filename = uploaded_file.name

    extension = (
        filename
        .lower()
        .split(".")[-1]
    )


    # =====================================================
    # TXT
    # =====================================================

    if extension == "txt":

        try:

            text = uploaded_file.read().decode(
                "utf-8"
            )

            return text, filename

        except Exception:

            return "", filename


    # =====================================================
    # PDF
    # =====================================================

    if extension == "pdf":

        if not PDF_AVAILABLE:

            return "", filename


        try:

            reader = PdfReader(
                uploaded_file
            )


            pages = []


            for page in reader.pages:

                page_text = (
                    page.extract_text()
                    or ""
                )

                pages.append(
                    page_text
                )


            return (
                "\n".join(pages),
                filename
            )


        except Exception:

            return "", filename


    return "", filename


# =========================================================
# TEXT TO SPEECH
# =========================================================

def generate_speech(text):

    if not TTS_AVAILABLE:

        return None


    try:

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            165
        )


        filename = (
            "data/response_audio.mp3"
        )


        engine.save_to_file(
            text,
            filename
        )

        engine.runAndWait()


        return filename


    except Exception:

        return None


# =========================================================
# AUDIO PLAYER
# =========================================================

def audio_player(file_path):

    if not file_path:

        return


    if not os.path.exists(
        file_path
    ):

        return


    with open(
        file_path,
        "rb"
    ) as audio_file:

        audio_bytes = (
            audio_file.read()
        )


    audio_base64 = base64.b64encode(
        audio_bytes
    ).decode()


    audio_html = f"""
    <audio controls>
        <source
            src="data:audio/mpeg;base64,
            {audio_base64}"
            type="audio/mpeg"
        >
    </audio>
    """


    st.markdown(
        audio_html,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=75
    )


    st.title(
        "AI Chatbot"
    )


    st.caption(
        "Version 4.0"
    )


    st.write("---")


    # =====================================================
    # QUICK CONTROLS
    # =====================================================

    st.markdown(
        "### 🎛️ Quick Controls"
    )


    st.session_state.ai_mode = st.selectbox(
        "AI Mode",
        AI_MODES,
        index=AI_MODES.index(
            st.session_state.ai_mode
        )
    )


    st.session_state.selected_language = (
        st.selectbox(
            "🌐 Language",
            SUPPORTED_LANGUAGES,
            index=SUPPORTED_LANGUAGES.index(
                st.session_state.selected_language
            )
        )
    )


    st.write("---")


    # =====================================================
    # MENU
    # =====================================================

    st.markdown(
        "### 📋 Menu"
    )


    if st.button(
        "🏠 Home",
        use_container_width=True
    ):

        st.session_state.page = "Home"

        st.rerun()


    if st.button(
        "💬 New Chat",
        use_container_width=True
    ):

        clear_chat()

        st.session_state.page = "New Chat"

        st.rerun()


    if st.button(
        "📜 Chat History",
        use_container_width=True
    ):

        st.session_state.page = "History"

        st.rerun()


    if st.button(
        "📊 Analytics",
        use_container_width=True
    ):

        st.session_state.page = "Analytics"

        st.rerun()


    if st.button(
        "📄 Documents",
        use_container_width=True
    ):

        st.session_state.page = "Documents"

        st.rerun()


    if st.button(
        "⚙️ Settings",
        use_container_width=True
    ):

        st.session_state.page = "Settings"

        st.rerun()


    if st.button(
        "ℹ️ About",
        use_container_width=True
    ):

        st.session_state.page = "About"

        st.rerun()


    st.write("---")


    # =====================================================
    # STATUS
    # =====================================================

    st.success(
        "🟢 Online"
    )


    st.caption(
        "Groq + GPT-OSS 20B"
    )


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
        ">
            Your Smart AI Assistant
        </p>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # METRICS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "💬 Questions",
            st.session_state.total_questions
        )


    with c2:

        st.metric(
            "📚 Dataset",
            f"{len(dataset)}+"
        )


    with c3:

        st.metric(
            "🤖 Model",
            "GPT-OSS 20B"
        )


    with c4:

        st.metric(
            "⚡ Status",
            "Online"
        )


    st.write("")


    # =====================================================
    # MODE CARD
    # =====================================================

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(
                135deg,
                #DBEAFE,
                #EEF2FF
            );
            padding:22px;
            border-radius:20px;
            border:1px solid #BFDBFE;
            margin-bottom:20px;
        ">

        <h2 style="
            margin:0;
            color:#1E3A8A;
        ">
            👋 Welcome to AI Chatbot 4.0
        </h2>

        <p style="
            color:#475569;
            font-size:16px;
        ">
            Mode: <b>{st.session_state.ai_mode}</b>
            &nbsp; | &nbsp;
            Language: <b>{st.session_state.selected_language}</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # CHAT
    # =====================================================

    st.subheader(
        "💬 Conversation"
    )


    for index, message in enumerate(
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


            if message["role"] == "assistant":

                col1, col2, col3 = (
                    st.columns(
                        [1, 1, 1]
                    )
                )


                with col1:

                    if st.button(
                        "👍",
                        key=f"home_like_{index}"
                    ):

                        save_feedback(
                            message.get(
                                "question",
                                ""
                            ),
                            message["content"],
                            "positive"
                        )


                        st.session_state.feedback.append(
                            "positive"
                        )


                        st.success(
                            "Thanks!"
                        )


                with col2:

                    if st.button(
                        "👎",
                        key=f"home_dislike_{index}"
                    ):

                        save_feedback(
                            message.get(
                                "question",
                                ""
                            ),
                            message["content"],
                            "negative"
                        )


                        st.session_state.feedback.append(
                            "negative"
                        )


                        st.info(
                            "Feedback received."
                        )


                with col3:

                    if st.button(
                        "🔊",
                        key=f"home_speak_{index}"
                    ):

                        if TTS_AVAILABLE:

                            text = message[
                                "content"
                            ]


                            if "\n\n---\n" in text:

                                text = text.split(
                                    "\n\n---\n"
                                )[0]


                            audio_file = (
                                generate_speech(
                                    text
                                )
                            )


                            if audio_file:

                                audio_player(
                                    audio_file
                                )

                        else:

                            st.warning(
                                "Install pyttsx3 "
                                "for TTS."
                            )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    if st.session_state.last_suggestions:

        st.markdown(
            "### 💡 Suggested Questions"
        )


        suggestion_cols = st.columns(3)


        for i, suggestion in enumerate(
            st.session_state.last_suggestions
        ):

            with suggestion_cols[i]:

                if st.button(
                    suggestion,
                    key=f"home_suggestion_{i}",
                    use_container_width=True
                ):

                    process_question(
                        suggestion
                    )

                    st.rerun()


    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Ask Anything...",
        key="home_input"
    )


    if prompt:

        process_question(
            prompt
        )

        st.rerun()


# =========================================================
# NEW CHAT
# =========================================================

elif st.session_state.page == "New Chat":

    st.title(
        "💬 New Chat"
    )


    st.caption(
        "Start a new conversation"
    )


    st.divider()


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div style="
                background:#EFF6FF;
                padding:25px;
                border-radius:18px;
                text-align:center;
            ">

            <div style="font-size:45px;">
                🐍
            </div>

            <h3>
                Python
            </h3>

            <p>
                Learn programming
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div style="
                background:#EEF2FF;
                padding:25px;
                border-radius:18px;
                text-align:center;
            ">

            <div style="font-size:45px;">
                🤖
            </div>

            <h3>
                Artificial Intelligence
            </h3>

            <p>
                Explore AI
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div style="
                background:#F0FDF4;
                padding:25px;
                border-radius:18px;
                text-align:center;
            ">

            <div style="font-size:45px;">
                📊
            </div>

            <h3>
                Machine Learning
            </h3>

            <p>
                Understand ML
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # =====================================================
    # QUICK PROMPTS
    # =====================================================

    st.subheader(
        "🚀 Quick Start"
    )


    quick_questions = [
        "What is Python?",
        "What is Machine Learning?",
        "Explain Artificial Intelligence",
        "What is an Operating System?",
        "Explain RAD model",
        "What is NLP?"
    ]


    quick_cols = st.columns(3)


    for i, question in enumerate(
        quick_questions
    ):

        with quick_cols[
            i % 3
        ]:

            if st.button(
                question,
                key=f"quick_{i}",
                use_container_width=True
            ):

                process_question(
                    question
                )

                st.session_state.page = (
                    "New Chat"
                )

                st.rerun()


    st.write("")


    # =====================================================
    # EXISTING CHAT
    # =====================================================

    for index, message in enumerate(
        st.session_state.messages
    ):

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    prompt = st.chat_input(
        "Ask Anything...",
        key="new_chat_input"
    )


    if prompt:

        process_question(
            prompt
        )

        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

elif st.session_state.page == "History":

    st.title(
        "📜 Chat History"
    )


    st.caption(
        "Search, review and export your conversation"
    )


    st.divider()


    if not st.session_state.messages:

        st.info(
            "No chat history found."
        )


    else:

        # =================================================
        # SEARCH
        # =================================================

        search_query = st.text_input(
            "🔍 Search conversation",
            placeholder="Search for a question or answer..."
        )


        # =================================================
        # EXPORT + CLEAR
        # =================================================

        col1, col2 = st.columns(2)


        with col1:

            st.download_button(
                "📥 Export Chat",
                create_chat_text(),
                file_name="ai_chatbot_history.txt",
                mime="text/plain",
                use_container_width=True
            )


        with col2:

            if st.button(
                "🧹 Clear Chat",
                use_container_width=True
            ):

                clear_chat()

                st.rerun()


        st.write("")


        results = search_chat_history(
            search_query
        )


        st.write(
            f"Found {len(results)} messages"
        )


        for message in results:

            if message["role"] == "user":

                st.markdown(
                    f"""
                    <div style="
                        background:#DBEAFE;
                        padding:15px;
                        border-radius:15px;
                        margin-bottom:10px;
                    ">

                    <b>👤 You</b>

                    <br><br>

                    {message["content"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:

                st.markdown(
                    f"""
                    <div style="
                        background:#FFFFFF;
                        padding:15px;
                        border-radius:15px;
                        margin-bottom:15px;
                        border:1px solid #E2E8F0;
                    ">

                    <b>🤖 AI Assistant</b>

                    <br><br>

                    {message["content"]}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# ANALYTICS
# =========================================================

elif st.session_state.page == "Analytics":

    st.title(
        "📊 Analytics Dashboard"
    )


    st.caption(
        "Chatbot performance and usage statistics"
    )


    st.divider()


    total = (
        st.session_state.total_questions
    )


    dataset_count = (
        st.session_state.dataset_answers
    )


    groq_count = (
        st.session_state.groq_answers
    )


    positive = (
        st.session_state.feedback.count(
            "positive"
        )
    )


    negative = (
        st.session_state.feedback.count(
            "negative"
        )
    )


    if st.session_state.response_times:

        average_time = (
            sum(
                st.session_state.response_times
            )
            /
            len(
                st.session_state.response_times
            )
        )

    else:

        average_time = 0


    # =====================================================
    # METRICS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "💬 Questions",
            total
        )


    with c2:

        st.metric(
            "📚 Dataset",
            dataset_count
        )


    with c3:

        st.metric(
            "☁️ Groq",
            groq_count
        )


    with c4:

        st.metric(
            "⏱️ Avg Time",
            f"{average_time:.2f}s"
        )


    st.write("")


    # =====================================================
    # SOURCE ANALYTICS
    # =====================================================

    st.subheader(
        "🔀 Answer Sources"
    )


    source_data = {

        "Source": [
            "Dataset",
            "Groq AI"
        ],

        "Answers": [
            dataset_count,
            groq_count
        ]
    }


    st.bar_chart(
        source_data,
        x="Source",
        y="Answers"
    )


    # =====================================================
    # FEEDBACK
    # =====================================================

    st.subheader(
        "👍👎 User Feedback"
    )


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "👍 Positive",
            positive
        )


    with c2:

        st.metric(
            "👎 Negative",
            negative
        )


    # =====================================================
    # PERFORMANCE
    # =====================================================

    st.subheader(
        "⚡ Response Performance"
    )


    if st.session_state.response_times:

        performance = {

            "Response": [
                f"#{i + 1}"
                for i in range(
                    len(
                        st.session_state.response_times
                    )
                )
            ],

            "Seconds": [
                round(
                    value,
                    2
                )

                for value in
                st.session_state.response_times
            ]
        }


        st.line_chart(
            performance,
            x="Response",
            y="Seconds"
        )


    else:

        st.info(
            "No performance data yet."
        )


# =========================================================
# DOCUMENTS
# =========================================================

elif st.session_state.page == "Documents":

    st.title(
        "📄 Document Assistant"
    )


    st.caption(
        "Upload a PDF or TXT file and ask questions about it"
    )


    st.divider()


    uploaded_file = st.file_uploader(
        "Upload document",
        type=[
            "pdf",
            "txt"
        ]
    )


    if uploaded_file:

        if (
            uploaded_file.name
            != st.session_state.document_name
        ):

            text, name = (
                read_uploaded_document(
                    uploaded_file
                )
            )


            if text:

                st.session_state.document_text = (
                    text
                )

                st.session_state.document_name = (
                    name
                )


                st.success(
                    f"✅ {name} loaded successfully."
                )


            else:

                if (
                    name.lower().endswith(
                        ".pdf"
                    )
                    and not PDF_AVAILABLE
                ):

                    st.warning(
                        "Install pypdf to read PDFs."
                    )

                else:

                    st.error(
                        "Could not read the document."
                    )


    if st.session_state.document_text:

        st.info(
            f"📄 Active document: "
            f"{st.session_state.document_name}"
        )


        with st.expander(
            "👁️ Preview Document"
        ):

            st.text(
                st.session_state.document_text[
                    :5000
                ]
            )


        st.subheader(
            "💬 Ask About Document"
        )


        document_question = st.chat_input(
            "Ask something about the document...",
            key="document_question"
        )


        if document_question:

            process_question(
                document_question,
                force_groq=True
            )

            st.rerun()


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.title(
        "⚙️ Settings"
    )


    st.divider()


    # =====================================================
    # AI SETTINGS
    # =====================================================

    st.subheader(
        "🤖 AI Configuration"
    )


    st.info(
        "Model: GPT-OSS 20B"
    )


    st.info(
        "Provider: Groq Cloud"
    )


    st.info(
        f"Dataset Threshold: "
        f"{DATASET_THRESHOLD}"
    )


    # =====================================================
    # LANGUAGE
    # =====================================================

    st.subheader(
        "🌐 Language"
    )


    st.session_state.selected_language = (
        st.selectbox(
            "Default response language",
            SUPPORTED_LANGUAGES,
            index=SUPPORTED_LANGUAGES.index(
                st.session_state.selected_language
            )
        )
    )


    # =====================================================
    # AI MODE
    # =====================================================

    st.subheader(
        "🧠 AI Mode"
    )


    st.session_state.ai_mode = st.selectbox(
        "Default AI mode",
        AI_MODES,
        index=AI_MODES.index(
            st.session_state.ai_mode
        )
    )


    # =====================================================
    # TTS
    # =====================================================

    st.subheader(
        "🔊 Text-to-Speech"
    )


    if TTS_AVAILABLE:

        st.session_state.tts_enabled = (
            st.checkbox(
                "Enable text-to-speech",
                value=st.session_state.tts_enabled
            )
        )

    else:

        st.warning(
            "pyttsx3 is not installed."
        )


    # =====================================================
    # VOICE
    # =====================================================

    st.subheader(
        "🎙️ Voice Input"
    )


    if SPEECH_AVAILABLE:

        st.session_state.voice_enabled = (
            st.checkbox(
                "Enable voice input",
                value=st.session_state.voice_enabled
            )
        )

    else:

        st.warning(
            "SpeechRecognition is not installed."
        )


    # =====================================================
    # FEATURES
    # =====================================================

    st.subheader(
        "✨ Active Features"
    )


    feature_list = [

        "✅ TF-IDF Search",

        "✅ Cosine Similarity",

        "✅ Groq AI",

        "✅ Conversation Memory",

        "✅ Suggested Questions",

        "✅ Feedback",

        "✅ Response-Time Tracking",

        "✅ Chat Export",

        "✅ Chat Search",

        "✅ Analytics",

        "✅ Multiple AI Modes",

        "✅ English / Hindi / Marathi",

        "✅ PDF / TXT Assistant",

        "✅ Text-to-Speech",

        "✅ Professional UI"
    ]


    for feature in feature_list:

        st.write(
            feature
        )


# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "About":

    st.title(
        "ℹ️ About"
    )


    st.divider()


    with st.container(
        border=True
    ):

        st.subheader(
            "🤖 AI Chatbot 4.0"
        )


        st.write(
            """
AI Chatbot 4.0 is a hybrid AI chatbot
that combines traditional NLP-based
question answering with Generative AI.
"""
        )


        st.subheader(
            "🛠️ Technologies"
        )


        technologies = [

            "🐍 Python",

            "🎨 Streamlit",

            "🧠 NLP",

            "📊 TF-IDF",

            "📐 Cosine Similarity",

            "🔬 Scikit-learn",

            "☁️ Groq API",

            "🤖 GPT-OSS 20B"
        ]


        for item in technologies:

            st.write(
                item
            )


        st.subheader(
            "⚙️ System Workflow"
        )


        st.write(
            """
1. User enters a question.

2. TF-IDF converts the question into
   numerical representation.

3. Cosine Similarity compares the question
   with the trained dataset.

4. If similarity is at least 0.90,
   the dataset answer is returned.

5. Otherwise, Groq GPT-OSS 20B generates
   the response.

6. Conversation memory provides context
   from recent messages.

7. Suggested questions are generated.

8. Feedback and performance data are recorded.
"""
        )


        st.subheader(
            "✨ Major Features"
        )


        st.write(
            """
• Hybrid NLP + Generative AI

• Conversation Memory

• Multiple AI Modes

• Multilingual Responses

• PDF/TXT Document Assistant

• Suggested Questions

• Feedback System

• Chat Search

• Chat Export

• Analytics Dashboard

• Text-to-Speech

• Professional Streamlit UI
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
        "4.0"
    )


st.markdown(
    """
    <div class="footer">

        © 2026 AI Chatbot 4.0 |
        Built with Python + Streamlit +
        NLP + Groq AI

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

    /* ==================================================
       MAIN APP
       ================================================== */

    .stApp {

        background:
        linear-gradient(
            135deg,
            #EFF6FF 0%,
            #F8FAFC 50%,
            #EEF2FF 100%
        );

    }


    /* ==================================================
       SIDEBAR
       ================================================== */

    section[data-testid="stSidebar"] {

        background:
        linear-gradient(
            180deg,
            #172554 0%,
            #1E3A8A 50%,
            #2563EB 100%
        );

    }


    section[data-testid="stSidebar"] * {

        color:white !important;

    }


    /* ==================================================
       HEADINGS
       ================================================== */

    h1 {

        font-weight:800 !important;

    }


    h2 {

        color:#1E3A8A !important;

    }


    h3 {

        color:#1E40AF !important;

    }


    /* ==================================================
       METRIC CARDS
       ================================================== */

    div[data-testid="metric-container"] {

        background:
        rgba(
            255,
            255,
            255,
            0.92
        );

        border:
        1px solid #DBEAFE;

        border-radius:18px;

        padding:18px;

        box-shadow:
        0 4px 15px
        rgba(
            30,
            64,
            175,
            0.08
        );

        transition:
        0.3s;

    }


    div[data-testid="metric-container"]:hover {

        transform:
        translateY(-3px);

        box-shadow:
        0 8px 25px
        rgba(
            30,
            64,
            175,
            0.15
        );

    }


    div[data-testid="stMetricValue"] {

        color:#1E3A8A;

        font-weight:800;

    }


    /* ==================================================
       BUTTONS
       ================================================== */

    .stButton > button {

        background:
        linear-gradient(
            90deg,
            #2563EB,
            #4F46E5
        );

        color:white !important;

        border:none;

        border-radius:12px;

        min-height:45px;

        font-weight:600;

        transition:0.3s;

    }


    .stButton > button:hover {

        transform:
        translateY(-2px);

        box-shadow:
        0 5px 15px
        rgba(
            37,
            99,
            235,
            0.30
        );

    }


    /* ==================================================
       CHAT
       ================================================== */

    [data-testid="stChatMessage"] {

        background:
        rgba(
            255,
            255,
            255,
            0.85
        );

        border-radius:16px;

        padding:12px;

        margin-bottom:10px;

        border:
        1px solid #E0E7FF;

    }


    /* ==================================================
       CHAT INPUT
       ================================================== */

    [data-testid="stChatInput"] {

        background:white;

        border-radius:18px;

        border:
        2px solid #BFDBFE;

        box-shadow:
        0 5px 20px
        rgba(
            37,
            99,
            235,
            0.10
        );

    }


    [data-testid="stChatInput"]:focus-within {

        border-color:#2563EB;

        box-shadow:
        0 0 0 3px
        rgba(
            37,
            99,
            235,
            0.12
        );

    }


    /* ==================================================
       INPUTS
       ================================================== */

    input,
    textarea {

        border-radius:12px !important;

    }


    /* ==================================================
       ALERTS
       ================================================== */

    div[data-testid="stAlert"] {

        border-radius:14px;

    }


    /* ==================================================
       DIVIDERS
       ================================================== */

    hr {

        border-color:#DBEAFE;

    }


    /* ==================================================
       FOOTER
       ================================================== */

    .footer {

        text-align:center;

        padding:20px;

        color:#64748B;

        font-size:14px;

    }


    /* ==================================================
       SCROLLBAR
       ================================================== */

    ::-webkit-scrollbar {

        width:8px;

    }


    ::-webkit-scrollbar-track {

        background:#EFF6FF;

    }


    ::-webkit-scrollbar-thumb {

        background:#93C5FD;

        border-radius:10px;

    }


    ::-webkit-scrollbar-thumb:hover {

        background:#2563EB;

    }

    </style>
    """,
    unsafe_allow_html=True
)
