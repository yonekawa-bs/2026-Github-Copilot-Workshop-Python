# アーキテクチャ概要

現在の実装状況に基づいたアーキテクチャドキュメントです。

## 現在のディレクトリ構成

```
1.pomodoro/
├── app.py                    # アプリのエントリポイント（未実装）
├── pyproject.toml            # pytest 設定
├── src/
│   ├── __init__.py           # パッケージ初期化（未実装）
│   └── timer.py              # タイマー状態遷移ロジック（実装済み）
└── tests/
    └── test_timer.py         # PomodoroTimer のテスト（実装済み）
```

## 実装済みコンポーネント

### `src/timer.py` — PomodoroTimer クラス

タイマーの状態遷移ロジックのみを担当する純粋な計算クラス。副作用を持たない。

- 状態（`state`）と完了回数（`completed_count`）をコンストラクタで受け取る
- `next_session()` メソッドは新しい `PomodoroTimer` インスタンスを返す（イミュータブル設計）
- `duration` プロパティで現在の状態に対応する秒数を返す

## 未実装コンポーネント

以下のコンポーネントは設計ドキュメント（`architecture.md`, `features.md`）に記載されているが、現時点では未実装：

- `src/__init__.py` — アプリファクトリ `create_app()`
- `src/stats.py` — PomodoroStats クラス
- `src/routes.py` — Flask API ルート
- `static/` — CSS / JavaScript
- `templates/` — HTML テンプレート

## 状態遷移

```
idle → working → short_break → working → ... → long_break → working → ...
                                          ↑                            |
                                          +--- 4回ごとに長い休憩 ----+
```

| 状態 | 説明 | 時間 |
|---|---|---|
| `idle` | 初期状態（未開始） | 25分（WORK_DURATION と同じ） |
| `working` | 作業中 | 25分 |
| `short_break` | 短い休憩 | 5分 |
| `long_break` | 長い休憩（4回ごと） | 15分 |

## テスト設定

`pyproject.toml` で pytest の `pythonpath` を `["."]` に設定することで、`src` モジュールを `from src.timer import PomodoroTimer` の形式でインポートできる。
