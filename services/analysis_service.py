"""Service layer for AI image analysis business logic."""

from datetime import datetime

from models.ai_analysis_log import AiAnalysisLog
from repositories.ai_analysis_log_repository import AiAnalysisLogRepository
from services.mock_ai_client import MockAiClient


class AnalysisService:
    """Facade that orchestrates image analysis: API call, log creation, and persistence.

    Args:
        client: An AI API client instance.
        repository: A repository instance for persisting logs.
    """

    def __init__(self, client: MockAiClient, repository: AiAnalysisLogRepository) -> None:
        self._client = client
        self._repository = repository

    def analyze(self, image_path: str) -> dict:
        """Run image analysis and persist the result.

        Args:
            image_path: The file path of the image to analyze.

        Returns:
            A dict containing:
                - log (dict): The persisted log entry as a dictionary.
                - api_response (dict): The raw API response.
        """
        request_timestamp = datetime.now()
        api_response = self._client.analyze(image_path)
        response_timestamp = datetime.now()

        estimated = api_response.get("estimated_data", {})

        log = AiAnalysisLog(
            image_path=image_path if image_path else None,
            is_success=api_response["is_success"],
            message=api_response.get("message"),
            class_label=estimated.get("class_label"),
            confidence=estimated.get("confidence"),
            request_timestamp=request_timestamp,
            response_timestamp=response_timestamp,
        )
        self._repository.save(log)

        return {
            "log": log.to_dict(),
            "api_response": api_response,
        }
