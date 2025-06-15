import streamlit as st
import numpy as np
import tempfile
import os
import sys
import time

# Try to handle OpenCV import with special compatibility module
try:
    from utils.cv2_fix import ensure_opencv
    cv2 = ensure_opencv()
except Exception as e:
    st.error(f"Failed to load OpenCV: {e}")
    # Fallback to direct import as last resort
    try:
        import cv2
    except ImportError:
        st.error("Cannot import OpenCV (cv2). The app may not function correctly.")
        # Create a dummy cv2 module with minimal functionality to prevent complete crashes
        class DummyCV2:
            def __getattr__(self, name):
                return lambda *args, **kwargs: None
        cv2 = DummyCV2()

from utils.bp_utils import estimate_bp_from_frame, classify_blood_pressure

# Add the parent directory to import from utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

st.set_page_config(
    page_title="Blood Pressure Detection - BP Fuel AI",
    page_icon="📷",
    layout="wide"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📷 Blood Pressure Detection</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Capture your facial image to analyze your blood pressure</p>", unsafe_allow_html=True)

# Check if questionnaire was completed
if "questionnaire" not in st.session_state:
    st.warning("Please complete the questionnaire first!")
    st.info("To provide you with accurate blood pressure analysis and personalized recommendations, we need some information about you.")
      # Use a native Streamlit button for better navigation
    if st.button("Go to Questionnaire", use_container_width=True, type="primary"):
        import streamlit as st_inner
        st_inner.switch_page("pages/1_📝_Questionnaire.py")
    st.stop()

# Information about the technology
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

# Create tabs for webcam or upload
tab1, tab2 = st.tabs(["Use Webcam", "Upload Image"])

with tab1:
    st.write("#### Capture Your Image")
    st.write("Position your face in the frame and take a photo.")
    
    camera_image = st.camera_input("", key="webcam_input")
    
    if camera_image:
        with st.spinner("Analyzing your blood pressure..."):
            # Add a small delay to simulate processing
            time.sleep(1.5)
            
            file_bytes = np.asarray(bytearray(camera_image.getvalue()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            # Get BP reading
            s, d = estimate_bp_from_frame(frame)
            st.session_state['bp_result'] = (s, d)
            
            # Get classification
            bp_classification = classify_blood_pressure(s, d)
            
            # Display results
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Captured image for analysis")
            
            with col2:
                st.subheader("Blood Pressure Analysis")
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Systolic", s, delta=None)
                with metric_col2:
                    st.metric("Diastolic", d, delta=None)
                
                st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                {bp_classification['category']}</div>""", unsafe_allow_html=True)
                st.write(bp_classification['description'])
                  # Use Streamlit's native button for navigation
                if st.button("Get Personalized Health Recommendations →", key="webcam_recommend", use_container_width=True, type="primary"):
                    import streamlit as st_inner
                    st_inner.switch_page("pages/3_💡_Health_Recommendations.py")

with tab2:
    st.write("#### Upload an Image")
    st.write("Upload a clear, well-lit photo of your face.")
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "mp4", "avi"], key="file_upload")
    
    if uploaded_file:
        with st.spinner("Analyzing your blood pressure..."):
            # Add a small delay to simulate processing
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
                # Get BP reading
                s, d = estimate_bp_from_frame(frame)
                st.session_state['bp_result'] = (s, d)
                
                # Get classification
                bp_classification = classify_blood_pressure(s, d)
                
                # Display results
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Uploaded image for analysis")
                
                with col2:
                    st.subheader("Blood Pressure Analysis")
                    
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        st.metric("Systolic", s, delta=None)
                    with metric_col2:
                        st.metric("Diastolic", d, delta=None)
                    
                    st.markdown(f"""<div style="color: {bp_classification['color']}; font-weight: bold; font-size: 1.3rem;">
                    {bp_classification['category']}</div>""", unsafe_allow_html=True)
                    st.write(bp_classification['description'])
                      # Use Streamlit's native button for navigation
                    if st.button("Get Personalized Health Recommendations →", key="upload_recommend", use_container_width=True, type="primary"):
                        import streamlit as st_inner
                        st_inner.switch_page("pages/3_💡_Health_Recommendations.py")

# Display how it works at the bottom
st.markdown("<h2 class='section-header'>Understanding the Technology</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Photoplethysmography (PPG)")
    st.write("Our AI analyzes subtle color changes in facial skin that correspond to blood flow patterns, using a technique called PPG.")

with col2:
    st.markdown("### Machine Learning")
    st.write("Our models have been trained on thousands of facial images paired with actual blood pressure readings to provide accurate estimates.")

with col3:
    st.markdown("### Personalization")
    st.write("By combining your questionnaire data with image analysis, we provide more accurate readings tailored to your health profile.")
