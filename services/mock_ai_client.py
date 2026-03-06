import random
from typing import Any


class MockAiClient:
    """Mock implementation of the AI image analysis API client.

    Simulates POST requests to http://example.com/ with an image_path payload.
    Returns a success response with probability 0.8, otherwise an error response.
    """

    SUCCESS_PROBABILITY: float = 0.8
    ERROR_MESSAGE: str = "Error:E50012"

    def analyze(self, image_path: str) -> dict[str, Any]:
        """Send an image path to the mock AI API and return the response.

        Args:
            image_path: The file path of the image to analyze.

        Returns:
            A dict containing:
                - is_success (bool): Whether the analysis succeeded.
                - message (str): "success" or an error code.
                - estimated_data (dict): class_label and confidence if successful.
        """
        if not image_path or not image_path.strip():
            return {
                "is_success": False,
                "message": self.ERROR_MESSAGE,
                "estimated_data": {},
            }

        if random.random() < self.SUCCESS_PROBABILITY:
            return {
                "is_success": True,
                "message": "success",
                "estimated_data": {
                    "class_label": random.randint(0, 9),
                    "confidence": round(random.uniform(0.5, 0.9999), 4),
                },
            }

        return {
            "is_success": False,
            "message": self.ERROR_MESSAGE,
            "estimated_data": {},
        }
