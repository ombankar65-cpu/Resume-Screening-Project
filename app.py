import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Pro ATS Optimizer",
    page_icon="🎯",
    layout="wide"
)

# ---------------------------------------------------
# ADVANCED CUSTOM CSS & ANIMATIONS
# ---------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top left, #0e1525, #1c263b);
        color: #e2e8f0;
    }

    /* Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(99, 102, 241, 0); }
        100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
    }

    /* Containers */
    .main-card {
        animation: fadeIn 0.8s ease-out;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }

    /* Titles */
    .glitch-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Inputs */
    [data-testid="stFileUploader"], textarea {
        border-radius: 15px !important;
        border: 1px solid #334155 !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1 !important;
        background: rgba(99, 102, 241, 0.05);
    }

    /* Custom Button */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s;
        width: 100%;
        margin-top: 20px;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(168, 85, 247, 0.3);
    }

    /* Score Badge */
    .score-container {
        text-align: center;
        padding: 30px;
        border-radius: 25px;
        background: rgba(15, 23, 42, 0.5);
        border: 2px solid #6366f1;
        animation: pulse 2s infinite;
        margin: 20px 0;
    }

    .score-val {
        font-size: 80px;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1;
    }
    
    /* Hide Default Header */
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOGIC FUNCTIONS
# ---------------------------------------------------

def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted: text += extracted
    return text

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Navigation")
    menu = st.radio("", ["ATS Engine", "Insights"])
    st.divider()
    st.info("Upload your resume and JD to see how well you rank.")

# ---------------------------------------------------
# MAIN UI
# ---------------------------------------------------

if menu == "ATS Engine":
    st.markdown('<div class="glitch-title">AI Resume Scanner</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94a3b8; font-size:1.2rem;">Optimize your career path with neural matching technology.</p>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### 📄 Resume")
            uploaded_file = st.file_uploader("Drop PDF here", type=["pdf"], label_visibility="collapsed")
            if uploaded_file:
                st.success("File Received")

        with col2:
            st.markdown("### 💼 Job Description")
            job_description = st.text_area("Paste the JD", height=200, placeholder="Paste requirements here...", label_visibility="collapsed")

        if st.button("🚀 INITIATE ANALYSIS"):
            if uploaded_file and job_description:
                with st.spinner("Decoding Resume structure..."):
                    time.sleep(1) # Visual effect
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    # NLP Calc
                    tfidf = TfidfVectorizer(stop_words='english')
                    vectors = tfidf.fit_transform([resume_text, job_description])
                    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
                    score = round(similarity[0][0] * 100, 1)

                    # Display Results
                    st.divider()
                    res_col1, res_col2 = st.columns([1, 2])
                    
                    with res_col1:
                        st.markdown(f"""
                        <div class="score-container">
                            <div style="font-size:14px; color:#94a3b8; letter-spacing:2px;">MATCH RATE</div>
                            <div class="score-val">{score}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with res_col2:
                        # Chart
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=score,
                            gauge={
                                'axis': {'range': [0, 100], 'tickcolor': "#94a3b8"},
                                'bar': {'color': "#6366f1"},
                                'bgcolor': "rgba(0,0,0,0)",
                                'steps': [
                                    {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.1)'},
                                    {'range': [50, 80], 'color': 'rgba(245, 158, 11, 0.1)'},
                                    {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.1)'}
                                ],
                            }
                        ))
                        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig, use_container_width=True)

                    if score >= 80:
                        st.balloons()
                        st.success("🔥 High Probability of selection! Your keywords align perfectly.")
                    elif score >= 50:
                        st.warning("⚡ Good start, but try adding more specific technical skills from the JD.")
                    else:
                        st.error("📉 Low match. Consider tailoring your experience descriptions.")
            else:
                st.error("Please provide both a Resume and a Job Description.")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("Project Architecture")
    st.write("Using TF-IDF (Term Frequency-Inverse Document Frequency) to vectorize text and Cosine Similarity to calculate the spatial distance between your resume and the job requirements.")
    st.code("""# Core Math
similarity = cosine_similarity(vectors[0:1], vectors[1:2])""", language="python")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div style="text-align:center; padding:20px; color:#64748b; font-size:0.8rem;">
    Powered by Streamlit & Scikit-Learn | Built for modern recruiters
</div>
""", unsafe_allow_html=True)
