import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main App */
.stApp {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: white;
}

/* Hide Streamlit Header */
header {
    visibility: hidden;
}

/* Main Container */
.main-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 40px;
    border-radius: 25px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 10px 40px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.1);
    margin-top: 20px;
}

/* Title */
.main-title {
    font-size: 55px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    font-size: 18px;
    color: #CBD5E1;
    margin-bottom: 35px;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    border: 2px dashed #8B5CF6;
    border-radius: 20px;
    padding: 20px;
}

/* Text Area */
textarea {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 2px solid #334155 !important;
    font-size: 16px !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: 500 !important;
}

/* Button */
.stButton>button {
    width: 100%;
    height: 58px;
    border: none;
    border-radius: 15px;
    background: linear-gradient(90deg, #7C3AED, #4F46E5);
    color: white;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
    margin-top: 15px;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0px 10px 25px rgba(124,58,237,0.5);
}

/* Score Card */
.score-card {
    background: linear-gradient(135deg, #7C3AED, #4F46E5);
    padding: 40px;
    border-radius: 25px;
    text-align: center;
    margin-top: 35px;
    color: white;
    box-shadow: 0px 10px 35px rgba(124,58,237,0.4);
}

/* Score Text */
.score-text {
    font-size: 70px;
    font-weight: bold;
}

/* Score Label */
.score-label {
    font-size: 20px;
    opacity: 0.9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🚀 ATS Resume Analyzer")

menu = st.sidebar.radio(
    "Navigation",
    ["ATS Checker", "About Project"]
)

# ---------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------

def extract_text_from_pdf(uploaded_file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text

    return text

# ---------------------------------------------------
# ATS CHECKER PAGE
# ---------------------------------------------------

if menu == "ATS Checker":

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown(
        '<div class="main-title">Smart ATS Resume Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Analyze your resume against job descriptions using NLP-powered ATS matching.</div>',
        unsafe_allow_html=True
    )

    # Layout
    col1, col2 = st.columns(2)

    with col1:

        uploaded_file = st.file_uploader(
            "📄 Upload Resume",
            type=["pdf"]
        )

    with col2:

        job_description = st.text_area(
            "💼 Paste Job Description",
            height=250
        )

    # Analyze Button
    calculate = st.button("⚡ Analyze Resume")

    # ---------------------------------------------------
    # CALCULATE ATS SCORE
    # ---------------------------------------------------

    if calculate:

        if uploaded_file is not None and job_description != "":

            # Extract Resume Text
            resume_text = extract_text_from_pdf(uploaded_file)

            # TF-IDF
            tfidf = TfidfVectorizer(stop_words='english')

            vectors = tfidf.fit_transform([
                resume_text,
                job_description
            ])

            # Similarity
            similarity = cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )

            score = round(similarity[0][0] * 100, 2)

            # ---------------------------------------------------
            # SCORE CARD
            # ---------------------------------------------------

            st.markdown(f"""
            <div class="score-card">

                <div class="score-label">
                    ATS MATCH SCORE
                </div>

                <div class="score-text">
                    {score}%
                </div>

            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # Progress Bar
            st.progress(int(score))

            # ---------------------------------------------------
            # GAUGE CHART
            # ---------------------------------------------------

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Resume Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#8B5CF6"},
                    'bgcolor': "white"
                }
            ))

            fig.update_layout(
                paper_bgcolor="#0F172A",
                font={'color': "white"}
            )

            st.plotly_chart(fig, use_container_width=True)

            # ---------------------------------------------------
            # RESULT MESSAGE
            # ---------------------------------------------------

            if score >= 80:

                st.success(
                    "✅ Excellent Match! Your resume strongly matches the job description."
                )

            elif score >= 60:

                st.warning(
                    "⚠️ Good Match! Add more relevant keywords and skills."
                )

            else:

                st.error(
                    "❌ Low Match Score! Improve your resume according to the job description."
                )

        else:

            st.warning(
                "⚠️ Please upload resume and enter job description."
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------

elif menu == "About Project":

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.markdown(
        '<div class="main-title">About This Project</div>',
        unsafe_allow_html=True
    )

    st.write("""

### 🚀 Smart ATS Resume Analyzer

This application compares resumes with job descriptions using NLP techniques.

### 🔥 Features

- Resume PDF Upload
- ATS Match Score
- NLP-based Similarity Matching
- Interactive Dashboard
- Modern UI Design

### 🧠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Plotly
- PyPDF2

""")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
