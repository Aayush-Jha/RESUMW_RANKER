import os
import csv
import joblib
from io import StringIO
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from utils.pdf_reader import extract_text_from_file
from utils.preprocess import extract_keywords
from utils.ranker import rank_resumes

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["ALLOWED_EXTENSIONS"] = {"pdf", "txt"}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jd_file = request.files.get("job_description")
        resume_files = request.files.getlist("resumes")

        if not jd_file or jd_file.filename == "":
            return render_template("index.html", error="Please upload a job description file.")
        if not resume_files or all(f.filename == "" for f in resume_files):
            return render_template("index.html", error="Please upload at least one resume.")

        jd_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(jd_file.filename))
        jd_file.save(jd_path)
        jd_text = extract_text_from_file(jd_path)

        resume_paths = []
        for resume_file in resume_files:
            if resume_file.filename == "":
                continue
            filename = secure_filename(resume_file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume_file.save(path)
            resume_paths.append(path)

        job_keywords = extract_keywords(jd_text)
        resume_texts = []
        for path in resume_paths:
            text = extract_text_from_file(path)
            resume_texts.append((os.path.basename(path), text))

        results = rank_resumes(job_keywords, resume_texts)
        average_match = round(sum(item["match_percentage"] for item in results) / len(results), 2) if results else 0
        csv_output = generate_csv(results)
        model_metrics = load_model_metrics()
        return render_template(
            "result.html",
            results=results,
            csv_output=csv_output,
            average_match=average_match,
            model_metrics=model_metrics,
        )

    return render_template("index.html")


@app.route("/download_csv")
def download_csv():
    csv_output = request.args.get("csv_output", "")
    stream = StringIO(csv_output)
    return send_file(stream, as_attachment=True, download_name="ranking.csv", mimetype="text/csv")


def load_model_metrics():
    model_path = os.path.join(os.path.dirname(__file__), "models", "resume_ranker_model.joblib")
    if not os.path.exists(model_path):
        return None
    artifact = joblib.load(model_path)
    if isinstance(artifact, dict) and "metrics" in artifact:
        return artifact["metrics"]
    return None


def generate_csv(results):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Rank", "Candidate", "Match Percentage", "Matching Skills", "Missing Skills"])
    for index, result in enumerate(results, start=1):
        writer.writerow([
            index,
            result["name"],
            f"{result['match_percentage']}%",
            ", ".join(result["matching_skills"]),
            ", ".join(result["missing_skills"]),
        ])
    return output.getvalue()


if __name__ == "__main__":
    app.run(debug=True)
