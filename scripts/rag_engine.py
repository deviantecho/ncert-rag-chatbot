import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import json
import faiss
import warnings
import numpy as np
import streamlit as st

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai


warnings.filterwarnings("ignore")

load_dotenv()


@st.cache_resource
def load_resources():

    print(
        "\nLoading AI resources..."
    )

    client = genai.Client(
        api_key=os.getenv(
            "GEMINI_API_KEY"
        )
    )

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    index = faiss.read_index(
        "data/faiss_index.bin"
    )

    with open(
        "data/chunk_metadata.json",
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    print(
        "Resources loaded successfully!"
    )

    return (
        client,
        embedding_model,
        index,
        chunks
    )


client, embedding_model, index, chunks = (
    load_resources()
)


def ask_question(
    question,
    chat_history
):

    history_text = ""

    for message in chat_history[-6:]:

        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    search_query = question

    # ------------------------------------
    # Rewrite follow-up questions
    # ------------------------------------

    if len(chat_history) > 0:

        rewrite_prompt = f"""
Previous Conversation:

{history_text}

Current Question:

{question}

Rewrite the current question into a complete standalone question.

Only return the rewritten question.
"""

        try:

            rewrite_response = (
                client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=rewrite_prompt
                )
            )

            search_query = (
                rewrite_response.text.strip()
            )

        except Exception:

            search_query = question

    # ------------------------------------
    # Create embedding
    # ------------------------------------

    question_embedding = (
        embedding_model.encode(
            search_query
        )
    )

    question_embedding = np.array(
        [question_embedding],
        dtype="float32"
    )

    # ------------------------------------
    # Retrieve chunks
    # ------------------------------------

    k = 5

    distances, indices = index.search(
        question_embedding,
        k
    )

    # ------------------------------------
    # Relevance filter
    # ------------------------------------

    if distances[0][0] > 1.3:

        return (
            "I could not find this information in the NCERT data.",
            [],
            chat_history
        )

    context = ""
    sources = []

    for i in range(k):

        chunk = chunks[
            indices[0][i]
        ]

        sources.append(
            f"{chunk['subject']} > "
            f"{chunk['chapter_file']} > "
            f"{chunk['section']}"
        )

        context += f"""
Subject: {chunk['subject']}
Chapter: {chunk['chapter_file']}
Section: {chunk['section']}

{chunk['text']}

--------------------------------
"""

    # ------------------------------------
    # Build prompt
    # ------------------------------------

    prompt = f"""
You are an NCERT Class 10 tutor.

Previous Conversation:

{history_text}

Context:

{context}

Current Question:

{question}

Instructions:

1. Answer ONLY using the provided NCERT context.
2. Do not use outside knowledge.
3. If the answer is not present, say:
   'I could not find this information in the NCERT data.'
4. Explain in a Class 10 friendly manner.
5. Use bullet points when useful.
6. Keep the answer concise and accurate.
"""

    # ------------------------------------
    # Generate answer
    # ------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

    except Exception as e:

        answer = (
            f"Gemini API Error:\n\n{e}"
        )

    # ------------------------------------
    # Save conversation
    # ------------------------------------

    chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    unique_sources = list(
        dict.fromkeys(sources)
    )

    return (
        answer,
        unique_sources,
        chat_history
    )