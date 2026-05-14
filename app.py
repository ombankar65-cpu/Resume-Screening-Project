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

    /* Vertical Icon Badge Container */
    .vertical-header {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 5px;
        margin-bottom: 20px;
    }

    /* Modern Badge Styling with Deep Shadow */
    .input-label-badge {
        background: #1e293b;
        color: white;
        padding: 8px 20px;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3); /* Stronger Shadow */
        border: 1px solid rgba(255,255,255,0.1);
        text-transform: uppercase;
    }

    .badge-subtext {
        color: #475569;
        font-size: 0.85rem;
        font-weight: 500;
        margin-left: 2px;
    }

    /* Glassmorphism Container with Shadow */
    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 2.5rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15); /* Deep Card Shadow */
        margin-bottom: 25px;
        transition: all 0.4s ease;
    }

    .glass-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.25);
        background: rgba(255, 255, 255, 0.9);
    }

    /* Input Box Styles */
    [data-testid="stFileUploader"], .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        border-radius: 18px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Button Styling */
    .stButton>button {
        background: #1e293b;
        color: white;
        border-radius: 18px;
        padding: 20px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: #e73c7e;
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(231, 60, 126, 0.4);
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

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
# MAIN UI
# ---------------------------------------------------

st.markdown("<h1 style='text-align: center; color: white; font-size: 4rem; font-weight: 800; text-shadow: 0 10px 20px rgba(0,0,0,0.2);'>ATS SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; margin-bottom: 4rem; font-size: 1.2rem;'>Advanced Semantic Match Analysis</p>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('''
        <div class="vertical-header">
            <span class="input-label-badge">STEP 01</span>
            <span class="badge-subtext">ATTACH YOUR RESUME (PDF)</span>
        </div>
    ''', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('''
        <div class="vertical-header">
            <span class="input-label-badge">STEP 02</span>
            <span class="badge-subtext">PASTE JOB DESCRIPTION</span>
        </div>
    ''', unsafe_allow_html=True)
    job_description = st.text_area("Paste JD", height=105, placeholder="Paste requirements here...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 1.2, 1])
with btn_col:
    analyze_btn = st.button("PROCEED TO ANALYSIS")

if analyze_btn:
    if uploaded_file and job_description:
        with st.status("Analyzing...", expanded=False):
            resume_text = extract_text_from_pdf(uploaded_file)
            tfidf = TfidfVectorizer(stop_words='english')
            vectors = tfidf.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])
            score = round(similarity[0][0] * 100, 1)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        res_1, res_2 = st.columns([1, 1.5])
        
        with res_1:
            st.markdown("<div style='text-align: center; margin-top: 30px;'><span class='input-label-badge'>MATCH RATE</span></div>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 100px; color: #1e293b; margin: 0;'>{score}%</h1>", unsafe_allow_html=True)
        
        with res_2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1e293b"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [0, 50], 'color': '#fca5a5'},
                        {'range': [50, 80], 'color': '#fde68a'},
                        {'range': [80, 100], 'color': '#86efac'}
                    ],
                }
            ))
            fig.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        if score >= 80:
            st.success("🎯 **Excellent Alignment!**")
        elif score >= 50:
            st.warning("⚠️ **Solid Match.**")
        else:
            st.error("❌ **Low Alignment.**")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.toast("Please upload a file and a job description.", icon="⚠️")
