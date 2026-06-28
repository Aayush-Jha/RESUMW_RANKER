import argparse
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from utils.dataset_loader import load_training_data


def train_model(dataset_path, model_path="models/resume_ranker_model.joblib"):
    df = load_training_data(dataset_path)
    df = df.dropna(subset=["resume_text", "job_description", "label"])

    X = df[["resume_text", "job_description"]].apply(
        lambda row: f"{row['resume_text']} {row['job_description']}",
        axis=1,
    )
    y = df["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    pipeline = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), min_df=1),
        LogisticRegression(max_iter=4000),
    )
    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    metrics = {
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "precision": round(precision_score(y_test, predictions, zero_division=0), 4),
        "recall": round(recall_score(y_test, predictions, zero_division=0), 4),
        "f1": round(f1_score(y_test, predictions, zero_division=0), 4),
    }

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump({"model": pipeline, "metrics": metrics}, model_path)

    print("Training complete")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    return pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", help="Path to a CSV dataset with resume_text, job_description, label")
    parser.add_argument("--model-path", default="models/resume_ranker_model.joblib")
    args = parser.parse_args()
    train_model(args.dataset, args.model_path)
