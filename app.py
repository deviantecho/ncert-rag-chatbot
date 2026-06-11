import streamlit as st

from scripts.rag_engine import ask_question


st.set_page_config(
    page_title="NCERT RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 NCERT RAG Chatbot")

st.markdown(
    """
Ask questions from **NCERT Class 10 Science and Mathematics**.

Examples:
- What is magnetic field?
- State the Fundamental Theorem of Arithmetic.
- Explain balancing of chemical equations.
"""
)

# Session State

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar

with st.sidebar:

    st.header("Controls")

    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()

# User Input

question = st.text_input(
    "Enter your question:"
)

# Ask Button

if st.button("Ask") and question:

    with st.spinner("Searching NCERT knowledge base..."):

        try:

            answer, sources, updated_history = ask_question(
                question,
                st.session_state.chat_history
            )

            st.session_state.chat_history = (
                updated_history
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

# Display Latest Answer

if len(st.session_state.chat_history) >= 2:

    latest_user = (
        st.session_state.chat_history[-2]["content"]
    )

    latest_answer = (
        st.session_state.chat_history[-1]["content"]
    )

    st.subheader("Question")

    st.info(latest_user)

    st.subheader("Answer")

    st.success(latest_answer)

    if "sources" in locals():

        with st.expander(
            "View Sources"
        ):

            for source in sources:

                st.write(
                    f"• {source}"
                )

# Conversation History

if len(st.session_state.chat_history) > 0:

    st.divider()

    st.subheader("Conversation History")

    for i in range(
        0,
        len(st.session_state.chat_history),
        2
    ):

        try:

            user_msg = (
                st.session_state.chat_history[i]
            )

            assistant_msg = (
                st.session_state.chat_history[i + 1]
            )

            with st.chat_message("user"):

                st.write(
                    user_msg["content"]
                )

            with st.chat_message("assistant"):

                st.write(
                    assistant_msg["content"]
                )

        except:
            pass