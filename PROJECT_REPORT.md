# AI-Powered Resume Ranker

## 1. Project Overview
The AI-Powered Resume Ranker is a web application that helps HR teams rank candidates by comparing their resumes with a job description. The system extracts text from uploaded PDF or TXT files, processes the content, and produces a ranked list with match percentage, matching skills, and missing skills.

## 2. Problem Statement
HR teams often receive a large number of resumes for a single job opening. Manually reviewing each resume is time-consuming and may lead to inconsistent selection. This project automates the initial screening process.

## 3. Objectives
- Upload a job description
- Upload one or more resumes
- Automatically rank candidates
- Show match percentage and skill alignment
- Export ranking results as CSV
- Support model-based scoring with a training workflow

## 4. Technologies Used
- Python
- Flask
- HTML/CSS
- scikit-learn
- spaCy
- pdfplumber
- pandas
- NumPy

## 5. Methodology
1. Upload job description and resumes.
2. Extract text from PDF or TXT files.
3. Clean and preprocess the text.
4. Extract keywords and skills using NLP.
5. Compute similarity using TF-IDF and cosine similarity.
6. Rank candidates and display results.
7. Optionally train and evaluate a machine learning model using CSV data.

## 6. Dataset
The project supports the uploaded dataset folder and also includes a sample training CSV. For internship submission, this can be explained as a collection of resumes and job descriptions used to build and test the ranking logic.

## 7. Results
The system produces:
- ranked candidate list
- match percentage
- matching skills
- missing skills
- CSV export
- evaluation metrics when a trained model is available

## 8. Conclusion
The project demonstrates how AI and NLP can be used to automate resume screening and make recruitment faster, more efficient, and easier to manage.
