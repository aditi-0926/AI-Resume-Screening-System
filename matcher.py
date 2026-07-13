"""
Core NLP matching engine.

- Skill extraction: spaCy PhraseMatcher against a curated skills database.
- Match scoring: TF-IDF vectorization + cosine similarity between resume and JD.
- Gap analysis: set difference between JD skills and resume skills.
- Recommendations: simple rule-based suggestions from the gaps.
"""
import re
import spacy
from spacy.matcher import PhraseMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_db import MASTER_SKILLS_LIST

_NLP = None
_MATCHER = None


def _load_nlp():
    """Lazily load spaCy model + PhraseMatcher once, then cache."""
    global _NLP, _MATCHER
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
        _MATCHER = PhraseMatcher(_NLP.vocab, attr="LOWER")
        patterns = [_NLP.make_doc(skill) for skill in MASTER_SKILLS_LIST]
        _MATCHER.add("SKILLS", patterns)
    return _NLP, _MATCHER


def clean_text(text: str) -> str:
    text = re.sub(r"[^\w\s\+\#\./-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str) -> set:
    """Return the set of known skills found in `text` (case-insensitive)."""
    nlp, matcher = _load_nlp()
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found.add(span.text.lower())
    return found


def calculate_match_score(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF vectorize both documents and return cosine similarity
    as a percentage (0-100).
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([clean_text(resume_text), clean_text(jd_text)])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)


def get_missing_skills(resume_skills: set, jd_skills: set) -> set:
    """Skills required by the JD but not found in the resume."""
    return jd_skills - resume_skills


def get_matching_skills(resume_skills: set, jd_skills: set) -> set:
    return resume_skills & jd_skills


def get_recommendations(missing_skills: set, match_score: float) -> list:
    """Rule-based, human-readable suggestions."""
    recs = []

    if match_score >= 75:
        recs.append("Strong match — this resume aligns well with the job description overall.")
    elif match_score >= 50:
        recs.append("Moderate match — some relevant experience present, but notable gaps remain.")
    else:
        recs.append("Weak match — this resume shares limited overlap with the job description's key terms.")

    if missing_skills:
        top_missing = sorted(missing_skills)[:8]
        recs.append(
            "Consider adding or highlighting these skills if applicable: "
            + ", ".join(top_missing) + "."
        )
        recs.append(
            "If the candidate has hands-on experience with these but didn't list them, "
            "encourage them to add specific projects or achievements that demonstrate it."
        )
    else:
        recs.append("No major skill gaps detected — resume covers the key skills mentioned in the job description.")

    return recs


def analyze(resume_text: str, jd_text: str) -> dict:
    """Run the full pipeline and return a results dictionary for the UI."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    match_score = calculate_match_score(resume_text, jd_text)
    missing = get_missing_skills(resume_skills, jd_skills)
    matching = get_matching_skills(resume_skills, jd_skills)
    recommendations = get_recommendations(missing, match_score)

    # Skill coverage: of the skills the JD asks for, how many does the resume have
    skill_coverage = round((len(matching) / len(jd_skills) * 100), 2) if jd_skills else 0.0

    return {
        "match_score": match_score,
        "skill_coverage": skill_coverage,
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "matching_skills": sorted(matching),
        "missing_skills": sorted(missing),
        "recommendations": recommendations,
    }
