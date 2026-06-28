import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_PATH = "models/resume_ranker_model.joblib"


def _load_model():
    if os.path.exists(MODEL_PATH):
        artifact = joblib.load(MODEL_PATH)
        if isinstance(artifact, dict) and "model" in artifact:
            return artifact["model"]
        return artifact
    return None


def rank_resumes(job_description, resumes):
    job_text = " ".join(job_description.split()) if isinstance(job_description, str) else " ".join(job_description)

    documents = [job_text] + [text for _, text in resumes]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    results = []
    job_words = set(job_text.lower().split())
    model = _load_model()
    for idx, (name, text) in enumerate(resumes):
        resume_words = set(text.lower().split())
        overlap = len(job_words.intersection(resume_words))
        overlap_score = (overlap / max(len(job_words), 1)) * 100
        similarity_score = float(similarities[idx])
        direct_match_bonus = overlap * 15
        heuristic_score = round(min(100.0, overlap_score + (similarity_score * 100 * 0.2) + direct_match_bonus), 2)

        if model is not None:
            prediction_input = f"{text} {job_text}"
            predicted_score = float(model.predict_proba([prediction_input])[0][1] * 100)
            match_percentage = round(min(100.0, max(heuristic_score, predicted_score * 0.7 + heuristic_score * 0.3)), 2)
        else:
            match_percentage = heuristic_score

        matching_skills = sorted(job_words.intersection(resume_words))
        missing_skills = sorted(job_words - resume_words)
        results.append({
            "name": name,
            "match_percentage": match_percentage,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
        })

    results.sort(key=lambda item: item["match_percentage"], reverse=True)
    return results
