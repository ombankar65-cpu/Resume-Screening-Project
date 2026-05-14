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

/* Import Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main Background */
.stApp {
    background: #0F172A;
    color: white;
}

/* Remove Streamlit Header */
header {
    visibility: hidden;
}

/* Main Container */
.main-container {
    background: linear-gradient(135deg, #111827, #1E293B);
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
}

/* Title */
.main-title {
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    color: #94A3B8;
    font-size: 18px;
    margin-bottom: 40px;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: #1E293B;
    border: 2px dashed #6366F1;
    border-radius: 18px;
    padding: 20px;
}

/* Text Area */
textarea {
    background-color: #1E293B !important;
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
    height: 55px;
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
    box-shadow: 0px 8px 25px rgba(124,58,237,0.4);
}

/* Score Card */
.score-card {
    background: linear-gradient(135deg, #7C3AED, #4F46E5);
    padding: 35px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-top: 30px;
    box-shadow: 0px 10px 35px rgba(79,70,229,0.4);
}

/* Score Text */
.score-text {
    font-size: 65px;
    font-weight: bold;
}

/* Small Text */
.score-label {
    font-size: 20px;
    opacity: 0.9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Success Box */
.stSuccess {
    border-radius: 15px;
}

/* Warning Box */
.stWarning {
    border-radius: 15px;
}

/* Error Box */
.stError {
    border-radius: 15px;
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
# PDF EXTRACT FUNCTION
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
        '<div class="sub-title">Analyze your resume against job descriptions using AI-powered ATS matching.</div>',
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

    # Button
    calculate = st.button("⚡ Analyze Resume")

    # ---------------------------------------------------
    # SCORE CALCULATION
    # ---------------------------------------------------

    if calculate:

        if uploaded_file is not None and job_description != "":

            resume_text = extract_text_from_pdf(uploaded_file)

            tfidf = TfidfVectorizer(stop_words='english')

            vectors = tfidf.fit_transform([
                resume_text,
                job_description
            ])

            similarity = cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )

            score = round(similarity[0][0] * 100, 2)

            # Score Card
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

            # Progress
            st.progress(int(score))

            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Resume Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#7C3AED"},
                    'bgcolor': "white",
                }
            ))

            fig.update_layout(
                paper_bgcolor="#111827",
                font={'color': "white"}
            )

            st.plotly_chart(fig, use_container_width=True)

            # Result Message
            if score >= 80:
                st.success("✅ Excellent Resume Match! Your resume is highly aligned with the job description.")

            elif score >= 60:
                st.warning("⚠️ Good Match! Add more relevant keywords and skills.")

            else:
                st.error("❌ Low Match Score! Improve your resume according to the job description.")

        else:
            st.warning("⚠️ Please upload resume and enter job description.")

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

    This application compares your resume with the job description using NLP techniques.

    ### 🔥 Features

    - Resume PDF Upload
    - ATS Match Score
    - NLP-based Matching
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
