"""AI Analysis API Client - Flask Application."""

from flask import Flask, render_template, request, jsonify
from models.ai_analysis_log import db
from services.mock_ai_client import MockAiClient
from services.analysis_service import AnalysisService
from repositories.ai_analysis_log_repository import AiAnalysisLogRepository
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'ai_analysis.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

_repo = AiAnalysisLogRepository()
_client = MockAiClient()
_service = AnalysisService(client=_client, repository=_repo)


@app.route("/")
def index():
    logs = _repo.find_latest()
    return render_template("index.html", logs=logs)


@app.route("/analyze", methods=["POST"])
def analyze():
    image_path = request.form.get("image_path", "").strip()
    result = _service.analyze(image_path)
    return jsonify(result)


@app.route("/logs")
def logs():
    logs = _repo.find_latest()
    return jsonify([l.to_dict() for l in logs])


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
