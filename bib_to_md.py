import re
import os

# 설정
BIB_FILE = "./_publications/papers.bib"
OUT_DIR = "_publications"
MY_NAME = ["Yujin Choi", "Choi, Yujin"] # 본인 이름의 다양한 표기법

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def bold_name(author_str):
    for name in MY_NAME:
        # 대소문자 구분 없이 본인 이름을 찾아 볼드 처리
        author_str = re.sub(name, f"**{name}**", author_str, flags=re.IGNORECASE)
    return author_str

def generate_md():
    with open(BIB_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 논문 엔트리 단위로 분리
    entries = re.findall(r'@(\w+)\{(.*?),', content)
    blocks = re.split(r'@\w+\{', content)[1:]

    for i, block in enumerate(blocks):
        key = entries[i][1]
        title = re.search(r'title\s*=\s*\{(.*?)\}', block, re.S).group(1).strip().replace('{', '').replace('}', '')
        authors = re.search(r'author\s*=\s*\{(.*?)\}', block, re.S).group(1).strip().replace('\n', ' ')
        year = re.search(r'year\s*=\s*\{(.*?)\}', block).group(1)
        
        # 저널 또는 학술대회 이름 추출
        venue_match = re.search(r'journal\s*=\s*\{(.*?)\}', block, re.S) or \
                      re.search(r'booktitle\s*=\s*\{(.*?)\}', block, re.S)
        venue = venue_match.group(1).strip().replace('{', '').replace('}', '') if venue_match else "arXiv"
        
        # 이름 볼드 처리
        authors_bold = bold_name(authors)
        
        # 파일명 및 내용 생성
        filename = f"{year}-01-01-{key}.md"
        md_content = f"""---
title: "{title}"
collection: publications
permalink: /publication/{year}-{key}
date: {year}-01-01
venue: '{venue}'
citation: '{authors_bold}. ({year}). "{title}." *{venue}*.'
---
"""
        with open(os.path.join(OUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_md()