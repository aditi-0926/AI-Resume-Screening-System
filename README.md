# AI Resume Screening & Job Description Matching System

An NLP-based resume screening application that analyzes resumes against job
descriptions using **spaCy**, **TF-IDF**, and **Cosine Similarity**. The system
extracts skills, calculates a match score, highlights missing skills, and
provides recommendations through an interactive Streamlit interface.

## Features

- 📄 Upload resumes and job descriptions as **PDF, DOCX, or TXT** (or paste text directly)
- 🧠 Skill extraction using a **spaCy PhraseMatcher** against a curated skills database (100+ skills across programming, data science, cloud, tools, and soft skills)
- 📊 **Match score** via TF-IDF vectorization + cosine similarity between resume and job description
- ✅ **Skill gap analysis**: see which required skills are present vs. missing
- 💡 **Rule-based recommendations** based on match strength and skill gaps
- 🎛️ Clean, interactive Streamlit UI with metrics, progress bar, and expandable skill lists

## Project Structure

```
resume_screener/
├── app.py            # Streamlit UI (entry point)
├── matcher.py         # Core NLP: skill extraction, TF-IDF, cosine similarity, recommendations
├── resume_parser.py   # Text extraction from PDF / DOCX / TXT
├── skills_db.py        # Curated skills database used for matching
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Run the app

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## How it works

1. **Text extraction** — `resume_parser.py` pulls raw text out of the uploaded
   PDF/DOCX/TXT file (or uses pasted text).
2. **Skill extraction** — `matcher.py` runs a spaCy `PhraseMatcher` over the
   text against `skills_db.py`'s master skills list to find known
   technical and soft skills, case-insensitively.
3. **Match scoring** — Both documents are vectorized with `TfidfVectorizer`
   and compared using cosine similarity to produce an overall match
   percentage.
4. **Gap analysis** — The job description's skill set minus the resume's
   skill set gives the missing skills; the intersection gives matched skills.
5. **Recommendations** — Simple rules turn the match score and skill gaps
   into human-readable suggestions.

## Extending this project

- Swap the rule-based skills list for a trained NER model for broader skill coverage
- Add support for ranking multiple resumes against a single job description in bulk
- Add weighting (e.g. required vs. nice-to-have skills) if the job description distinguishes them
- Persist results to a database for tracking candidates over time
- Add authentication and a recruiter dashboard for managing multiple job postings
