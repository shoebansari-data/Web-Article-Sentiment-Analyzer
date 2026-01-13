import pandas as pd
import os

# Current project folder
BASE_DIR = os.getcwd()

# Input file correct path
input_path = os.path.join(BASE_DIR, "Input", "Input.xlsx")

print("Looking for file at:", input_path)

# Check if file exists
if not os.path.exists(input_path):
    print("❌ File NOT found. Check folder & file name.")
    exit()

# Read excel file
df = pd.read_excel(input_path)

# Show first 5 rows
print("\n✅ File Successfully Read. First 5 rows:\n")
print(df.head())
import requests
from bs4 import BeautifulSoup

# Output folder ensure 
out_dir = os.path.join(BASE_DIR, "extracted_texts")
os.makedirs(out_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("\n--- Starting scraping for each URL ---")

# Extract data from URL
for _, row in df.iterrows():
    url_id = str(row["URL_ID"])
    url = row["URL"]

    print(f"\nFetching: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        # Title
        title_tag = soup.find("h1") or soup.title
        title_text = title_tag.get_text(strip=True) if title_tag else ""

        # Paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        article_text = "\n".join(paragraphs)

        full_text = title_text + "\n\n" + article_text

        # .txt file path
        out_path = os.path.join(out_dir, f"{url_id}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print("✅ Saved:", out_path)

    except Exception as e:
        print("❌ Error with URL", url, ":", e)