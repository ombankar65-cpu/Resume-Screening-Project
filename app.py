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
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
    }

    /* Titles */
    h1 {
        color: #1e293b !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Custom Button */
    .stButton>button {
        background: #1e293b;
        color: white;
        border-radius: 12px;
        padding: 10px 25px;
        border: none;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stButton>button:hover {
        background: #334155;
        color: #60a5fa;
        transform: scale(1.02);
    }

    /* File Uploader styling */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.5);
        border-radius: 15px;
        padding: 10px;
    }

    /* Hide redundant elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted: text += extracted
    return text

# ---------------------------------------------------
# MAIN APP INTERFACE
# ---------------------------------------------------

# Centered Layout Header
st.markdown("<h1 style='text-align: center;'>🚀 Smart ATS Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #475569; margin-bottom: 2rem;'>Optimize your resume for the modern job market.</p>", unsafe_allow_html=True)

# Main Interaction Area
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📄 Your Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💼 Job Details")
    job_description = st.text_area("Paste Description", height=100, placeholder="Requirements, skills, and roles...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Trigger
analyze_btn = st.button("RUN AI SCANNER")

if analyze_btn:
    if uploaded_file and job_description:
        with st.status("Analyzing Match...", expanded=True) as status:
            st.write("Extracting text from PDF...")
            resume_text = extract_text_from_pdf(uploaded_file)
            time.sleep(0.5)
            
            st.write("Comparing keywords...")
            tfidf = TfidfVectorizer(stop_words='english')
            vectors = tfidf.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])
            score = round(similarity[0][0] * 100, 1)
            time.sleep(0.5)
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # Results Display
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.markdown(f"<h3 style='text-align: center;'>Match Score</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #1e293b;'>{score}%</h1>", unsafe_allow_html=True)
        
        with c2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "black"},
                    'bar': {'color': "#1e293b"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [0, 40], 'color': '#f87171'},
                        {'range': [40, 75], 'color': '#fbbf24'},
                        {'range': [75, 100], 'color': '#34d399'}
                    ],
                }
            ))
            fig.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        # Verdict
        if score >= 80:
            st.balloons()
            st.success("🎯 **Perfect Match!** Your resume is optimized for this role.")
        elif score >= 50:
            st.warning("⚠️ **Solid Effort.** Try adding more specific keywords from the JD.")
        else:
            st.error("❌ **Low Alignment.** We recommend revising your resume to match the JD requirements.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.toast("Please upload both a resume and job description!", icon="⚠️")

# ---------------------------------------------------
# FOOTER INFO
# ---------------------------------------------------
st.markdown("""
<div style='text-align: center; margin-top: 50px; color: white; font-weight: 600;'>
    Made with ❤️ for Job Seekers
</div>
""", unsafe_allow_html=True)
