import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
try:
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path=env_path)
    # We'll show this in the sidebar later
    env_loaded = True
except ImportError:
    env_loaded = False
except Exception as e:
    env_error = str(e)
    env_loaded = False

# Configure page settings
st.set_page_config(
    page_title="BP Fuel AI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="❤️"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Display environment variable status in sidebar
if 'env_loaded' in locals():
    if env_loaded:
        st.sidebar.success("✅ Environment variables loaded successfully")
    else:
        if 'env_error' in locals():
            st.sidebar.error(f"⚠️ Error loading environment variables: {env_error}")
        else:
            st.sidebar.warning("⚠️ python-dotenv not installed. For .env support, install with 'pip install python-dotenv'")

# Add OpenAI API key status check
if os.environ.get('OPENAI_API_KEY'):
    st.sidebar.success("✅ OpenAI API key found")
else:
    st.sidebar.warning("⚠️ OpenAI API key not found. Please add it to your .env file")

# Create a two-column layout for the header
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=150)

with col2:
    st.markdown("<h1 class='main-title'>❤️ BP Fuel AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Your Personal Blood Pressure Management Assistant</p>", unsafe_allow_html=True)

with col3:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=150)

# Main content area with card-like appearance
# Create a styled container for the welcome message using Streamlit's native components
with st.container():
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("Welcome to BP Fuel AI")
    st.write("""
        Take control of your cardiovascular health with our advanced blood pressure monitoring
        and recommendation system. Our AI-powered application helps you track, analyze, and
        improve your blood pressure with personalized recommendations.
    """)
    
    st.subheader("How to use this app:")
    
    # Using native Streamlit components for the list items
    st.write("1️⃣ **📝 Questionnaire** - Fill out a simple health questionnaire")
    st.write("2️⃣ **📷 Webcam or Upload** - Use your webcam or upload an image for blood pressure detection")
    st.write("3️⃣ **💡 Health Recommendations** - Get AI-powered personalized diet and exercise recommendations")
      # Add buttons to navigate directly to each section
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Start Questionnaire", use_container_width=True, type="primary"):
            # Navigate to questionnaire page
            import streamlit as st_inner
            st_inner.switch_page("pages/1_📝_Questionnaire.py")
    with col2:
        if st.button("📷 Blood Pressure Detection", use_container_width=True, type="primary"):
            import streamlit as st_inner
            st_inner.switch_page("pages/2_📷_Webcam_or_Upload.py")
    with col3:
        if st.button("💡 Get Recommendations", use_container_width=True, type="primary"):
            import streamlit as st_inner
            st_inner.switch_page("pages/3_💡_Health_Recommendations.py")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Testimonials section with multiple columns
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

# Information section
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
        <div class="fact-content">< 90/60 mmHg</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>BP Fuel AI - Your Personal Blood Pressure Management Assistant © 2025</p>
</div>
""", unsafe_allow_html=True)
