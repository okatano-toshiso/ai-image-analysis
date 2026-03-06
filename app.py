"""AI Analysis API Client - Flask Application."""

from flask import Flask, render_template, request, jsonify
from models.ai_analysis_log import db, AiAnalysisLog
from services.mock_ai_client import MockAiClient
from repositories.ai_analysis_log_repository import AiAnalysisLogRepository
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'ai_analysis.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

_client = MockAiClient()
_repo = AiAnalysisLogRepository()


@app.route("/")
def index():
    logs = _repo.find_latest()
    return render_template("index.html", logs=logs)


@app.route("/analyze", methods=["POST"])
def analyze():
    image_path = request.form.get("image_path", "").strip()

    request_timestamp = datetime.now()
    api_response = _client.analyze(image_path)
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
    _repo.save(log)

    return jsonify({
        "log": log.to_dict(),
        "api_response": api_response
    })


@app.route("/logs")
def logs():
    logs = _repo.find_latest()
    return jsonify([l.to_dict() for l in logs])


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
