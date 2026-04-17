# ポモドーロタイマー アーキテクチャ（現状）

> **注意:** このドキュメントは現在の実装状況を反映しています。実装が進むにつれて更新されます。

## 現在の実装状況

| STEP | 内容 | 状態 |
|------|------|------|
| STEP 1 | `PomodoroTimer` コアロジック | ✅ 完了 |
| STEP 2 | `PomodoroStats` 統計ロジック | ⬜ 未実装 |
| STEP 3 | Flask アプリ基盤と API ルート | ⬜ 未実装 |
| STEP 4 | HTML テンプレートと CSS | ⬜ 未実装 |
| STEP 5 | フロントエンド JavaScript | ⬜ 未実装 |

## ディレクトリ構成（現状）

```
1.pomodoro/
├── app.py                    # エントリポイント（未実装）
├── src/
│   ├── __init__.py           # アプリファクトリ（未実装）
│   └── timer.py              # タイマー状態遷移ロジック（実装済み）
└── tests/
    └── test_timer.py         # PomodoroTimer のテスト（実装済み）
```

## モジュール構成

### `src/timer.py` — タイマー状態遷移ロジック

副作用を持たない純粋な計算クラス `PomodoroTimer` のみが存在する。

- コンストラクタで `state`（状態）と `completed_count`（完了数）を受け取る
- `next_session()` メソッドで次の状態を持つ新しいインスタンスを返す（イミュータブル設計）
- `duration` プロパティで現在の状態に対応する秒数を返す

## 状態遷移

```
idle
  ↓ next_session()
working (25分)
  ↓ next_session()  [completed_count % 4 != 0]
short_break (5分)
  ↓ next_session()
working (25分)
  ↓ next_session()  [completed_count % 4 == 0]
long_break (15分)
  ↓ next_session()
working (25分)  ← 次サイクル開始
```

## テスト戦略

| テストファイル | 対象 | テスト内容 |
|---|---|---|
| `tests/test_timer.py` | `PomodoroTimer` | 状態遷移の正しさ、duration の値、イミュータブル性 |

テストは `pytest` で実行する。

```bash
cd 1.pomodoro
pytest tests/test_timer.py
```
