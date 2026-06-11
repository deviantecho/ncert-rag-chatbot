from pathlib import Path
import re
import json


input_root = Path("data/clean_text")
output_root = Path("data/chunks")

output_root.mkdir(exist_ok=True)


section_pattern = re.compile(
    r"^\d+\.\d+(\.\d+)?\s+[A-Z]"
)

def split_into_subchunks(text, max_words=400):

    words = text.split()

    chunks = []

    for i in range(0, len(words), max_words):

        chunk = " ".join(
            words[i:i + max_words]
        )

        chunks.append(chunk)

    return chunks

for subject_folder in input_root.iterdir():

    if not subject_folder.is_dir():
        continue

    chunks = []

    for txt_file in subject_folder.glob("*.txt"):

        text = txt_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        lines = text.splitlines()

        current_section = None
        current_text = []

        for line in lines:

            line = line.strip()

            if section_pattern.match(line):

                if current_section:

                    chunk_text = "\n".join(current_text)

                    if len(chunk_text.strip()) >= 50:

                      subchunks = split_into_subchunks(chunk_text)

                      for idx, subchunk in enumerate(subchunks, start=1):

                        chunks.append({
                          "subject": subject_folder.name,
                          "chapter_file": txt_file.stem,
                          "section": current_section,
                          "chunk_id": idx,
                          "text": subchunk
        })

                current_section = line
                current_text = []
            else:
                current_text.append(line)

        if current_section:

            chunk_text = "\n".join(current_text)

            if len(chunk_text.strip()) >= 50:

               subchunks = split_into_subchunks(chunk_text)

               for idx, subchunk in enumerate(subchunks, start=1):

                   chunks.append({
                     "subject": subject_folder.name,
                      "chapter_file": txt_file.stem,
                      "section": current_section,
                      "chunk_id": idx,
                      "text": subchunk
        })
        

    output_file = output_root / f"{subject_folder.name}_chunks.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Created {len(chunks)} chunks for {subject_folder.name}"
    )

print("Chunking complete.")