---
permalink: /
title: "About Me"
author_profile: false
redirect_from: 
  - /about/
  - /about.html
---

{% include profile-header.html %}

I am a **Postdoctoral Researcher** at **Nanyang Technological University (NTU)** in Singapore, hosted by [Prof. Jaehong Yoon](https://jaehong31.github.io/) and **Ulsan National Institute of Science and Technology (UNIST)** in Korea, mentored by [Prof. Saerom Park](https://sites.google.com/view/safe-ai-lab/home). I received my **Ph.D.** in Industrial Engineering from **Seoul National University (SNU)**, advised by [Prof. Jaewook Lee](https://safeai.snu.ac.kr/home).

My research focuses on building **Trustworthy AI**, with a particular emphasis on ensuring the privacy, fairness, and robustness of machine learning systems. 

## Research Interests
* **Trustworthy AI**: Privacy-preserving machine learning (differential privacy, attacks/defense) and fairness.
* **Generative Models**: Enhancing safety and utility in Diffusion models, Flow matching, and Large Language Models (LLMs).

## Education
* **Ph.D.** in **Industrial Engineering**, Seoul National University, 2026
    * *Dissertation: [Trustworthy Generative Model: from Privacy to Fairness](https://s-space.snu.ac.kr/handle/10371/234094)*
* **B.S.** in **Industrial Engineering** and **Mathematics**, Yonsei University, 2021

## News

{% include news-feed.html limit=10 %}

## Selected Publications

<div class="pub-list">
{% assign selected = site.publications | where: "selected", true | sort: "date" | reverse %}
{% for pub in selected %}
  {% include publication-card.html pub=pub full_label=true %}
{% endfor %}
</div>

See [the full list](/publications/) or my [Google Scholar profile](https://scholar.google.com/citations?user=3u0-O2sAAAAJ).