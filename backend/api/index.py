"""
Vercel serverless function entry point.
This file is required for Vercel to properly deploy the FastAPI app.
"""

from app.main import create_app

# Create the FastAPI app instance
app = create_app()
