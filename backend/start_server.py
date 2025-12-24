"""
Start script for the Physical AI & Humanoid Robotics Textbook API
"""
import uvicorn
import sys
import os
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Starting Physical AI & Humanoid Robotics Textbook API server...")

    # Check if required environment variables are set
    required_env_vars = [
        "OPENAI_API_KEY",
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "DATABASE_URL",
        "SECRET_KEY"
    ]

    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logger.warning(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.warning("Some features may not work properly without these variables.")

    logger.info("Starting Uvicorn server...")

    uvicorn.run(
        "backend.rag.app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )

if __name__ == "__main__":
    main()