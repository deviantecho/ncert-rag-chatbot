from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np


model = SentenceTransformer(
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


question = input(
    "\nAsk a question: "
)


question_embedding = model.encode(
    question
)

question_embedding = np.array(
    [question_embedding],
    dtype="float32"
)


k = 3

distances, indices = index.search(
    question_embedding,
    k
)


print("\nTOP RESULTS\n")


for i in range(k):

    chunk = chunks[
        indices[0][i]
    ]

    print("=" * 80)

    print(
        f"Distance: {distances[0][i]:.4f}"
    )

    print(
        f"Subject: {chunk['subject']}"
    )

    print(
        f"Chapter: {chunk['chapter_file']}"
    )

    print(
        f"Section: {chunk['section']}"
    )

    print()

    print(
        chunk["text"][:500]
    )

    print("\n")