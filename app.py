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
    page_title="ATS Intelligence Pro",
    page_icon="🎯",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS & ANIMATIONS
# ---------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Outfit', sans-serif;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2.5rem;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
        transition: all 0.4s ease;
    }

    /* Iconic Badge Labels */
    .input-badge {
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(90deg, #1e293b, #334155);
        color: white;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        letter-spacing: 1px;
    }

    /* Interactive Box Glow */
    [data-testid="stFileUploader"], textarea {
        border-radius: 18px !important;
        border: 2px solid transparent !important;
        background: rgba(255, 255, 255, 0.6) !important;
        transition: all 0.3s ease !important;
    }
    
    textarea:focus {
        border: 2px solid #e73c7e !important;
        box-shadow: 0 0 15px rgba(231, 60, 126, 0.2) !important;
    }

    /* Main Title */
    .hero-text {
        text-align: center;
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.2);
    }

    /* Button Styling */
    .stButton>button {
        background: #1e293b;
        color: white;
        border-radius: 15px;
        padding: 15px 30px;
        border: none;
        font-weight: 700;
        width: 100%;
        margin-top: 10px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton>button:hover {
        background: white;
        color: #e73c7e;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOGIC
# ---------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted: text += extracted
    return text

# ---------------------------------------------------
# UI DESIGN
# ---------------------------------------------------

st.markdown('<div class="hero-text">ATS INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; opacity: 0.9; font-size: 1.1rem; margin-bottom: 3rem;'>Bridge the gap between your resume and the hiring algorithm.</p>", unsafe_allow_html=True)

# Grid Layout
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<span class="input-badge">📁 STEP 1: RESUME</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    st.markdown("<p style='font-size: 12px; color: #64748b; margin-top: 8px;'>Accepted format: PDF only</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<span class="input-badge">📝 STEP 2: JOB DESCRIPTION</span>', unsafe_allow_html=True)
    job_description = st.text_area("Paste JD", height=105, placeholder="Paste the job requirements here...", label_visibility="collapsed")
    st.markdown("<p style='font-size: 12px; color: #64748b; margin-top: 8px;'>Include keywords and tech stack</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Action
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    analyze_btn = st.button("Analyze Match")

if analyze_btn:
    if uploaded_file and job_description:
        with st.status("Running AI Matcher...", expanded=False):
            resume_text = extract_text_from_pdf(uploaded_file)
            tfidf = TfidfVectorizer(stop_words='english')
            vectors = tfidf.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])
            score = round(similarity[0][0] * 100, 1)
        
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        
        res_1, res_2 = st.columns([1, 1])
        
        with res_1:
            st.markdown(f"<div style='margin-top: 20px;'><span class='input-badge'>ANALYSIS RESULT</span></div>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='font-size: 100px; color: #1e293b; margin: 0;'>{score}%</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #475569; font-weight: 600;'>System Match Score</p>", unsafe_allow_html=True)
        
        with res_2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1e293b"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [0, 50], 'color': '#ffccd5'},
                        {'range': [50, 80], 'color': '#fff0f3'},
                        {'range': [80, 100], 'color': '#c1fba4'}
                    ],
                }
            ))
            fig.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        if score >= 80:
            st.success("✨ **Elite Match!** Your profile is highly compatible.")
        elif score >= 50:
            st.warning("⚡ **Strong Match.** Add a few more keywords to reach 80%+")
        else:
            st.error("📉 **Low Match.** Tailor your bullet points to the JD requirements.")

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.toast("Please fill both sections!", icon="⚠️")

st.markdown("<div style='text-align: center; color: white; margin-top: 30px; font-weight: 500;'>Optimized for Modern Applicant Tracking Systems</div>", unsafe_allow_html=True)
