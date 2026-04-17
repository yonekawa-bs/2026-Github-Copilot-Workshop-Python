# ポモドーロタイマー 段階的実装計画

## STEP 1: バックエンドのコアロジック（`PomodoroTimer`）

**対象ファイル:** `src/timer.py`, `tests/test_timer.py`

- `PomodoroTimer` クラスを実装（状態定数、`next_session()` メソッド）
- 作業→短休憩→作業→…→4回目で長休憩の状態遷移ロジック
- `test_timer.py` で状態遷移の正しさを検証するテストを作成

**狙い:** UIや通信に依存しない純粋なロジックから着手し、土台を固める

---

## STEP 2: 統計ロジック（`PomodoroStats`）

**対象ファイル:** `src/stats.py`, `tests/test_stats.py`, `tests/conftest.py`

- `PomodoroStats` クラスを実装（`record_completion`, `today_summary`）
- `clock` 注入による日付またぎテスト
- `conftest.py` にモッククロック等の共通フィクスチャを定義

**狙い:** 時刻依存を注入で制御し、集計ロジックを確実にテスト

---

## STEP 3: Flask アプリ基盤と API ルート

**対象ファイル:** `src/__init__.py`, `src/routes.py`, `tests/test_routes.py`, `app.py`

- `create_app()` ファクトリ関数を実装（Blueprint 登録、`PomodoroStats` を `app.config` に設定）
- Blueprint で `GET /`, `GET /api/stats`, `POST /api/stats` を定義
- `app.py` をエントリポイントとして `create_app()` を呼び出す構成に更新
- `test_routes.py` でステータスコード・JSONレスポンス形式を検証

**狙い:** STEP 1-2 のロジックを HTTP API として公開し、結合テストで確認

---

## STEP 4: HTML テンプレートと CSS スタイリング

**対象ファイル:** `templates/index.html`, `static/css/style.css`

- セマンティック HTML の構築（SVG 円形プログレスバー、タイマー表示、ボタン、進捗セクション）
- 紫基調グラデーション背景、カード型レイアウト、ボタンデザインの CSS 実装
- `GET /` でテンプレートが正しく返却されることを確認

**狙い:** 静的な見た目をモック画像に合わせて完成させる（まだ動作なし）

---

## STEP 5: フロントエンド JavaScript（タイマー制御）

**対象ファイル:** `static/js/timer.js`

- `setInterval` による毎秒カウントダウン処理
- 開始/一時停止トグル、リセットボタンの動作
- SVG `stroke-dashoffset` による円形プログレスバーのアニメーション更新
- 状態遷移（作業中→休憩中のラベル切替、次セッションへの移行）
- セッション完了時に `POST /api/stats` で記録、`GET /api/stats` で進捗表示を更新

**狙い:** フロントエンドとバックエンドを結合し、アプリとして動作する状態にする

---

## 各 STEP の対応関係

| STEP | レイヤー | 成果物 | 確認方法 |
|------|---------|--------|----------|
| 1 | ロジック | `PomodoroTimer` | `pytest test_timer.py` |
| 2 | ロジック | `PomodoroStats` | `pytest test_stats.py` |
| 3 | API | Flask ルート + ファクトリ | `pytest test_routes.py` |
| 4 | UI（静的） | HTML + CSS | ブラウザで外観確認 |
| 5 | UI（動的） | JavaScript | ブラウザで動作確認 |
