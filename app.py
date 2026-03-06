"""AI Analysis API Client - Flask Application."""

from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_cors import CORS
from models.ai_analysis_log import db
from services.mock_ai_client import MockAiClient
from services.analysis_service import AnalysisService
from repositories.ai_analysis_log_repository import AiAnalysisLogRepository
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'ai_analysis.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

_repo = AiAnalysisLogRepository()
_client = MockAiClient()
_service = AnalysisService(client=_client, repository=_repo)


class AnalyzeView(MethodView):
    """View for submitting an image path for AI analysis."""

    def post(self):
        """Accept an image path, run analysis, and return the result as JSON."""
        image_path = request.form.get("image_path", "").strip()
        result = _service.analyze(image_path)
        return jsonify(result)


class LogsView(MethodView):
    """View for retrieving the latest analysis logs as JSON."""

    def get(self):
        """Return the latest 50 log entries as a JSON array."""
        logs = _repo.find_latest()
        return jsonify([log.to_dict() for log in logs])


app.add_url_rule("/analyze", view_func=AnalyzeView.as_view("analyze"))
app.add_url_rule("/logs", view_func=LogsView.as_view("logs"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
