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

    /* Modern Badge Styling */
    .input-label-badge {
        background: rgba(30, 41, 59, 0.9);
        color: white;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Glassmorphism Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }

    .glass-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.85);
        box-shadow: 0 20px 45px rgba(0,0,0,0.15);
    }

    /* Input Box Enhancements */
    [data-testid="stFileUploader"], .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.5) !important;
        border: 2px solid transparent !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #e73c7e !important;
        box-shadow: 0 0 15px rgba(231, 60, 126, 0.3) !important;
    }

    /* Main Title */
    .main-title {
        color: white !important;
        font-size: 3.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        text-shadow: 0 10px 20px rgba(0,0,0,0.2);
        margin-bottom: 0px;
    }

    /* Custom Button */
    .stButton>button {
        background: #1e293b;
        color: white;
        border-radius: 15px;
        padding: 18px 30px;
        border: none;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: white;
        color: #1e293b;
        transform: scale(1.03);
    }

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

st.markdown("<h1 class='main-title'>AI ATS SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; margin-bottom: 3.5rem; font-size: 1.2rem; opacity: 0.9;'>Instant Keyword Optimization & Match Analysis</p>", unsafe_allow_html=True)

# Main Interaction Area
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-label-badge">STEP 1: ATTACH RESUME</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    st.markdown("<p style='color: #64748b; font-size: 0.8rem; margin-top: 10px;'>Supported format: PDF</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-label-badge">STEP 2: JOB TARGET</div>', unsafe_allow_html=True)
    job_description = st.text_area("Paste Description", height=105, placeholder="Paste the job description here...", label_visibility="collapsed")
    st.markdown("<p style='color: #64748b; font-size: 0.8rem; margin-top: 10px;'>Include skills & requirements</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Trigger (Centered)
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    analyze_btn = st.button("START ANALYSIS")

if analyze_btn:
    if uploaded_file and job_description:
        with st.status("Decoding Match Logic...", expanded=False) as status:
            resume_text = extract_text_from_pdf(uploaded_file)
            time.sleep(0.4)
            tfidf = TfidfVectorizer(stop_words='english')
            vectors = tfidf.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])
            score = round(similarity[0][0] * 100, 1)
            time.sleep(0.4)
            status.update(label="Analysis Complete!", state="complete")

        # Results Display
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.markdown(f"<div style='text-align: center; margin-top: 20px;'><span class='input-label-badge'>FINAL SCORE</span></div>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 90px; color: #1e293b; margin: 0;'>{score}%</h1>", unsafe_allow_html=True)
        
        with c2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "#1e293b"},
                    'bar': {'color': "#1e293b"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0, 40], 'color': '#fca5a5'},
                        {'range': [40, 75], 'color': '#fde68a'},
                        {'range': [75, 100], 'color': '#86efac'}
                    ],
                }
            ))
            fig.update_layout(height=260, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        if score >= 80:
            st.balloons()
            st.success("🎯 **Elite Match!** Your resume is highly aligned with this position.")
        elif score >= 50:
            st.warning("⚠️ **Strong Foundation.** Adding more specific industry keywords could boost your score.")
        else:
            st.error("❌ **Low Alignment.** The system detected missing core competencies required for this JD.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.toast("Missing Data: Please upload both fields.", icon="⚠️")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div style='text-align: center; margin-top: 50px; color: white; font-weight: 500; letter-spacing: 1px;'>
    AI ENGINE POWERED BY TF-IDF SEMANTIC MATCHING
</div>
""", unsafe_allow_html=True)
