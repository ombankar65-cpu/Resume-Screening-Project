import streamlit as st
import pdf_reader
import text_cleaner
import ats_score
import time

# Page Configuration
st.set_page_config(
    page_title="Smart ATS Pro",
    page_icon="📄",
    layout="wide",
)

# Custom CSS for Background Animation and Layout
st.markdown("""
    <style>
    /* Animated Gradient Background */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    /* Make text readable on animated background */
    .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        color: white !important;
    }

    /* Style for the Input Containers */
    div.stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.9);
        color: #333 !important;
        border-radius: 10px;
    }
    
    div[data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #ffffff;
        color: #e73c7e !important;
        font-weight: 800;
        font-size: 1.2rem;
        border: none;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        background-color: #f0f0f0;
        color: #23a6d5 !important;
    }

    .score-container {
        padding: 40px;
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
        margin-top: 25px;
    }

    .score-text {
        font-size: 80px;
        font-weight: 900;
        color: #e73c7e !important;
        margin-bottom: 0;
    }
    
    .score-label {
        color: #333 !important;
        font-size: 24px;
        font-weight: 600;
    }

    /* Fix: Explicitly remove borders/lines */
    hr {
        display: none !important;
    }
    </style>
    """, unsafe_allow_headers=True)

def main():
    # Header Section
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 0;'>Smart ATS Resume Analyzer</h1>", unsafe_allow_headers=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.9;'>Optimize your career path with AI-driven insights</p>", unsafe_allow_headers=True)

    st.write("") # Spacing

    # Layout: Two columns for input
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📂 Upload Resume")
        uploaded_file = st.file_uploader("Upload your PDF Resume", type=["pdf"])
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")

    with col2:
        st.subheader("📝 Job Description")
        job_description = st.text_area("Paste requirements", height=200, placeholder="Enter skills, experience, and role details...")

    st.markdown("<br>", unsafe_allow_headers=True)

    # Action button
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        submit = st.button("Analyze Match")

    if submit:
        if uploaded_file and job_description.strip():
            with st.spinner("🚀 AI is analyzing your compatibility..."):
                # Extraction & Cleaning
                resume_text = pdf_reader.get_pdf_text(uploaded_file)
                cleaned_resume = text_cleaner.clean_text(resume_text)
                cleaned_jd = text_cleaner.clean_text(job_description)
                
                # ATS Scoring
                score = ats_score.get_ats_score(cleaned_resume, cleaned_jd)
                time.sleep(1) 

            # Result Display
            st.markdown(f"""
            <div class='score-container'>
                <div class='score-label'>MATCH COMPATIBILITY</div>
                <div class='score-text'>{score}%</div>
            </div>
            """, unsafe_allow_headers=True)
            
            # Match animations
            if score >= 75:
                st.balloons()
                st.success("🎉 Excellent! Your profile is a strong match.")
            elif score >= 50:
                st.info("👍 Good potential. Tailor your keywords slightly to improve score.")
            else:
                st.warning("🧐 Opportunity for improvement. Align your resume more closely with the JD.")
        else:
            st.error("Please upload a resume and provide a job description.")

if __name__ == '__main__':
    main()
