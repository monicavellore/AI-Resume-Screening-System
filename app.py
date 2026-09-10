import streamlit as st
from pypdf import PdfReader
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

/* Main background */
.stApp {
    background: #f5f7fb;
}

/* Main content width */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main title */
h1 {
    text-align: center;
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 17px;
    margin-bottom: 35px;
}

/* Section headings */
h2 {
    color: #172554;
    margin-top: 30px;
}

h3 {
    color: #1e293b;
}

/* Cards */
.card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Score card */
.score-card {
    background: white;
    border-radius: 18px;
    padding: 28px;
    text-align: center;
    border: 1px solid #dbeafe;
    box-shadow: 0 5px 20px rgba(0,0,0,0.07);
}

.score {
    font-size: 48px;
    font-weight: 800;
    color: #2563eb;
}

.score-label {
    color: #64748b;
    font-size: 14px;
}

/* Skill badges */
.skill {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    padding: 7px 13px;
    border-radius: 20px;
    margin: 4px;
    font-size: 14px;
    font-weight: 600;
}

.missing {
    display: inline-block;
    background: #fef2f2;
    color: #dc2626;
    padding: 7px 13px;
    border-radius: 20px;
    margin: 4px;
    font-size: 14px;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    font-weight: 700;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 12px;
    padding: 10px;
}

/* Text areas */
textarea {
    border-radius: 10px !important;
}

/* Divider */
hr {
    margin: 30px 0;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CUSTOM CSS - PROFESSIONAL UI
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main container */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        padding: 35px 40px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.18);
    }

    .main-header h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 8px;
        font-weight: 700;
    }

    .main-header p {
        color: #dbeafe;
        font-size: 17px;
        margin: 0;
    }

    /* Section titles */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #172554;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Cards */
    .info-card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        min-height: 130px;
    }

    .info-card h3 {
        margin-top: 0;
        color: #1e3a8a;
        font-size: 18px;
    }

    .info-card p {
        color: #374151;
        font-size: 16px;
    }

    /* Result card */
    .result-card {
        background: white;
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        margin-top: 20px;
    }

    /* Score */
    .score-box {
        text-align: center;
        padding: 20px;
    }

    .score-number {
        font-size: 52px;
        font-weight: 800;
        color: #2563eb;
    }

    .score-label {
        font-size: 16px;
        color: #6b7280;
        font-weight: 600;
    }

    /* Skill pills */
    .skill-pill {
        display: inline-block;
        padding: 8px 13px;
        margin: 5px;
        border-radius: 20px;
        background-color: #dbeafe;
        color: #1e40af;
        font-weight: 600;
        font-size: 14px;
    }

    .missing-pill {
        display: inline-block;
        padding: 8px 13px;
        margin: 5px;
        border-radius: 20px;
        background-color: #fee2e2;
        color: #991b1b;
        font-weight: 600;
        font-size: 14px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 17px;
        font-weight: 700;
    }

    /* Divider */
    .divider {
        height: 1px;
        background-color: #e5e7eb;
        margin: 35px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        margin-top: 40px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">
    <h1>📄 AI Resume Screening System</h1>
    <p>Intelligent Resume Analysis & Job Matching Platform</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTION 1: CHECK WHETHER SKILL EXISTS
# =========================================================

def skill_found(skill, text):

    pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

    return re.search(pattern, text.lower()) is not None


# =========================================================
# FUNCTION 2: EXTRACT INFORMATION FROM RESUME
# =========================================================

def extract_information(resume_text):

    text = resume_text.lower()

    skill_list = [
        "python",
        "java",
        "sql",
        "machine learning",
        "git",
        "github",
        "reactjs",
        "nodejs",
        "tensorflow",
        "c++",
        "c",
        "html",
        "css"
    ]

    found_skills = []

    for skill in skill_list:

        if skill_found(skill, text):
            found_skills.append(skill)

    # -------------------------
    # Education
    # -------------------------

    education = "Not detected"

    education_keywords = [
        "bachelor",
        "master",
        "b.tech",
        "m.tech",
        "computer science",
        "software engineering"
    ]

    for keyword in education_keywords:

        if keyword in text:
            education = keyword.title()
            break

    # -------------------------
    # Experience
    # -------------------------

    experience = "Not detected"

    experience_match = re.search(
        r"(\d+)\s*(?:year|years)\s*(?:of)?\s*(?:experience)?",
        text
    )

    if experience_match:
        experience = experience_match.group(0)

    # -------------------------
    # Projects
    # -------------------------

    projects = "Not detected"

    if "project" in text:
        projects = "Project information detected"

    return found_skills, education, experience, projects


# =========================================================
# FUNCTION 3: EXTRACT SKILLS FROM JOB DESCRIPTION
# =========================================================

def extract_jd_skills(job_description):

    text = job_description.lower()

    skill_list = [
        "python",
        "java",
        "sql",
        "machine learning",
        "git",
        "github",
        "reactjs",
        "nodejs",
        "tensorflow",
        "c++",
        "c",
        "html",
        "css"
    ]

    jd_skills = []

    for skill in skill_list:

        if skill_found(skill, text):
            jd_skills.append(skill)

    return jd_skills


# =========================================================
# FUNCTION 4: CALCULATE MATCHING SCORE
# =========================================================

def calculate_matching_score(resume_skills, jd_skills):

    if not jd_skills:
        return 0, [], []

    matched_skills = []
    missing_skills = []

    resume_skill_lower = [
        skill.lower() for skill in resume_skills
    ]

    for skill in jd_skills:

        if skill.lower() in resume_skill_lower:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    score = (
        len(matched_skills) / len(jd_skills)
    ) * 100

    return score, matched_skills, missing_skills


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📥 Resume & Job Details</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# =========================================================
# RESUME UPLOAD
# =========================================================

with col1:

    st.markdown("""
    <div class="info-card">
        <h3>📄 Resume Upload</h3>
        <p>Upload a candidate resume in PDF format.</p>
    </div>
    """, unsafe_allow_html=True)

    resume = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )


# =========================================================
# JOB DESCRIPTION
# =========================================================

with col2:

    st.markdown("""
    <div class="info-card">
        <h3>💼 Job Description</h3>
        <p>Enter the requirements for the target position.</p>
    </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area(
        "Job Description",
        height=160,
        placeholder="""Example:

Python Developer

Required Skills:
Python, Java, SQL, Machine Learning,
Git, GitHub, ReactJS, NodeJS

Education:
Bachelor's degree in Computer Science.

Experience:
1-2 years of software development experience.""",
        label_visibility="collapsed"
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.write("")

analyze = st.button(
    "🔍  Analyze Resume",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if resume is None:

        st.warning("⚠️ Please upload a resume PDF.")

    elif not job_description.strip():

        st.warning("⚠️ Please enter a job description.")

    else:

        # =================================================
        # READ PDF
        # =================================================

        try:

            reader = PdfReader(resume)

            resume_text = ""

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:
                    resume_text += extracted + "\n"

        except Exception as e:

            st.error("❌ Unable to read the uploaded PDF.")

            st.stop()


        # =================================================
        # CHECK EXTRACTED TEXT
        # =================================================

        if not resume_text.strip():

            st.error(
                "❌ No readable text was extracted from the PDF."
            )

            st.stop()


        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        st.success(
            f"✅ Resume uploaded and parsed successfully! "
            f"Characters extracted: {len(resume_text)}"
        )


        # =================================================
        # NLP INFORMATION EXTRACTION
        # =================================================

        skills, education, experience, projects = (
            extract_information(resume_text)
        )


        # =================================================
        # EXTRACT JD SKILLS
        # =================================================

        jd_skills = extract_jd_skills(
            job_description
        )


        # =================================================
        # MATCHING
        # =================================================

        if jd_skills:

            score, matched_skills, missing_skills = (
                calculate_matching_score(
                    skills,
                    jd_skills
                )
            )

        else:

            score = 0
            matched_skills = []
            missing_skills = []


        # =================================================
        # CANDIDATE INFORMATION
        # =================================================

        st.markdown(
            '<div class="section-title">🧠 Candidate Information</div>',
            unsafe_allow_html=True
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.markdown(f"""
            <div class="info-card">
                <h3>🔧 Skills</h3>
                <p>{len(skills)} skills detected</p>
            </div>
            """, unsafe_allow_html=True)

        with info2:

            st.markdown(f"""
            <div class="info-card">
                <h3>🎓 Education</h3>
                <p>{education}</p>
            </div>
            """, unsafe_allow_html=True)

        with info3:

            st.markdown(f"""
            <div class="info-card">
                <h3>💼 Experience</h3>
                <p>{experience}</p>
            </div>
            """, unsafe_allow_html=True)


        # =================================================
        # SKILLS SECTION
        # =================================================

        st.markdown(
            '<div class="section-title">🔧 Extracted Skills</div>',
            unsafe_allow_html=True
        )

        if skills:

            skill_html = ""

            for skill in skills:

                skill_html += (
                    f'<span class="skill-pill">'
                    f'{skill.title()}'
                    f'</span>'
                )

            st.markdown(
                skill_html,
                unsafe_allow_html=True
            )

        else:

            st.info("No recognized skills detected.")


        # =================================================
        # MATCHING RESULT
        # =================================================

        st.markdown(
            '<div class="divider"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">📊 Resume–Job Matching</div>',
            unsafe_allow_html=True
        )


        if jd_skills:

            # =================================================
            # SCORE
            # =================================================

            score_col1, score_col2 = st.columns([1, 2])

            with score_col1:

                st.markdown(f"""
                <div class="result-card">
                    <div class="score-box">
                        <div class="score-number">
                            {score:.1f}%
                        </div>
                        <div class="score-label">
                            Overall Match Score
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with score_col2:

                st.write("")

                st.progress(
                    int(score)
                )

                st.write(
                    f"**{len(matched_skills)} of "
                    f"{len(jd_skills)} required skills matched**"
                )


            # =================================================
            # MATCHED + MISSING
            # =================================================

            match_col, missing_col = st.columns(2)


            # -------------------------
            # MATCHED
            # -------------------------

            with match_col:

                st.markdown(
                    "### ✅ Matched Skills"
                )

                if matched_skills:

                    matched_html = ""

                    for skill in matched_skills:

                        matched_html += (
                            f'<span class="skill-pill">'
                            f'✓ {skill.title()}'
                            f'</span>'
                        )

                    st.markdown(
                        matched_html,
                        unsafe_allow_html=True
                    )

                else:

                    st.info(
                        "No matching skills found."
                    )


            # -------------------------
            # MISSING
            # -------------------------

            with missing_col:

                st.markdown(
                    "### ❌ Missing Skills"
                )

                if missing_skills:

                    missing_html = ""

                    for skill in missing_skills:

                        missing_html += (
                            f'<span class="missing-pill">'
                            f'✕ {skill.title()}'
                            f'</span>'
                        )

                    st.markdown(
                        missing_html,
                        unsafe_allow_html=True
                    )

                else:

                    st.success(
                        "No missing skills!"
                    )


        else:

            st.warning(
                "⚠️ No recognized skills found in the Job Description."
            )


        # =================================================
        # RESUME TEXT
        # =================================================

        st.markdown(
            '<div class="divider"></div>',
            unsafe_allow_html=True
        )

        with st.expander(
            "📄 View Extracted Resume Text"
        ):

            st.text_area(
                "Resume Content",
                value=resume_text,
                height=300,
                label_visibility="collapsed"
            )


        # =================================================
        # JOB DESCRIPTION
        # =================================================

        with st.expander(
            "💼 View Job Description"
        ):

            st.write(
                job_description
            )


        # =================================================
        # PROJECT INFORMATION
        # =================================================

        st.markdown(
            '<div class="section-title">🚀 Additional Information</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="info-card">
            <h3>🚀 Projects</h3>
            <p>{projects}</p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    AI Resume Screening System • Resume Analysis • NLP • Job Matching
</div>
""", unsafe_allow_html=True)