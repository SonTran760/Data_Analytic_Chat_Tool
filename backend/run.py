"""
Application startup script.
Run the FastAPI application with Uvicorn.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from src.utils import get_settings


def main():
    """Start the application."""
    settings = get_settings()
    
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    print(f"Debug: {settings.DEBUG}")
    print("-" * 50)
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()
