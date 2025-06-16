import numpy as np
import streamlit as st
import asyncio
import os
import json
import re
import random
from typing import Dict, Tuple, List, Optional

# Try to import OpenCV, but create fallbacks if not available
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# Try to import OpenAI - we'll handle missing cases
try:
    import openai
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Set OpenAI API key from .env file, environment variables, or Streamlit secrets
def get_openai_api_key() -> Optional[str]:
    try:
        # Try to load from .env file
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        load_dotenv(dotenv_path=env_path)
    except ImportError:
        st.warning("python-dotenv not installed. Install with 'pip install python-dotenv' to use .env files.")
    
    # Try all possible sources for API key
    if 'OPENAI_API_KEY' in os.environ:
        return os.environ['OPENAI_API_KEY']
    elif 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    else:
        return None

def estimate_bp_from_frame(frame):
    """
    Estimate blood pressure from a video frame
    Uses advanced image processing (simulated for demo)
    
    Args:
        frame: Video frame from webcam
        
    Returns:
        Tuple of (systolic, diastolic) blood pressure values
    """
    if frame is None:
        raise ValueError("Frame is null.")
    
    if not OPENCV_AVAILABLE:
        # Fallback if OpenCV is not available - generate "realistic" random values
        st.warning("OpenCV not available. Using simulated blood pressure values.")
        base_systolic = 120
        base_diastolic = 80
        variation = random.uniform(-15, 15)
        systolic = int(base_systolic + variation)
        diastolic = int(base_diastolic + variation * 0.7)
        
        # Ensure values are in reasonable ranges
        systolic = max(min(systolic, 190), 90)
        diastolic = max(min(diastolic, 110), 60)
        
        return systolic, diastolic
    
    try:
        # In a real application, this would use a trained ML model
        # Here we're simulating with a more sophisticated approach than just random
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        avg_pixel_val = np.mean(gray)
        
        # Use the average pixel value to generate "realistic" BP values
        base_systolic = 120
        base_diastolic = 80
        
        # Create variation based on image brightness
        systolic = int(base_systolic + (avg_pixel_val - 128) / 12)
        diastolic = int(base_diastolic + (avg_pixel_val - 128) / 18)
        
        # Ensure values are in reasonable ranges
        systolic = max(min(systolic, 190), 90)
        diastolic = max(min(diastolic, 110), 60)
        
        return systolic, diastolic
    except Exception as e:
        # Fallback if anything fails with OpenCV processing
        st.warning(f"Error processing image with OpenCV: {str(e)}. Using simulated values.")
        systolic = random.randint(100, 140)
        diastolic = random.randint(65, 90)
        return systolic, diastolic

# Function to classify blood pressure
def classify_blood_pressure(systolic: int, diastolic: int) -> Dict:
    """
    Classify blood pressure based on systolic and diastolic values
    
    Args:
        systolic: Systolic blood pressure value
        diastolic: Diastolic blood pressure value
    
    Returns:
        Dictionary containing classification and color code
    """
    if systolic < 90 or diastolic < 60:
        return {
            "category": "Low Blood Pressure",
            "description": "Your blood pressure is below the normal range.",
            "class": "bp-low",
            "color": "blue",
            "risk_level": "low to moderate",
            "alert": False
        }
    elif systolic < 120 and diastolic < 80:
        return {
            "category": "Normal",
            "description": "Your blood pressure is within the normal range.",
            "class": "bp-normal",
            "color": "green",
            "risk_level": "low",
            "alert": False
        }
    elif systolic < 130 and diastolic < 80:
        return {
            "category": "Elevated",
            "description": "Your blood pressure is slightly above normal and you may be at risk of developing hypertension.",
            "class": "bp-elevated",
            "color": "yellow",
            "risk_level": "moderate",
            "alert": False
        }
    elif systolic < 140 or diastolic < 90:
        return {
            "category": "Hypertension Stage 1",
            "description": "Your blood pressure is high. Lifestyle changes are recommended.",
            "class": "bp-high",
            "color": "orange",
            "risk_level": "moderate to high",
            "alert": True
        }
    elif systolic < 180 or diastolic < 120:
        return {
            "category": "Hypertension Stage 2",
            "description": "Your blood pressure is very high. Consult a doctor as soon as possible.",
            "class": "bp-high",
            "color": "red",
            "risk_level": "high",
            "alert": True
        }
    else:
        return {
            "category": "Hypertensive Crisis",
            "description": "Your blood pressure is extremely high. Seek emergency medical attention immediately!",
            "class": "bp-crisis",
            "color": "darkred",
            "risk_level": "very high",
            "alert": True
        }

def generate_tips(age, diet, salt_intake, exercise, smoker, alcohol, prev_conditions, systolic=None, diastolic=None):
    """
    Generate basic health tips based on user inputs and blood pressure
    
    Args:
        Various user health parameters and blood pressure readings
        
    Returns:
        List of health tips
    """
    tips = []
    if age > 50:
        tips.append("You're over 50. Regular BP checks are important.")
    if diet == "Unhealthy":
        tips.append("Improve your diet with more whole foods.")
    if salt_intake == "High":
        tips.append("Lower your salt intake.")
    if exercise in ["Rarely", "Never"]:
        tips.append("Try exercising at least 3x a week.")
    if smoker == "Yes":
        tips.append("Quit smoking to help manage BP.")
    if alcohol == "Yes":
        tips.append("Reduce alcohol intake.")
    if "Hypertension" in prev_conditions:
        tips.append("Follow your doctor's guidance for high BP.")
    if systolic and diastolic:
        if systolic > 140 or diastolic > 90:
            tips.append("High BP detected. Consult a doctor.")
        elif systolic < 90 or diastolic < 60:
            tips.append("Low BP detected. Monitor for dizziness.")
        else:
            tips.append("Your BP is in the normal range.")
    tips.append("Always consult a healthcare professional if symptoms worsen.")
    return tips

async def get_openai_recommendations(bp_data: Dict, user_info: Dict) -> Dict:
    """
    Get personalized health recommendations using OpenAI
    
    Args:
        bp_data: Blood pressure data including category and risk level
        user_info: User information from questionnaire
    
    Returns:
        Dictionary containing diet, exercise, and lifestyle recommendations
    """
    if not OPENAI_AVAILABLE:
        return {
            "error": "OpenAI library not installed. Please install it with 'pip install openai'.",
            "diet": [],
            "exercise": [],
            "lifestyle": []
        }
    
    api_key = get_openai_api_key()
    
    if not api_key:
        return {
            "error": "OpenAI API key not found. Please add it to your environment variables or Streamlit secrets.",
            "diet": [],
            "exercise": [],
            "lifestyle": []
        }
    
    client = AsyncOpenAI(api_key=api_key)
    
    # Prepare user information for the prompt
    age = user_info.get("age", "unknown age")
    gender = user_info.get("gender", "unspecified gender")
    weight = user_info.get("weight", "unknown weight")
    height = user_info.get("height", "unknown height")
    medical_conditions = user_info.get("medical_conditions", [])
    medications = user_info.get("medications", [])
    activity_level = user_info.get("activity_level", "moderate")
    diet = user_info.get("diet", "not specified")
    
    medical_conditions_str = ", ".join(medical_conditions) if medical_conditions else "none"
    medications_str = ", ".join(medications) if medications else "none"
    
    # Create the prompt for OpenAI
    prompt = f"""
    As a medical nutrition and exercise expert, provide personalized recommendations for a {age} year old {gender} 
    with {bp_data['category']} blood pressure (risk level: {bp_data['risk_level']}). 
    
    Additional information:
    - Height: {height}
    - Weight: {weight}
    - Current diet: {diet}
    - Medical conditions: {medical_conditions_str}
    - Current medications: {medications_str}
    - Activity level: {activity_level}
    
    Please provide specific recommendations in these three areas:
    
    1. Diet recommendations: Include specific foods to eat and avoid, meal planning suggestions, and any dietary approaches specifically beneficial for their blood pressure category.
    
    2. Exercise recommendations: Include specific types of exercises, duration, frequency, and intensity level appropriate for their condition.
    
    3. Lifestyle modifications: Include stress management techniques, sleep recommendations, and other lifestyle changes that could help manage their blood pressure.
    
    Format your response as a JSON object with keys 'diet', 'exercise', and 'lifestyle', each containing a list of 3-5 specific recommendations.
    """
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical expert specializing in cardiovascular health, nutrition, and exercise physiology."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract response
        result_text = response.choices[0].message.content
        
        # Parse JSON from the response
        # Find JSON content between triple backticks if present
        json_match = re.search(r'```json\n([\s\S]*?)\n```', result_text)
        if json_match:
            result_text = json_match.group(1)
        
        try:
            recommendations = json.loads(result_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, use regex to extract sections
            diet_match = re.search(r'"diet":\s*\[(.*?)\]', result_text, re.DOTALL)
            exercise_match = re.search(r'"exercise":\s*\[(.*?)\]', result_text, re.DOTALL)
            lifestyle_match = re.search(r'"lifestyle":\s*\[(.*?)\]', result_text, re.DOTALL)
            
            diet = diet_match.group(1).split('",') if diet_match else []
            exercise = exercise_match.group(1).split('",') if exercise_match else []
            lifestyle = lifestyle_match.group(1).split('",') if lifestyle_match else []
            
            # Clean up the items
            diet = [item.strip().strip('"') for item in diet]
            exercise = [item.strip().strip('"') for item in exercise]
            lifestyle = [item.strip().strip('"') for item in lifestyle]
            
            recommendations = {
                "diet": diet,
                "exercise": exercise,
                "lifestyle": lifestyle
            }
        
        return recommendations
        
    except Exception as e:
        return {
            "error": str(e),
            "diet": [],
            "exercise": [],
            "lifestyle": []
        }

# Fallback function for when OpenAI is not available
def get_default_recommendations(bp_category: str) -> Dict:
    """
    Get default recommendations based on blood pressure category
    
    Args:
        bp_category: Blood pressure category
    
    Returns:
        Dictionary containing diet, exercise, and lifestyle recommendations
    """
    recommendations = {
        "Low Blood Pressure": {
            "diet": [
                "Increase salt intake slightly",
                "Stay hydrated with plenty of fluids",
                "Eat smaller, more frequent meals",
                "Include more high-carbohydrate foods",
                "Add more B-vitamins like B12 and folic acid"
            ],
            "exercise": [
                "Start with gentle exercises like walking",
                "Avoid sudden changes in posture",
                "Incorporate strength training gradually",
                "Try recumbent exercises like cycling",
                "Stay hydrated during workouts"
            ],
            "lifestyle": [
                "Rise slowly from sitting or lying down",
                "Avoid prolonged standing",
                "Wear compression stockings",
                "Limit alcohol consumption",
                "Consider elevating the head of your bed"
            ]
        },
        "Normal": {
            "diet": [
                "Maintain a balanced diet with plenty of fruits and vegetables",
                "Keep sodium intake moderate",
                "Stay hydrated with water",
                "Include potassium-rich foods like bananas and avocados",
                "Consume healthy fats like olive oil and avocados"
            ],
            "exercise": [
                "Aim for 150 minutes of moderate activity weekly",
                "Include both cardio and strength training",
                "Try activities like walking, swimming, or cycling",
                "Practice yoga for flexibility and stress reduction",
                "Take active breaks throughout the day"
            ],
            "lifestyle": [
                "Maintain a healthy sleep schedule",
                "Practice stress management techniques",
                "Limit alcohol and avoid tobacco",
                "Monitor your blood pressure regularly",
                "Stay socially connected"
            ]
        },
        "Elevated": {
            "diet": [
                "Follow the DASH diet (Dietary Approaches to Stop Hypertension)",
                "Reduce sodium intake to less than 2,300mg daily",
                "Increase potassium intake through fruits and vegetables",
                "Limit processed foods and added sugars",
                "Consider using herbs and spices instead of salt"
            ],
            "exercise": [
                "Aim for 30 minutes of moderate exercise most days",
                "Focus on aerobic activities like brisk walking",
                "Try interval training for efficiency",
                "Add 2-3 days of strength training weekly",
                "Monitor your heart rate during exercise"
            ],
            "lifestyle": [
                "Practice deep breathing or meditation daily",
                "Limit alcohol to 1 drink daily for women, 2 for men",
                "Quit smoking and avoid secondhand smoke",
                "Monitor your blood pressure at home regularly",
                "Maintain a healthy weight"
            ]
        },
        "Hypertension Stage 1": {
            "diet": [
                "Follow the DASH diet strictly",
                "Reduce sodium intake to 1,500mg daily",
                "Increase consumption of fruits, vegetables, and whole grains",
                "Limit red meat and increase lean proteins",
                "Consider a Mediterranean diet approach"
            ],
            "exercise": [
                "Consult with a doctor before starting an exercise program",
                "Begin with 10-15 minutes of daily walking",
                "Gradually increase to 30-45 minutes most days",
                "Include regular strength training",
                "Try low-impact activities like swimming"
            ],
            "lifestyle": [
                "Practice stress reduction techniques daily",
                "Get 7-8 hours of quality sleep nightly",
                "Monitor your blood pressure daily",
                "Limit caffeine intake",
                "Consider working with a healthcare provider on a management plan"
            ]
        },
        "Hypertension Stage 2": {
            "diet": [
                "Work with a dietitian on a personalized eating plan",
                "Strictly limit sodium to less than 1,500mg daily",
                "Focus on plant-based foods",
                "Avoid processed foods completely",
                "Consider the DASH or Mediterranean diet under medical supervision"
            ],
            "exercise": [
                "Exercise only under medical supervision",
                "Start with very short (5-10 minute) walking sessions",
                "Focus on gentle movement like tai chi",
                "Avoid high-intensity workouts",
                "Monitor blood pressure before and after activity"
            ],
            "lifestyle": [
                "Take all prescribed medications regularly",
                "Monitor blood pressure multiple times daily",
                "Follow up with healthcare provider regularly",
                "Eliminate alcohol and caffeine",
                "Prioritize stress management and quality sleep"
            ]
        },
        "Hypertensive Crisis": {
            "diet": [
                "Follow strict medical advice on diet",
                "Severe sodium restriction may be necessary",
                "Maintain consistent meal timing",
                "Stay well hydrated",
                "Track all food intake"
            ],
            "exercise": [
                "Do not exercise without medical clearance",
                "Follow specific exercise prescriptions from your doctor",
                "Focus on gentle movement as approved",
                "Monitor blood pressure before, during, and after any activity",
                "Report any symptoms immediately"
            ],
            "lifestyle": [
                "Seek immediate medical attention",
                "Take all prescribed medications exactly as directed",
                "Monitor blood pressure as directed by your physician",
                "Rest and avoid stressful situations",
                "Attend all follow-up appointments"
            ]
        }
    }
    
    return recommendations.get(bp_category, recommendations["Normal"])
