# AI Resume Ranker

A Flask-based web app that lets an HR user upload a job description and multiple resumes, then ranks the candidates by skill overlap using TF-IDF, NLP keyword extraction, and cosine similarity.

## Features
- Upload a job description file (.pdf or .txt)
- Upload multiple resumes (.pdf or .txt)
- Rank candidates by match percentage
- Show matching and missing skills
- Download the ranking as CSV
- Includes a sample dataset for demos

## Local setup
1. Install Python 3.12+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000

## Sample dataset
A ready-to-use demo dataset is included in the dataset folder with:
- one job description
- three sample resumes

You can upload these files directly from the web UI or copy them into the uploads folder for quick testing.

## Deploying to Render / Railway / Heroku
- Use the included Procfile and wsgi.py entrypoint.
- Set the start command to:
  ```bash
  gunicorn wsgi:app
  ```
- Ensure Python 3.12 is selected in the deployment environment.
