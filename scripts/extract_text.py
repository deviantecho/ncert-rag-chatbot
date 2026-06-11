import fitz
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    pdf = fitz.open(pdf_path)

    text = ""

    for page in pdf:
        text += page.get_text()

    return text


pdf_root = Path("data/pdfs")
output_root = Path("data/text")

for subject_folder in pdf_root.iterdir():

    if not subject_folder.is_dir():
        continue

    subject_output = output_root / subject_folder.name
    subject_output.mkdir(parents=True, exist_ok=True)

    for pdf_file in subject_folder.glob("*.pdf"):

        print(f"Processing: {pdf_file.name}")

        text = extract_text_from_pdf(pdf_file)

        output_file = (
            subject_output /
            f"{pdf_file.stem}.txt"
        )

        output_file.write_text(
            text,
            encoding="utf-8"
        )

print("All PDFs processed.")