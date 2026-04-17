# ポモドーロタイマー 実装機能一覧

## バックエンド（Python / Flask）

| # | ファイル | 機能 | 説明 |
|---|---|---|---|
| 1 | `src/__init__.py` | アプリファクトリ `create_app()` | Flask アプリの生成、Blueprint 登録、`PomodoroStats` の `app.config` への設定 |
| 2 | `src/timer.py` | `PomodoroTimer` クラス | 状態遷移ロジック（作業→短休憩→作業→…→長休憩）。`next_session()` でイミュータブルに次の状態を返す |
| 3 | `src/stats.py` | `PomodoroStats` クラス | ポモドーロ完了の記録追加 (`record_completion`)、今日の完了数・集中時間の集計 (`today_summary`) |
| 4 | `src/routes.py` | API ルート (Blueprint) | `GET /` → HTMLテンプレート返却、`GET /api/stats` → 進捗JSON返却、`POST /api/stats` → 完了記録追加 |
| 5 | `app.py` | エントリポイント | `create_app()` を呼び出してサーバー起動 |

## フロントエンド（HTML / CSS / JS）

| # | ファイル | 機能 | 説明 |
|---|---|---|---|
| 6 | `templates/index.html` | メインページ | 円形プログレスバー（SVG）、タイマー表示、状態ラベル、ボタン、進捗セクション |
| 7 | `static/css/style.css` | UIスタイル | 紫基調グラデーション背景、カード型レイアウト、円形プログレスバーのスタイル、ボタンデザイン |
| 8 | `static/js/timer.js` | タイマー制御 | カウントダウン処理、開始/一時停止トグル、リセット、プログレスバー更新、状態遷移、API連携 |

## テスト

| # | ファイル | 機能 | 説明 |
|---|---|---|---|
| 9 | `tests/conftest.py` | テストフィクスチャ | `app`、`client`、モッククロック等の pytest fixtures |
| 10 | `tests/test_timer.py` | タイマーテスト | 状態遷移の正しさ（作業→休憩→作業、4回目で長い休憩） |
| 11 | `tests/test_stats.py` | 統計テスト | 記録追加、今日の完了数・集中時間の集計、日付またぎ |
| 12 | `tests/test_routes.py` | ルートテスト | ステータスコード、JSONレスポンス形式の検証 |

## 主要なビジネスロジック詳細

### PomodoroTimer の状態遷移

- 作業時間: **25分**（1500秒）
- 短い休憩: **5分**（300秒）
- 長い休憩: **15分**（900秒）、**4回ごと**に発生
- 状態: `idle` → `working` → `short_break` → `working` → … → `long_break`

### timer.js のフロントエンド機能

- 毎秒のカウントダウン更新（`setInterval`）
- SVG `stroke-dashoffset` による円形プログレスバーのアニメーション
- 「開始」ボタン → 開始 / 一時停止のトグル動作
- 「リセット」ボタン → 現在のセッションを初期値に戻す
- セッション完了時に `POST /api/stats` でサーバーに記録
- `GET /api/stats` で進捗を取得し「今日の進捗」セクションを更新
