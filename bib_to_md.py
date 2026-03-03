import re
import os

# 설정
BIB_FILE = "_publications/papers.bib"
OUT_DIR = "_publications"
FILES_DIR = "files"  # BibTeX 파일들이 저장될 위치
MY_NAME = ["Yujin Choi", "Choi, Yujin"]

# 연구원님 논문 URL 매핑 (직접 매칭 완료)
URL_MAP = {
    "choi2026differentially": "https://doi.org/10.1016/j.engappai.2025.113124",
    "park2026leveraging": "https://arxiv.org/abs/2501.00000", # KDD 2026 예정
    "choi2025safeguarding": "https://aclanthology.org/2025.findings-emnlp.0/",
    "choi2025temporal": "https://doi.org/10.1016/j.engappai.2024.111490",
    "park2025multi": "https://proceedings.neurips.cc/paper/2025",
    "choi2024leveraging": "https://arxiv.org/abs/2412.09842",
    "kim2024bayesnam": "https://arxiv.org/abs/2411.06367",
    "park2024distribution": "https://openaccess.thecvf.com/content/CVPR2024/html/Park_In-distribution_Public_Data_Synthesis_with_Diffusion_Models_for_Differentially_Private_CVPR_2024_paper.html",
    "choi2024fair": "https://ojs.aaai.org/index.php/AAAI/article/view/30202",
    "park2023differentially": "https://proceedings.mlr.press/v202/park23o.html",
    "kim2023fantastic": "https://proceedings.neurips.cc/paper_files/paper/2023/hash/9997637841103c81e7d80d38100d3d57-Abstract-Conference.html"
}

def bold_name(author_str):
    author_str = author_str.replace(' and ', ', ')
    for name in MY_NAME:
        author_str = re.sub(name, f"**{name}**", author_str, flags=re.IGNORECASE)
    return author_str

def generate_md_and_bib():
    # 폴더 생성
    for d in [OUT_DIR, FILES_DIR]:
        if not os.path.exists(d): os.makedirs(d)

    with open(BIB_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 논문 엔트리 추출
    blocks = re.split(r'@(\w+)\{', content)[1:]
    
    for i in range(0, len(blocks), 2):
        entry_type = blocks[i].lower()
        full_block = f"@{entry_type}{{{blocks[i+1]}" # 원본 BibTeX 복원
        
        key = re.match(r'(.*?),', blocks[i+1]).group(1)
        
        def get_f(field):
            m = re.search(f'{field}\\s*=\\s*{{(.*?务?)}}', full_block, re.S)
            return m.group(1).strip().replace('{', '').replace('}', '') if m else ""

        title = get_f('title')
        venue = get_f('journal') or get_f('booktitle') or "arXiv"
        year = get_f('year')
        
        # 1. 개별 BibTeX 파일 저장
        bib_filename = f"{key}.bib"
        with open(os.path.join(FILES_DIR, bib_filename), "w", encoding="utf-8") as f:
            f.write(full_block)

        # 2. 마크다운 생성
        paper_url = URL_MAP.get(key, "")
        category = "conferences" if entry_type == "inproceedings" else ("preprints" if "arxiv" in venue.lower() else "manuscripts")
        authors_bold = bold_name(get_f('author'))
        date_str = f"{year}-01-01"

        md_content = f"""---
title: "{title}"
collection: publications
category: {category}
permalink: /publication/{date_str}-{key}
date: {date_str}
venue: '{venue}'
paperurl: '{paper_url}'
bibtexurl: '/{FILES_DIR}/{bib_filename}'
citation: '{authors_bold}. ({year}). &quot;{title}.&quot; <i>{venue}</i>.'
---
"""
        with open(os.path.join(OUT_DIR, f"{date_str}-{key}.md"), "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Generated: {key} (.md and .bib)")

if __name__ == "__main__":
    generate_md_and_bib()