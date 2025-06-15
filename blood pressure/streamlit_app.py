import os
import sys
import importlib
import subprocess
import streamlit as st
import time

def install_opencv():
    """Attempt to ensure OpenCV is properly installed"""
    try:
        # Try to import cv2 first
        import cv2
        st.success("OpenCV is already installed correctly")
        return True
    except ImportError:
        st.warning("OpenCV not found. Attempting to install...")
        try:
            # Try to install a specific version known to work on Streamlit Cloud
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "opencv-python-headless==4.6.0.66"])
            st.success("OpenCV installed successfully!")
            # Need to force module reload to recognize the newly installed package
            importlib.invalidate_caches()
            time.sleep(2)  # Give it a moment to complete installation
            return True
        except Exception as e:
            st.error(f"Failed to install OpenCV: {e}")
            return False

# Try to ensure OpenCV is available
install_opencv()

# Add the bp_app directory to the path
bp_app_path = os.path.join(os.path.dirname(__file__), "bp_app")
sys.path.append(bp_app_path)

# Change directory to bp_app so relative imports work properly
os.chdir(bp_app_path)

# Import and run the main app
try:
    import main
except ImportError as e:
    if "cv2" in str(e):
        st.error("OpenCV could not be loaded. Please check deployment logs.")
    else:
        st.error(f"Error importing main app: {e}")
except Exception as e:
    st.error(f"Error running the application: {e}")
