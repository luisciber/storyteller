from app.api.health.health_dto import HealthCheckResponse

class HealthService:
    def check_health(self) -> HealthCheckResponse:
        return HealthCheckResponse(status="UP")
