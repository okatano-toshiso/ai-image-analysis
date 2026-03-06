# AI Image Analysis App

画像ファイルへのパスをAI分析APIに送信し、返却されたクラス分類結果をデータベースに保存するWebアプリケーションです。

---

## 課題の概要と対処方針

### 課題

> 特定の画像ファイルへのPathを与えると、AIで分析し、その画像が所属するClassを返却するAPIがあるとします。  
> このAPIに対してリクエストを投げ、レスポンスをDBに保存する処理を作成してください。  
> ただし、実際に動作するAPIは存在しないため、APIの仕様からレスポンスを想定し、保存処理を作成してください。

### 対処方針

実際のAPIが存在しないため、以下の方針で実装しました。

1. **APIレスポンスの仕様を定義**  
   課題の仕様から、成功時・失敗時のJSONレスポンス構造を想定し、型定義（TypeScript）とモデル（Python）に落とし込みました。

2. **MockAiClient によるAPIシミュレーション**  
   `services/mock_ai_client.py` に `MockAiClient` クラスを実装し、実際のAPIへのPOSTリクエストをシミュレーションしています。  
   - 80%の確率で成功レスポンス（`class_label`, `confidence` を含む）を返す  
   - 20%の確率、または `image_path` が空の場合は失敗レスポンス（`Error:E50012`）を返す

3. **レイヤードアーキテクチャによる責務分離**  
   単一ファイルに処理が集中しないよう、Model / Repository / Service / Routing の4層に分離しました。

4. **検証UIの実装**  
   実際のAPIが存在しない状況でも動作確認できるよう、React + TypeScript + Tailwind CSS によるフロントエンドを実装しました。  
   分析結果のRaw JSONを画面上で確認できる機能も追加しています。

---

## 想定APIの仕様

### リクエスト

```
POST http://example.com/
Content-Type: application/json

{
  "image_path": "/path/to/image.jpg"
}
```

### レスポンス

**成功時（`is_success: true`）**
```json
{
  "is_success": true,
  "message": "success",
  "estimated_data": {
    "class_label": 3,
    "confidence": 0.8683
  }
}
```

**失敗時（`is_success: false`）**
```json
{
  "is_success": false,
  "message": "Error:E50012",
  "estimated_data": {}
}
```

---

## アーキテクチャ

```
ai-image-analysis/
├── app.py                                      # Flaskルーティング（MethodView）
├── models/
│   └── ai_analysis_log.py                      # ORMモデル定義
├── services/
│   ├── mock_ai_client.py                       # モックAPIクライアント
│   └── analysis_service.py                     # ビジネスロジック（Facadeパターン）
├── repositories/
│   └── ai_analysis_log_repository.py           # DB操作（Repository パターン）
├── frontend/                                   # React + TypeScript + Tailwind CSS
│   └── src/
│       ├── App.tsx
│       ├── components/
│       │   ├── AnalyzeForm.tsx                 # 画像パス入力・結果表示
│       │   └── LogTable.tsx                    # 分析ログ一覧
│       └── types/
│           └── analysis.ts                     # 型定義
├── requirements.txt
└── init_db.sql                                 # MySQL用スキーマ参照
```

### 各レイヤーの責務

| レイヤー | ファイル | 責務 |
|---------|---------|------|
| ルーティング | `app.py` | HTTPリクエスト/レスポンスのみ（MethodView） |
| サービス | `services/analysis_service.py` | API呼び出し・ログ生成・保存の一連の流れを統括 |
| クライアント | `services/mock_ai_client.py` | AIAPIへのPOSTリクエストをシミュレーション |
| リポジトリ | `repositories/ai_analysis_log_repository.py` | DB操作（保存・取得） |
| モデル | `models/ai_analysis_log.py` | ORMモデル定義 |

---

## データベース

**SQLite** を使用しています（初回起動時に `ai_analysis.db` が自動生成されます）。  
MySQLを使用する場合は `init_db.sql` を参照してください。

### テーブル構造（`ai_analysis_log`）

| カラム名 | 型 | 説明 |
|---------|---|------|
| id | INTEGER | 主キー（自動採番） |
| image_path | VARCHAR(255) | 送信した画像ファイルパス |
| success | BOOLEAN | API成功フラグ（true/false） |
| message | VARCHAR(255) | APIレスポンスメッセージ |
| class | INTEGER | 分析結果のクラス番号 |
| confidence | DECIMAL(5,4) | 分析結果の信頼度（0〜1） |
| request_timestamp | DATETIME | APIリクエスト日時 |
| response_timestamp | DATETIME | APIレスポンス受信日時 |

---

## セットアップ手順

### 前提条件

- Python 3.10 以上
- Node.js 20.12 以上（Reactフロントエンドを使用する場合）

### 1. リポジトリのクローン

```bash
git clone https://github.com/okatano-toshiso/ai-image-analysis.git
cd ai-image-analysis
```

### 2. Python仮想環境の構築

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\Activate.ps1    # Windows PowerShell
pip install -r requirements.txt
```

### 3. Flask APIサーバーの起動

```bash
python app.py
# http://127.0.0.1:5000 で起動
```

### 4. Reactフロントエンドの起動（開発環境）

```bash
cd frontend
npm install
npm run dev
# http://localhost:5173 で起動
```

ブラウザで `http://localhost:5173` を開いてください。

---

## 使い方

1. 画像パス入力欄に画像ファイルパスを入力します  
   例）`/images/sample.jpg`
2. **分析実行** ボタンをクリック（またはEnterキー）
3. 分析結果（SUCCESS/FAILURE・クラス番号・信頼度）が表示されます
4. **Raw JSON** をクリックすると、APIレスポンスとDB保存内容のJSONを確認できます
5. 画面下部のログ一覧でDBの保存内容（最新50件）を確認できます

---

## 動作検証方法

### 成功ケースの確認

任意の画像パスを入力して「分析実行」を押します。  
80%の確率で `is_success: true` のレスポンスが返り、`class_label` と `confidence` がDBに保存されます。

### 失敗ケースの確認

入力欄を**空のまま**「分析実行」を押します。  
`image_path` が空の場合、`MockAiClient` は必ず `is_success: false`（`Error:E50012`）を返します。

### Raw JSONによる確認

分析実行後、結果ボックス下部の **Raw JSON** をクリックすると、以下の内容をJSON形式で確認できます：

- `log`：DBに保存されたレコードの内容
- `api_response`：APIから返却されたレスポンスの内容

---

## 実際のAPIへの差し替え方法

実際のAI分析APIが用意できた場合は、`services/mock_ai_client.py` の `MockAiClient` を以下のように差し替えてください：

```python
import requests
from typing import Any

class RealAiClient:
    """Real AI image analysis API client."""

    API_URL: str = "http://example.com/"

    def analyze(self, image_path: str) -> dict[str, Any]:
        """Send image path to the AI API and return the response."""
        response = requests.post(
            self.API_URL,
            json={"image_path": image_path},
            timeout=10,
        )
        return response.json()
```

`app.py` の `MockAiClient()` を `RealAiClient()` に変更するだけで切り替えられます。

---

## 仮想環境の無効化

```bash
deactivate
```
