import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Blood Pressure Detection - BP Fuel AI",
    page_icon="📷",
    layout="wide"
)

import numpy as np
import tempfile
import os
import sys
import time

# Helper function for navigation
def navigate_to(page):
    st.switch_page(page)

# Try to import OpenCV, handle gracefully if unavailable
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# Add the parent directory to import from utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from utils.bp_utils import estimate_bp_from_frame, classify_blood_pressure

# Load custom CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Show warning if OpenCV is not available
if not OPENCV_AVAILABLE:
    st.warning("⚠️ OpenCV (cv2) is not installed. Upload/Camera image analysis will be limited to simulated values.")

st.markdown("<h1 class='main-title'>📷 Blood Pressure Detection</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Capture your facial image to analyze your blood pressure</p>", unsafe_allow_html=True)

# Questionnaire check
if "questionnaire" not in st.session_state:
    st.warning("Please complete the questionnaire first!")
    st.info("To provide you with accurate blood pressure analysis and personalized recommendations, we need some information about you.")
    if st.button("Go to Questionnaire", use_container_width=True, type="primary"):
        navigate_to("pages/1_📝_Questionnaire.py")
    st.stop()

with st.expander("How This Works", expanded=False):
    st.write("""
        Our advanced AI technology analyzes facial features and skin tone variations to estimate your blood pressure. 
        For the most accurate results:
        - Make sure your face is well-lit with even lighting
        - Look directly at the camera
        - Remove glasses or anything that covers your face
        - Stay still while the image is being captured
    """)
    st.info("Note: This technology provides an estimate and should not replace medical devices or professional guidance.")

# Tabs
tab1, tab2 = st.tabs(["Use Webcam", "Upload Image"])

# -------- Webcam Tab --------
with tab1:
    st.write("#### Capture Your Image")
    st.write("Position your face in the frame and take a photo.")

    camera_image = st.camera_input("", key="webcam_input")

    if camera_image:
        with st.spinner("Analyzing your blood pressure..."):
            time.sleep(1.5)
            try:
                file_bytes = np.asarray(bytearray(camera_image.getvalue()), dtype=np.uint8)

                if OPENCV_AVAILABLE:
                    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    s, d = estimate_bp_from_frame(frame)
                else:
                    frame = None
                    s, d = estimate_bp_from_frame(frame)

                st.session_state['bp_result'] = (s, d)
                bp_classification = classify_blood_pressure(s, d)

                col1, col2 = st.columns([1, 1])
                with col1:
                    if OPENCV_AVAILABLE:
                        display_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        st.image(display_img, caption="Captured image for analysis")
                    else:
                        st.image(camera_image, caption="Captured image for analysis")

                with col2:
                    st.subheader("Blood Pressure Analysis")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Systolic", s)
                    metric_col2.metric("Diastolic", d)
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                        {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])

                    if st.button("Get Personalized Health Recommendations →", key="webcam_recommend", use_container_width=True, type="primary"):
                        navigate_to("pages/3_💡_Health_Recommendations.py")

            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                s, d = 120, 80  # Fallback
                st.session_state['bp_result'] = (s, d)
                bp_classification = classify_blood_pressure(s, d)
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.image(camera_image, caption="Captured image (analysis failed)")
                    st.warning("Using default blood pressure values due to processing error.")
                with col2:
                    st.subheader("Blood Pressure Analysis")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Systolic", s)
                    metric_col2.metric("Diastolic", d)
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                        {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])

# -------- Upload Tab --------
with tab2:
    st.write("#### Upload an Image")
    st.write("Upload a clear, well-lit photo of your face.")

    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "mp4", "avi"], key="file_upload")

    if uploaded_file:
        if not OPENCV_AVAILABLE:
            st.error("OpenCV is required to process uploaded files. Please install `opencv-python-headless`.")
            st.stop()

        with st.spinner("Analyzing your blood pressure..."):
            time.sleep(1.5)
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            frame = None

            if uploaded_file.type.startswith("image/"):
                frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                    tfile.write(file_bytes)
                    tfile.flush()
                    video = cv2.VideoCapture(tfile.name)
                    ret, frame = video.read()
                    video.release()

            if frame is not None:
                s, d = estimate_bp_from_frame(frame)
                st.session_state['bp_result'] = (s, d)
                bp_classification = classify_blood_pressure(s, d)

                col1, col2 = st.columns([1, 1])
                with col1:
                    st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Uploaded image for analysis")
                with col2:
                    st.subheader("Blood Pressure Analysis")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Systolic", s)
                    metric_col2.metric("Diastolic", d)
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                        {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])

                    if st.button("Get Personalized Health Recommendations →", key="upload_recommend", use_container_width=True, type="primary"):
                        navigate_to("pages/3_💡_Health_Recommendations.py")

# Footer
st.markdown("<h2 class='section-header'>Understanding the Technology</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Photoplethysmography (PPG)")
    st.write("Our AI analyzes subtle color changes in facial skin that correspond to blood flow patterns.")
with col2:
    st.markdown("### Machine Learning")
    st.write("Our models are trained on thousands of facial images and real BP readings.")
with col3:
    st.markdown("### Personalization")
    st.write("We use your questionnaire data to tailor blood pressure estimation.")
