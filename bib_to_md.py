import re
import os

BIB_FILE = "./_publications/papers.bib"
OUT_DIR = "_publications"
MY_NAME = ["Yujin Choi", "Choi, Yujin"] # 본인 이름 볼드 처리를 위함

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def bold_name(author_str):
    for name in MY_NAME:
        author_str = re.sub(name, f"**{name}**", author_str, flags=re.IGNORECASE)
    return author_str

def generate_md():
    with open(BIB_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # @type{key, 구조 파싱
    entries = re.findall(r'@(\w+)\{(.*?),', content)
    blocks = re.split(r'@\w+\{', content)[1:]

    for i, block in enumerate(blocks):
        entry_type = entries[i][0].lower() # article or inproceedings
        key = entries[i][1]
        
        title = re.search(r'title\s*=\s*\{(.*?)\}', block, re.S).group(1).strip().replace('{', '').replace('}', '')
        authors = re.search(r'author\s*=\s*\{(.*?)\}', block, re.S).group(1).strip().replace('\n', ' ')
        year = re.search(r'year\s*=\s*\{(.*?)\}', block).group(1)
        
        venue_match = re.search(r'journal\s*=\s*\{(.*?)\}', block, re.S) or \
                      re.search(r'booktitle\s*=\s*\{(.*?)\}', block, re.S)
        venue = venue_match.group(1).strip().replace('{', '').replace('}', '') if venue_match else "Unknown"

        # --- 카테고리 판별 로직 ---
        if entry_type == "inproceedings":
            category = "conferences"
        elif "arxiv" in venue.lower() or entry_type == "unpublished":
            category = "preprints"
        else:
            category = "manuscripts"
        # -----------------------

        authors_bold = bold_name(authors)
        filename = f"{year}-01-01-{key}.md"
        
        md_content = f"""---
title: "{title}"
collection: publications
permalink: /publication/{year}-{key}
date: {year}-01-01
venue: '{venue}'
category: {category}
citation: '{authors_bold}. ({year}). "{title}." *{venue}*.'
---

 PhD Dissertation research and Trustworthy AI publications.
"""
        with open(os.path.join(OUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Generated ({category}): {filename}")

if __name__ == "__main__":
    generate_md()