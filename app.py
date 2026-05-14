import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ATS Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #f5f7fa, #c3cfe2);
    font-family: Arial, sans-serif;
}

/* Main Title */
.main-title {
    font-size: 45px;
    font-weight: bold;
    color: #1E3A8A;
    text-align: center;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #374151;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Card Design */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
    border: 1px solid #ddd;
    margin-bottom: 20px;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #4F46E5;
    border-radius: 15px;
    padding: 15px;
    background-color: #ffffff;
}

/* Text Area */
textarea {
    border-radius: 12px !important;
    border: 2px solid #4F46E5 !important;
}

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #9333EA, #4F46E5);
}

/* Score Box */
.score-box {
    background: linear-gradient(to right, #10B981, #059669);
    color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.2);
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
    font-size: 15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown(
    '<div class="main-title">📄 ATS Resume Screening System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Upload Resume & Compare with Job Description</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Go To",
    ["ATS Checker", "About Project"]
)

# ---------------------------------------------------
# PDF TEXT EXTRACTION FUNCTION
# ---------------------------------------------------

def extract_text_from_pdf(pdf_file):
    text = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# ---------------------------------------------------
# ATS CHECKER
# ---------------------------------------------------

if menu == "ATS Checker":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader(
            "📂 Upload Resume (PDF)",
            type=["pdf"]
        )

    with col2:
        job_description = st.text_area(
            "📝 Enter Job Description",
            height=250
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------
    # BUTTON
    # ---------------------------------------------------

    if st.button("🚀 Calculate ATS Score"):

        if uploaded_file is not None and job_description != "":

            # Extract Resume Text
            resume_text = extract_text_from_pdf(uploaded_file)

            # TF-IDF Vectorization
            tfidf = TfidfVectorizer(stop_words='english')

            vectors = tfidf.fit_transform([
                resume_text,
                job_description
            ])

            # Cosine Similarity
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])

            score = round(similarity[0][0] * 100, 2)

            # ---------------------------------------------------
            # SCORE DISPLAY
            # ---------------------------------------------------

            st.markdown(f"""
            <div class="score-box">
                ATS Match Score <br><br>
                {score}%
            </div>
            """, unsafe_allow_html=True)

            # ---------------------------------------------------
            # PROGRESS BAR
            # ---------------------------------------------------

            st.progress(int(score))

            # ---------------------------------------------------
            # GAUGE CHART
            # ---------------------------------------------------

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "ATS Score"},
                gauge={
                    'axis': {'range': [0, 100]}
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

            # ---------------------------------------------------
            # FEEDBACK
            # ---------------------------------------------------

            if score >= 80:
                st.success("✅ Excellent Resume Match!")
            elif score >= 60:
                st.warning("⚠️ Good Match, but can be improved.")
            else:
                st.error("❌ Resume Match is Low. Improve your resume.")

        else:
            st.warning("⚠️ Please upload resume and enter job description.")

# ---------------------------------------------------
# ABOUT SECTION
# ---------------------------------------------------

elif menu == "About Project":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.header("📘 About This Project")

    st.write("""
    This ATS Resume Screening System compares:

    - Resume Content
    - Job Description

    using NLP techniques like:

    ✅ TF-IDF Vectorization  
    ✅ Cosine Similarity  

    and calculates the ATS Match Score.
    """)

    st.write("### 🚀 Technologies Used")

    st.write("""
    - Python
    - Streamlit
    - Scikit-learn
    - PyPDF2
    - Plotly
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
