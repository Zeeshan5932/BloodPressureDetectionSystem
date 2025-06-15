import os
import sys
import streamlit as st

# Add the bp_app directory to the path
bp_app_path = os.path.join(os.path.dirname(__file__), "bp_app")
sys.path.append(bp_app_path)

# Change directory to bp_app so relative imports work properly
os.chdir(bp_app_path)

# Import and run the main app
try:
    # Use more direct approach by importing main instead of exec
    import main
except ImportError as e:
    st.error(f"Error importing main app: {e}")
    st.info("Please check that all dependencies are installed correctly via requirements.txt")
except Exception as e:
    st.error(f"Error running the application: {e}")
