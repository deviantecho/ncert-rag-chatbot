from pathlib import Path
import re


input_root = Path("data/text")
output_root = Path("data/clean_text")

output_root.mkdir(exist_ok=True)

def remove_consecutive_duplicates(lines):

    cleaned_lines = []

    previous_line = None

    for line in lines:

        line = line.strip()

        if line == previous_line:
            continue

        cleaned_lines.append(line)

        previous_line = line

    return cleaned_lines


def clean_text(text):

    text = re.sub(r"Reprint\s+\d{4}-\d{2}", "", text)

    text = re.sub(r"\n\s*\n", "\n\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    lines = text.splitlines()

    lines = remove_consecutive_duplicates(lines)

    text = "\n".join(lines)

    return text.strip()


for subject_folder in input_root.iterdir():

    if not subject_folder.is_dir():
        continue

    subject_output = output_root / subject_folder.name
    subject_output.mkdir(exist_ok=True)

    for txt_file in subject_folder.glob("*.txt"):

        text = txt_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        cleaned = clean_text(text)

        output_file = subject_output / txt_file.name

        output_file.write_text(
            cleaned,
            encoding="utf-8"
        )

        print(f"Cleaned: {txt_file.name}")

print("Cleaning complete.")