# AI Resume Ranker

An AI-powered Flask web app that ranks resumes against a job description and displays match percentage, matching skills, missing skills, and CSV export.

## Features
- Upload a job description (.pdf or .txt)
- Upload multiple resumes (.pdf or .txt)
- Rank candidates automatically
- Show matching and missing skills
- Download results as CSV
- View a visual match distribution chart
- Train a simple machine learning model from CSV data

## Project Structure
- app.py
- wsgi.py
- requirements.txt
- Procfile
- templates/
- static/
- utils/
- dataset/
- tests/

## Setup Locally
1. Install Python 3.12+
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   python app.py
4. Open: http://127.0.0.1:5000

## Deployment
Use this start command on Render:
- gunicorn wsgi:app

## Training a Model
Run:
- python train_model.py dataset/training_data.csv --model-path models/resume_ranker_model.joblib
