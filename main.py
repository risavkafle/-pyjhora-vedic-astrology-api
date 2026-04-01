"""
Cloud Function entry point.
"""
# This file makes the FastAPI app in `app/main.py` discoverable by Google Cloud Functions.
# The deployment command should specify 'app' as the entry point, and Cloud Functions
# will automatically find the 'app' object defined in `app.main` and imported here.
from app.main import app
