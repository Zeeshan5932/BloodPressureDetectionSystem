import streamlit as st

st.set_page_config(
    page_title="Questionnaire - BP Fuel AI",
    page_icon="📝",
    layout="wide"
)

# Load custom CSS
import os
css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📝 Health Questionnaire</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Help us understand your health better</p>", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <h2>Why This Information Matters</h2>
    <p>
        Your answers help our AI provide more accurate blood pressure analysis and personalized health recommendations. 
        All information is kept private and used only to improve your results.
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("questionnaire_form"):
    st.markdown("<h3>Personal Information</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    
    col1, col2 = st.columns(2)
    with col1:
        height_unit = st.selectbox("Height Unit", ["cm", "ft/in"])
        if height_unit == "cm":
            height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
            height_value = f"{height} cm"
        else:
            height_ft = st.number_input("Height (ft)", min_value=1, max_value=8, value=5)
            height_in = st.number_input("Height (in)", min_value=0, max_value=11, value=8)
            height_value = f"{height_ft}'{height_in}\""
    
    with col2:
        weight_unit = st.selectbox("Weight Unit", ["kg", "lb"])
        if weight_unit == "kg":
            weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
            weight_value = f"{weight} kg"
        else:
            weight = st.number_input("Weight (lb)", min_value=45, max_value=660, value=155)
            weight_value = f"{weight} lb"
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Lifestyle Information</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        diet = st.selectbox("Diet Quality", ["Excellent", "Good", "Average", "Poor", "Very Poor"])
        salt_intake = st.selectbox("Salt Intake", ["Low", "Moderate", "High", "Very High"])
    
    with col2:
        exercise = st.selectbox("Exercise Frequency", ["Daily", "4-6 times a week", "2-3 times a week", "Once a week", "Rarely", "Never"])
        sleep = st.selectbox("Average Sleep per Night", ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        smoker = st.radio("Do you smoke?", ["Yes", "No", "Former smoker"])
    with col2:
        alcohol = st.radio("Alcohol consumption?", ["None", "Occasional", "Regular", "Heavy"])
    with col3:
        stress = st.radio("Stress levels?", ["Low", "Moderate", "High", "Very high"])
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Medical Information</h3>", unsafe_allow_html=True)
    
    prev_conditions = st.multiselect("Medical Conditions (select all that apply)", 
                                    ["None", "Hypertension", "Diabetes", "Heart Disease", "Stroke", 
                                     "Kidney Disease", "High Cholesterol", "Obesity", "Thyroid Problems"])
    
    medications = st.multiselect("Medications (select all that apply)",
                                ["None", "Blood Pressure Medication", "Cholesterol Medication", 
                                 "Diabetes Medication", "Heart Medication", "Anticoagulants",
                                 "Diuretics", "Other"])
    
    family_history = st.multiselect("Family History of (select all that apply)",
                                    ["None", "Hypertension", "Heart Disease", "Stroke", 
                                     "Diabetes", "Kidney Disease"])
    
    additional_info = st.text_area("Any additional information you'd like to share about your health?", "")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button("Submit Questionnaire", use_container_width=True)

if submitted:
    # Process and clean the data
    if "None" in prev_conditions and len(prev_conditions) > 1:
        prev_conditions.remove("None")
    
    if "None" in medications and len(medications) > 1:
        medications.remove("None")
    
    if "None" in family_history and len(family_history) > 1:
        family_history.remove("None")
          # Save to session state
    st.session_state['questionnaire'] = {
        "age": age,
        "gender": gender,
        "height": height_value,
        "weight": weight_value,
        "diet": diet,
        "salt_intake": salt_intake,
        "exercise": exercise,
        "sleep": sleep,
        "smoker": smoker,
        "alcohol": alcohol,
        "stress": stress,
        "prev_conditions": prev_conditions,
        "medications": medications,
        "family_history": family_history,
        "additional_info": additional_info
    }
    
    st.success("✅ Questionnaire completed successfully!")
    st.balloons()
    
    st.info("**Next step:** Proceed to the Webcam or Upload page to measure your blood pressure.")
      # Use Streamlit's native button for better functionality
    if st.button("Continue to Blood Pressure Detection →", use_container_width=True, type="primary"):
        # Navigate to the next page using Streamlit's switch_page function
        import streamlit as st_inner
        st_inner.switch_page("pages/2_📷_Webcam_or_Upload.py")
