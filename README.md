# Resume-Screening-Project

Live Project Link : https://resume-screening-project-pbvubmrijaokgrbtuurbhq.streamlit.app/


# ATS Resume Screening Project

An AI-powered ATS (Applicant Tracking System) Resume Screening application built using Python, NLP, and Streamlit.
This project compares a candidate's resume with a job description and calculates the ATS match score using Natural Language Processing techniques.

---

# 🚀 Features

* 📄 Upload Resume PDF
* 💼 Paste Job Description
* 🧠 NLP-based Resume Analysis
* 📊 ATS Match Score Calculation
* ⚡ Cosine Similarity Matching
* 🎨 Modern Streamlit UI
* 📈 Interactive Gauge Chart
* ☁️ Streamlit Cloud Deployment

---

# 🛠️ Technologies Used

* Python
* Streamlit
* Scikit-learn
* NLP
* TF-IDF Vectorization
* Cosine Similarity
* PyPDF2
* Plotly

---

# 🧠 How It Works

1. User uploads resume PDF
2. User enters job description
3. Resume text is extracted using PyPDF2
4. TF-IDF converts text into vectors
5. Cosine Similarity calculates similarity score
6. ATS Match Score is displayed

---

# 📊 NLP Techniques Used

## TF-IDF Vectorization

TF-IDF converts text into numerical vectors based on word importance.

## Cosine Similarity

Measures similarity between resume and job description vectors.

\cos(\theta)=\frac{A \cdot B}{|A||B|}

---

# ☁️ Deployment

This project is deployed using Streamlit Cloud.
