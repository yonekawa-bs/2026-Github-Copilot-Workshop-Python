# API リファレンス

> **注意**: 現時点では REST API は未実装です。`app.py` および `src/__init__.py` は空の状態であり、Flask アプリケーションやルート定義は存在しません。

## 実装予定エンドポイント

設計ドキュメント（`architecture.md`）に基づく予定 API：

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/` | GET | `index.html` を返す |
| `/api/stats` | GET | 今日の進捗（完了数・集中時間）を取得 |
| `/api/stats` | POST | ポモドーロ完了時に記録を追加 |

### `GET /api/stats`（予定）

今日の統計情報を JSON で返す。

**レスポンス例:**

```json
{
  "completed_count": 3,
  "focus_time_sec": 4500
}
```

### `POST /api/stats`（予定）

ポモドーロセッション完了を記録する。

**リクエスト例:**

```json
{
  "duration_sec": 1500
}
```

**レスポンス例:**

```json
{
  "status": "ok"
}
```

---

API が実装されたら、このドキュメントを実際の実装に合わせて更新してください。
