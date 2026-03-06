# AI Image Analysis App

画像ファイルパスをAI分析APIに送信し、レスポンスをデータベースに保存するWebアプリケーションです。

## 構成

```
ai-image-analysis/
├── app.py              # メインアプリケーション（Flask）
├── requirements.txt    # 依存パッケージ
├── env.example         # 環境変数サンプル（.envにコピーして使用）
├── .gitignore
├── README.md
└── templates/
    └── index.html      # WebUI
```

> `ai_analysis.db`（SQLiteファイル）はアプリ初回起動時に自動生成されます。

## 機能

- 画像ファイルパスを入力してAI分析を実行
- モックAPIによるSuccess/Failureレスポンスのシミュレーション（実際のAPIが存在しないため）
- 分析結果（class, confidence）をデータベースに保存
- 分析ログを一覧表示（最新50件）

## データベースについて

課題では MySQL を想定したテーブル定義が提示されていますが、本実装では **SQLite** を使用しています。  
アプリ初回起動時に `ai_analysis.db` が自動生成されます。

MySQL を使用する場合は `init_db.sql` を参照してください。

### テーブル構造（`ai_analysis_log`）

| カラム名 | 型 | 説明 |
|---|---|---|
| id | INTEGER | 主キー（自動採番） |
| image_path | VARCHAR(255) | 送信した画像ファイルパス |
| success | BOOLEAN | API成功フラグ（true/false） |
| message | VARCHAR(255) | APIレスポンスメッセージ |
| class | INTEGER | 分析結果のクラス番号 |
| confidence | DECIMAL(5,4) | 分析結果の信頼度（0〜1） |
| request_timestamp | DATETIME | APIリクエスト日時 |
| response_timestamp | DATETIME | APIレスポンス受信日時 |

## セットアップ手順

### 前提条件

- Python 3.10 以上

---

### 1. リポジトリのクローン

```bash
git clone <リポジトリURL>
cd ai-image-analysis
```

---

### 2. 仮想環境の構築（venv）

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化（Mac/Linux）
source venv/bin/activate

# Windows（PowerShell）
# venv\Scripts\Activate.ps1
```

有効化されると、ターミナルの先頭に `(venv)` と表示されます。

---

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

---

### 4. アプリケーションの起動

```bash
python app.py
```

初回起動時に `ai_analysis.db`（SQLiteファイル）が自動で作成されます。  
ブラウザで `http://localhost:5000` を開いてください。

---

## 使い方

1. 画像パス入力欄に画像ファイルパスを入力します  
   例）`/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg`
2. 「分析実行」ボタンをクリック（またはEnterキー）
3. 分析結果が画面に表示され、DBに保存されます
4. 画面下部のログ一覧でDBの保存内容を確認できます

---

## モックAPIについて

実際のAI分析API（`http://example.com/`）が存在しないため、`app.py` 内の `mock_ai_api()` 関数でレスポンスをシミュレーションしています。

- image_pathが空の場合 → 必ず失敗レスポンス
- 通常時 → 80%の確率で成功、20%で失敗レスポンス

実際のAPIが用意できた場合は、`analyze()` 関数内のモック呼び出し部分を以下に差し替えてください：

```python
import requests

response = requests.post(
    "http://example.com/",
    json={"image_path": image_path},
    timeout=10
)
api_response = response.json()
```

---

## 仮想環境の無効化

```bash
deactivate
```