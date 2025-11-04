"""
Health check and system status endpoints.
"""
from fastapi import APIRouter, status

from src.services import get_cosmos_service
from src.utils import get_logger, get_settings

router = APIRouter(prefix="/health", tags=["health"])
logger = get_logger(__name__)


@router.get("", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        System health status
    """
    return {"status": "healthy", "service": "Data Analytics Chat Tool"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Readiness check - verify all dependencies are available.
    
    Returns:
        Readiness status with dependency checks
    """
    try:
        settings = get_settings()
        cosmos_service = get_cosmos_service()
        
        # Check Cosmos DB connection
        cosmos_healthy = False
        try:
            # Simple check - try to list databases
            await cosmos_service.cosmos_client.read_all_databases()
            cosmos_healthy = True
        except Exception as e:
            logger.error(f"Cosmos DB health check failed: {e}")
        
        # Overall readiness
        ready = cosmos_healthy
        
        return {
            "status": "ready" if ready else "not_ready",
            "checks": {
                "cosmos_db": "healthy" if cosmos_healthy else "unhealthy",
                "configuration": "healthy"
            }
        }
        
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {
            "status": "not_ready",
            "error": str(e)
        }


@router.get("/info", status_code=status.HTTP_200_OK)
async def system_info():
    """
    Get system information.
    
    Returns:
        System configuration and status
    """
    settings = get_settings()
    
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "llm_providers": {
            "openai": settings.OPENAI_API_KEY is not None,
            "google": settings.GOOGLE_API_KEY is not None,
            "anthropic": settings.ANTHROPIC_API_KEY is not None
        },
        "services": {
            "cosmos_db": settings.COSMOS_DATABASE_NAME,
            "vector_store": settings.VECTOR_STORE_TYPE,
            "rag_enabled": True
        }
    }
