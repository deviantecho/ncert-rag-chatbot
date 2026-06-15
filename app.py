import streamlit as st

from scripts.rag_engine import ask_question


st.set_page_config(
    page_title="NCERT AI Tutor",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
<style>

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

[data-testid="stSidebar"]{
    border-right:1px solid rgba(255,255,255,0.08);
}

.hero-container{
    padding:30px;
    border-radius:22px;
    background:linear-gradient(
        135deg,
        #111827,
        #1f2937
    );
    border:1px solid rgba(255,255,255,0.08);
    margin-bottom:25px;
}

.hero-title{
    font-size:3rem;
    font-weight:700;
    margin-bottom:8px;
}

.hero-subtitle{
    color:#9ca3af;
    font-size:1.1rem;
}

.source-card{
    padding:14px;
    border-radius:14px;
    background:#111827;
    border:1px solid rgba(255,255,255,0.08);
    margin-bottom:10px;
}

.retrieval-card{
    padding:14px;
    border-radius:14px;
    background:#0f172a;
    border:1px solid rgba(255,255,255,0.08);
    margin-bottom:10px;
}

.footer{
    text-align:center;
    color:#9ca3af;
    padding-top:20px;
    padding-bottom:10px;
}

</style>
""",
    unsafe_allow_html=True
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "prefill_question" not in st.session_state:
    st.session_state.prefill_question = None

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("📚 NCERT AI Tutor")

    st.caption(
        "AI-powered NCERT learning assistant"
    )

    st.divider()

    st.subheader("📊 Knowledge Base")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Subjects",
            "2"
        )

    with col2:
        st.metric(
            "Chunks",
            "465"
        )

    st.metric(
        "Chapters",
        "27"
    )

    st.divider()

    subject_filter = st.radio(
        "📚 Subject",
        [
            "All Subjects",
            "Science",
            "Mathematics"
        ]
    )

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    st.caption("Version 1.2")

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    """
<div class="hero-container">

<div class="hero-title">
📚 NCERT AI Tutor
</div>

<div class="hero-subtitle">
Learn Science and Mathematics using Retrieval-Augmented Generation (RAG), FAISS, Sentence Transformers and Gemini.
</div>

</div>
""",
    unsafe_allow_html=True
)

# --------------------------------------------------
# STATS ROW
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Subjects",
        "2"
    )

with c2:
    st.metric(
        "Chapters",
        "27"
    )

with c3:
    st.metric(
        "Knowledge Chunks",
        "465"
    )

with c4:
    st.metric(
        "LLM",
        "Gemini"
    )

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        """
<h2 style="text-align:center;">
What would you like to learn today?
</h2>
""",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🧪 Explain Chemical Reactions",
            use_container_width=True
        ):
            st.session_state.prefill_question = (
                "Explain chemical reactions."
            )
            st.rerun()

        if st.button(
            "🔬 Explain Human Reproduction",
            use_container_width=True
        ):
            st.session_state.prefill_question = (
                "Explain human reproduction."
            )
            st.rerun()

    with col2:

        if st.button(
            "➗ Fundamental Theorem of Arithmetic",
            use_container_width=True
        ):
            st.session_state.prefill_question = (
                "State the Fundamental Theorem of Arithmetic."
            )
            st.rerun()

        if st.button(
            "🧲 Magnetic Effects of Electric Current",
            use_container_width=True
        ):
            st.session_state.prefill_question = (
                "Explain magnetic effects of electric current."
            )
            st.rerun()

# --------------------------------------------------
# DISPLAY CHAT
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# --------------------------------------------------
# HANDLE SUGGESTIONS
# --------------------------------------------------

question = None

if st.session_state.prefill_question:

    question = (
        st.session_state.prefill_question
    )

    st.session_state.prefill_question = None

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask anything from NCERT..."
)

if user_input:
    question = user_input

# --------------------------------------------------
# RUN QUERY
# --------------------------------------------------

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching NCERT knowledge base..."
        ):

            try:

                (
                    answer,
                    sources,
                    retrieval_details,
                    updated_history
                ) = ask_question(
                    question,
                    st.session_state.chat_history,
                    subject_filter
                )

                st.session_state.chat_history = (
                    updated_history
                )

                st.markdown(answer)

                # ----------------------------------
                # Sources
                # ----------------------------------

                if len(sources) > 0:

                    with st.expander(
                        "📖 Sources"
                    ):

                        for source in sources:

                            st.markdown(
                                f"""
<div class="source-card">
📖 {source}
</div>
""",
                                unsafe_allow_html=True
                            )

                # ----------------------------------
                # Retrieval Details
                # ----------------------------------

                if len(
                    retrieval_details
                ) > 0:

                    with st.expander(
                        "🔍 Retrieval Details"
                    ):

                        for item in (
                            retrieval_details
                        ):

                            score_color = (
                                "#22c55e"
                                if item["score"] >= 80
                                else "#eab308"
                                if item["score"] >= 60
                                else "#ef4444"
                            )

                            st.markdown(
                                f"""
<div class="retrieval-card">

### #{item['rank']}

**Subject:** {item['subject']}

**Chapter:** {item['chapter']}

**Section:** {item['section']}

<p style="
font-size:18px;
font-weight:700;
color:{score_color};
margin-bottom:8px;
">
Relevance Score: {item['score']}%
</p>

Distance: {item['distance']}

</div>
""",
                                unsafe_allow_html=True
                            )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
<div class="footer">
Built with Streamlit • FAISS • Sentence Transformers • Gemini
</div>
""",
    unsafe_allow_html=True
)