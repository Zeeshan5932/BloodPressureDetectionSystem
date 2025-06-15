# BloodPressureDetectionSystem


A Streamlit application that estimates blood pressure using computer vision and provides AI-powered personalized health recommendations.

## Features

- Webcam-based blood pressure estimation
- Comprehensive health questionnaire
- AI-powered personalized health recommendations using OpenAI
- Interactive and modern user interface
- Educational blood pressure information
- Health tracking tools

## Requirements

- Python 3.x
- OpenCV
- Streamlit
- NumPy
- OpenAI API key
- python-dotenv

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Create a `.env` file in the `blood pressure` directory
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Usage

1. Run the Streamlit app:
   ```bash
   cd "blood pressure"
   streamlit run bp_app/main.py
   ```
2. Navigate through the application:
   - Fill out the health questionnaire
   - Get your blood pressure reading using webcam or by uploading an image
   - View personalized AI-generated health recommendations
3. Allow webcam access when prompted

## Disclaimer

This app is for demonstration purposes only and does not provide medical advice.
