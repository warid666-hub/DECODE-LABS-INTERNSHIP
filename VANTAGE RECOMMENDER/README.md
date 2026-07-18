# Vantage — Live Career Path Recommender

A desktop app that matches your skills to the tech career paths that fit best — in real time. Built with TF-IDF vectorization and cosine similarity, the same core technique behind real-world recommendation engines.

## Preview

*(Add a short screen recording or GIF here of the skill chips being clicked and the match cards re-ranking live — this is the most compelling part of the project.)*

## What It Does

- Presents skills as clickable tags, grouped into categories (Languages, Data & ML, Cloud & DevOps, Web & Design, Engineering & Security)
- Select at least 3 skills and instantly see your **top 3 matching career paths**
- Each match shows a live percentage score and a short role description
- Rankings update **instantly** as you add or remove skills — no submit button

## How It Works — Content-Based Filtering

1. **Ingestion** — every job role is defined by a set of required skills (acts as the "raw_skills.csv" dataset)
2. **Vectorization (TF-IDF)** — both job roles and the user's selected skills are converted into weighted numerical vectors. Common/generic skills are down-weighted; specific, descriptive ones are weighted higher
3. **Scoring (Cosine Similarity)** — measures the angle between the user's skill vector and each job role's vector, producing a similarity score between 0 and 1
4. **Sorting & Filtering** — roles are ranked by score, and only the Top 3 are shown (protecting against choice overload)

```python
vectorizer = TfidfVectorizer()
role_vectors = vectorizer.fit_transform(job_role_documents)

query_vec = vectorizer.transform([" ".join(selected_skills)])
scores = cosine_similarity(query_vec, role_vectors)[0]
```

This project deliberately uses **content-based filtering** rather than collaborative filtering, since it requires no historical user data and works immediately — avoiding the "cold start" problem entirely.

## Tech Stack

- **Python 3**
- **scikit-learn** — TF-IDF vectorization and cosine similarity
- **CustomTkinter** — live GUI

## Installation & Usage

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/project-3-vantage-recommender

pip install -r requirements.txt

python vantage_recommender.py
```

## What This Project Demonstrates

- Turning qualitative attributes ("Python", "Cloud") into numerical vectors machines can compare
- Why raw keyword overlap fails, and how TF-IDF fixes it by weighting term specificity
- Cosine similarity as an industry-standard way to measure similarity independent of vector magnitude
- Building a full input → process → output recommendation pipeline, not just a lookup table

## Roadmap

- [ ] Add more job roles and a wider skill vocabulary
- [ ] Let users type free-text skills instead of only selecting from fixed tags
- [ ] Add a "why this match" breakdown showing which specific skills drove the score

## License

Open for learning and reference purposes.

