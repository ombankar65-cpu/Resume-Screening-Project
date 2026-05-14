import streamlit as st

from pdf_reader import get_pdf_text
from text_cleaner import clean_text
from ats_score import get_ats_score


# Page Config
st.set_page_config(page_title="ATS Resume Checker", page_icon="📄")


# Title
st.title("📄 ATS Resume Screening App")

st.write("Upload Resume PDF and Paste Job Description")


# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


# Job Description Input
job_description = st.text_area(
    "Paste Job Description Here"
)


# Button
if st.button("Check ATS Score"):

    if uploaded_file is not None and job_description != "":

        # Extract Resume Text
        resume_text = get_pdf_text(uploaded_file)

        # Clean Text
        clean_resume = clean_text(resume_text)
        clean_jd = clean_text(job_description)

        # ATS Score
        score = get_ats_score(clean_resume, clean_jd)

        # Show Score
        st.success(f"ATS Score: {score}%")

        # Score Message
        if score >= 80:
            st.success("Excellent Resume Match ✅")

        elif score >= 60:
            st.warning("Good Match 👍")

        else:
            st.error("Resume Needs Improvement ❌")

    else:
        st.warning("Please Upload Resume and Enter Job Description")
