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
    # Execute the main.py file directly
    main_file = os.path.join(bp_app_path, "main.py")
    with open(main_file, "r") as f:
        code = compile(f.read(), main_file, 'exec')
        exec(code, globals())
except Exception as e:
    st.error(f"Error running the application: {e}")
    st.info("Please check that all dependencies are installed correctly via requirements.txt")
