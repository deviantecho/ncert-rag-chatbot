# NCERT RAG Chatbot

A Conversational Retrieval-Augmented Generation (RAG) chatbot built using FAISS, Sentence Transformers, and Google's Gemini API.

The chatbot answers questions from NCERT Class 10 Science and Mathematics textbooks by retrieving relevant textbook content and generating grounded responses using Gemini.

---

## Features

* PDF text extraction pipeline
* Text cleaning and preprocessing
* Section-aware chunking
* Semantic embeddings using Sentence Transformers
* FAISS vector database for efficient retrieval
* Gemini-powered answer generation
* Source citation support
* Multi-turn conversation memory
* History-aware query rewriting

---

## Tech Stack

### AI & NLP

* Sentence Transformers (all-MiniLM-L6-v2)
* Google Gemini 2.5 Flash

### Vector Search

* FAISS

### Backend

* Python

### Data Processing

* JSON
* Regular Expressions

---

## Project Pipeline

NCERT PDFs

↓

Text Extraction

↓

Text Cleaning

↓

Section-Based Chunking

↓

Embedding Generation

↓

FAISS Indexing

↓

Semantic Retrieval

↓

Gemini Response Generation

↓

Final Answer + Sources

---

## Dataset

Currently supports:

* NCERT Class 10 Mathematics
* NCERT Class 10 Science

---

## Example

### Question

What is a balanced chemical equation?

### Answer

A chemical equation is balanced if the number of atoms of each element is the same on both sides of the equation. This ensures that the law of conservation of mass is satisfied.

### Sources

* Science > Chapter 1 > Balanced Chemical Equations

---

## Repository Structure

```text
data/
├── pdfs/
├── text/
├── clean_text/
├── chunks/
├── embeddings/

scripts/
├── extract_text.py
├── clean_text.py
├── chunk_text.py
├── generate_embeddings.py
├── build_faiss_index.py
├── chatbot.py

main.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/deviantecho/ncert-rag-chatbot.git
cd ncert-rag-chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the chatbot:

```bash
python scripts/chatbot.py
```

---

## Future Improvements

* Streamlit web interface
* Better retrieval ranking
* Support for more NCERT subjects
* Hybrid search (keyword + vector)
* Citation highlighting
* Deployment on cloud infrastructure

---

## Author

Devesh Kumar Singh

Computer Science Engineering Student

Interested in AI, Software Development, and Applied Machine Learning.
