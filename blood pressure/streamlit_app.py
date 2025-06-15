import os
import sys
import streamlit as st

# Add the bp_app directory to the path
bp_app_path = os.path.join(os.path.dirname(__file__), "bp_app")
sys.path.append(bp_app_path)

# Change directory to bp_app so relative imports work properly
os.chdir(bp_app_path)

# Import and run the main app - using exec to run the file directly
with open(os.path.join(bp_app_path, "main.py"), "r") as f:
    exec(f.read())
