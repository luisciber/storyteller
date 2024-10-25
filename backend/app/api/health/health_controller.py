from fastapi import APIRouter
from app.api.health.health_service import HealthService
from app.api.health.health_dto import HealthCheckResponse

router = APIRouter()
health_service = HealthService()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    return health_service.check_health()
