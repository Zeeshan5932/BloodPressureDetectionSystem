"""
OpenCV compatibility module for Streamlit Cloud deployments.
This file provides workarounds for common OpenCV installation issues.
"""

import subprocess
import sys
import importlib
import streamlit as st

def ensure_opencv():
    """
    Try multiple methods to ensure OpenCV is available
    """
    try:
        # First attempt - direct import
        import cv2
        return cv2
    except ImportError:
        # Try to install a specific version
        st.warning("⚠️ OpenCV not available. Attempting to install...")
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "--no-cache-dir", 
                "opencv-python-headless==4.6.0.66"
            ])
            
            # Need to force module reload to recognize new package
            importlib.invalidate_caches()
            
            # Try import again
            try:
                import cv2
                st.success("✅ OpenCV installed successfully!")
                return cv2
            except ImportError:
                st.error("❌ Failed to import OpenCV even after installation")
                raise
        except Exception as e:
            st.error(f"❌ Error installing OpenCV: {str(e)}")
            raise
