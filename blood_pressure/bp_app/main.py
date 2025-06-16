import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
env_loaded = load_dotenv(dotenv_path=env_path)

# Check for required variable
openai_key_found = bool(os.getenv("OPENAI_API_KEY"))
env_error = None
if not env_loaded:
    env_error = ".env file not found or failed to load."
elif not openai_key_found:
    env_error = "OPENAI_API_KEY not found in .env file."

# Configure page
st.set_page_config(
    page_title="BP Fuel AI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="❤️"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Custom CSS not found at: assets/styles.css")

# Sidebar feedback
if env_loaded and openai_key_found:
    st.sidebar.success("✅ Environment loaded successfully")
    st.sidebar.success("✅ OpenAI API key found")
else:
    st.sidebar.error(f"⚠️ {env_error}")

# Header layout
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=150)
with col2:
    st.markdown("<h1 class='main-title'>❤️ BP Fuel AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Your Personal Blood Pressure Management Assistant</p>", unsafe_allow_html=True)
with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=150)

# Main section
with st.container():
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("Welcome to BP Fuel AI")
    st.write("""
        Take control of your cardiovascular health with our advanced blood pressure monitoring
        and recommendation system. Our AI-powered application helps you track, analyze, and
        improve your blood pressure with personalized recommendations.
    """)
    st.subheader("How to use this app:")
    st.write("1️⃣ **📝 Questionnaire** - Fill out a simple health questionnaire")
    st.write("2️⃣ **📷 Webcam or Upload** - Use your webcam or upload an image for blood pressure detection")
    st.write("3️⃣ **💡 Health Recommendations** - Get AI-powered personalized diet and exercise recommendations")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Start Questionnaire", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📝_Questionnaire.py")
    with col2:
        if st.button("📷 Blood Pressure Detection", use_container_width=True, type="primary"):
            st.switch_page("pages/2_📷_Webcam_or_Upload.py")
    with col3:
        if st.button("💡 Get Recommendations", use_container_width=True, type="primary"):
            st.switch_page("pages/3_💡_Health_Recommendations.py")

    st.markdown("</div>", unsafe_allow_html=True)

# Testimonials
st.markdown("<h2 class='section-header'>What Our Users Say</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-content">
            "This app has completely changed how I manage my blood pressure. The personalized recommendations are spot on!"
        </div>
        <div class="testimonial-author">- Maria S., 56</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-content">
            "I've been struggling with high blood pressure for years. This AI assistant has given me practical steps that actually work."
        </div>
        <div class="testimonial-author">- James T., 62</div>
    </div>
    """, unsafe_allow_html=True)

# Facts
st.markdown("<h2 class='section-header'>Blood Pressure Facts</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="fact-card">
        <div class="fact-header">Normal BP</div>
        <div class="fact-content">120/80 mmHg</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="fact-card">
        <div class="fact-header">Hypertension</div>
        <div class="fact-content">≥ 130/80 mmHg</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="fact-card">
        <div class="fact-header">Low Blood Pressure</div>
        <div class="fact-content">&lt; 90/60 mmHg</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>BP Fuel AI - Your Personal Blood Pressure Management Assistant © 2025</p>
</div>
""", unsafe_allow_html=True)
