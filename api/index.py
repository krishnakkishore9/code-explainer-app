import os
import sys

# Add the project root to the path so we can import app.py if needed
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def handler(event, context):
    """
    Vercel Serverless Function entry point.
    Note: Deploying Streamlit on Vercel is highly experimental.
    Streamlit usually requires a persistent WebSocket connection which
    Serverless Functions do not natively support for long periods.
    """
    return {
        "statusCode": 200,
        "body": "Streamlit app entry point. Please note: Streamlit is best hosted on Streamlit Community Cloud or Hugging Face Spaces for persistent sessions."
    }
