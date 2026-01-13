import os
import pandas as pd

# Base folders
BASE_DIR = os.getcwd()
TEXT_DIR = os.path.join(BASE_DIR, "extracted_texts")
STOPWORDS_DIR = os.path.join(BASE_DIR, "stopwords")
MASTER_DIR = os.path.join(BASE_DIR, "master_dict")


def load_wordlist(path):
    words = set()
    with open(path, "r", encoding="latin-1", errors="ignore") as f:
        for line in f:
            w = line.strip()
            if not w:
                continue
            #
            if w.startswith(";"):
                continue
            words.add(w.lower())
    return words


#  Stopwords load
stopwords = set()
for fname in os.listdir(STOPWORDS_DIR):
    fpath = os.path.join(STOPWORDS_DIR, fname)
    stopwords.update(load_wordlist(fpath))

print("Stopwords loaded:", len(stopwords))

#  Positive / negative words load
positive_words = load_wordlist(os.path.join(MASTER_DIR, "positive-words.txt"))
negative_words = load_wordlist(os.path.join(MASTER_DIR, "negative-words.txt"))

print("Positive words loaded:", len(positive_words))
print("Negative words loaded:", len(negative_words))

#  text file analyse
results = []

for fname in os.listdir(TEXT_DIR):
    if not fname.endswith(".txt"):
        continue

    fpath = os.path.join(TEXT_DIR, fname)
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().lower()

    words = text.split()
    clean_words = [w for w in words if w not in stopwords]

    pos_count = sum(1 for w in clean_words if w in positive_words)
    neg_count = sum(1 for w in clean_words if w in negative_words)

    results.append([fname, pos_count, neg_count, len(clean_words)])

#  Result save in Excel
df = pd.DataFrame(
    results,
    columns=["File Name", "Positive Score", "Negative Score", "Clean Word Count"]
)

out_path = os.path.join(BASE_DIR, "final_output.xlsx")
df.to_excel(out_path, index=False)

print("Final Output Excel Generated at:", out_path)