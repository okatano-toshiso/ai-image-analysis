"""
AI Analysis API Client - Flask Application
画像ファイルパスをAI分析APIに送信し、結果をDBに保存するアプリケーション
"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)

# -----------------------------------------------
# DB設定（SQLite）
# -----------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'ai_analysis.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -----------------------------------------------
# Model
# -----------------------------------------------
class AiAnalysisLog(db.Model):
    __tablename__ = "ai_analysis_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String(255), nullable=True)
    success = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.String(255), nullable=True)
    class_ = db.Column("class", db.Integer, nullable=True)
    confidence = db.Column(db.Numeric(5, 4), nullable=True)
    request_timestamp = db.Column(db.DateTime, nullable=True)
    response_timestamp = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "image_path": self.image_path,
            "success": self.success,
            "message": self.message,
            "class": self.class_,
            "confidence": float(self.confidence) if self.confidence is not None else None,
            "request_timestamp": self.request_timestamp.isoformat() if self.request_timestamp else None,
            "response_timestamp": self.response_timestamp.isoformat() if self.response_timestamp else None,
        }


# -----------------------------------------------
# Mock API（実際のAPIが存在しないためモックで代替）
# -----------------------------------------------
def mock_ai_api(image_path: str) -> dict:
    """
    AI分析APIのモック関数
    実際のAPIは http://example.com/ (POST) に image_path を送信する想定。
    ランダムに成功/失敗レスポンスを返す。
    """
    if not image_path or not image_path.strip():
        return {
            "success": False,
            "message": "Error:E50012",
            "estimated_data": {}
        }

    # 80%の確率で成功レスポンス
    if random.random() < 0.8:
        return {
            "success": True,
            "message": "success",
            "estimated_data": {
                "class": random.randint(0, 9),
                "confidence": round(random.uniform(0.5, 0.9999), 4)
            }
        }
    else:
        return {
            "success": False,
            "message": "Error:E50012",
            "estimated_data": {}
        }


# -----------------------------------------------
# Routes
# -----------------------------------------------
@app.route("/")
def index():
    logs = AiAnalysisLog.query.order_by(AiAnalysisLog.id.desc()).limit(50).all()
    return render_template("index.html", logs=logs)


@app.route("/analyze", methods=["POST"])
def analyze():
    image_path = request.form.get("image_path", "").strip()

    request_timestamp = datetime.now()

    # モックAPIを呼び出し（実際はrequests.post("http://example.com/", ...)）
    api_response = mock_ai_api(image_path)

    response_timestamp = datetime.now()

    estimated = api_response.get("estimated_data", {})

    log = AiAnalysisLog(
        image_path=image_path if image_path else None,
        success=api_response["success"],
        message=api_response.get("message"),
        class_=estimated.get("class"),
        confidence=estimated.get("confidence"),
        request_timestamp=request_timestamp,
        response_timestamp=response_timestamp,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "log": log.to_dict(),
        "api_response": api_response
    })


@app.route("/logs")
def logs():
    logs = AiAnalysisLog.query.order_by(AiAnalysisLog.id.desc()).limit(50).all()
    return jsonify([l.to_dict() for l in logs])


# アプリ起動時にテーブルを自動作成
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
