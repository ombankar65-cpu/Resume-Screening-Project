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

# Custom CSS for a professional, modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: none;
    }
    .score-container {
        padding: 30px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
        border-top: 5px solid #007bff;
    }
    .score-text {
        font-size: 80px;
        font-weight: 800;
        color: #28a745;
        margin: 0;
    }
    .header-text {
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_headers=True)

def main():
    # Sidebar for extra information
    with st.sidebar:
        st.title("Settings & Tips")
        st.info("This AI tool uses TF-IDF Vectorization and Cosine Similarity to compare your resume against a job description.")
        st.markdown("---")
        st.markdown("### 💡 Quick Tips:")
        st.write("- Use keywords found in the job description.")
        st.write("- Avoid complex tables or graphics in your PDF.")
        st.write("- Ensure your contact info is clear.")

    # Header Section
    st.markdown("<h1 class='header-text' style='text-align: center;'>🚀 AI-Powered ATS Resume Scorer</h1>", unsafe_allow_headers=True)
    st.markdown("<p style='text-align: center; color: #6c757d; font-size: 1.2rem;'>Optimize your resume for the modern job market with instant feedback</p>", unsafe_allow_headers=True)
    st.markdown("---")

    # Layout: Two columns for input sections
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("📂 Step 1: Upload Resume")
        uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"], help="Supports standard PDF resumes.")
        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

    with col2:
        st.subheader("📝 Step 2: Job Description")
        job_description = st.text_area("Paste the requirements", height=200, placeholder="Paste the job requirements, skills, and description here...")

    st.markdown("<br>", unsafe_allow_headers=True)

    # Center column for the action button
    _, btn_col, _ = st.columns([1, 1.5, 1])
    with btn_col:
        submit = st.button("🎯 CALCULATE MATCH SCORE")

    if submit:
        if uploaded_file is not None and job_description.strip() != "":
            # Animation: Status bar and loading messages
            with st.status("🔍 Analyzing Document Alignment...", expanded=True) as status:
                st.write("Extracting text from PDF...")
                resume_text = pdf_reader.get_pdf_text(uploaded_file)
                
                if not resume_text.strip():
                    st.error("Error: Could not extract text. The PDF might be a scanned image or empty.")
                    status.update(label="Analysis Failed", state="error")
                    return

                st.write("Cleaning and Pre-processing contents...")
                cleaned_resume = text_cleaner.clean_text(resume_text)
                cleaned_jd = text_cleaner.clean_text(job_description)
                time.sleep(0.6) # Small delay for visual effect

                st.write("Calculating Cosine Similarity using TF-IDF...")
                score = ats_score.get_ats_score(cleaned_resume, cleaned_jd)
                time.sleep(0.6)
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)

            # Results UI Card
            st.markdown(f"""
            <div class='score-container'>
                <h3>Your ATS Match Score</h3>
                <div class='score-text'>{score}%</div>
            </div>
            """, unsafe_allow_headers=True)
            
            # Progress bar for visual feedback
            st.progress(score / 100)

            # Dynamic Feedback based on score
            if score >= 80:
                st.balloons() # Animation for high score
                st.success("🔥 **Outstanding!** Your resume is a fantastic match for this role. You are ready to apply!")
            elif score >= 60:
                st.info("✨ **Good Match.** You have the core skills. Try adding a few more specific keywords from the JD to improve your ranking.")
            elif score >= 40:
                st.warning("⚠️ **Moderate Match.** Your resume matches some key areas but needs more alignment with the specific skills mentioned.")
            else:
                st.error("📉 **Low Match.** We recommend tailoring your resume significantly to include more relevant keywords and technologies.")

            # Details Expander
            with st.expander("📊 View Detailed Keyword Preview"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Processed Resume Content:**")
                    st.caption(cleaned_resume[:800] + "...")
                with c2:
                    st.markdown("**Processed JD Content:**")
                    st.caption(cleaned_jd[:800] + "...")
        else:
            st.error("⚠️ Please provide both a Resume and a Job Description to begin the analysis.")

if __name__ == '__main__':
    main()
