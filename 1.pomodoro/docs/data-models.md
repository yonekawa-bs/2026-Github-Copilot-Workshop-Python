# データモデル仕様

> **注意:** このドキュメントは現在の実装状況を反映しています。

## PomodoroTimer（実装済み）

**ファイル:** `src/timer.py`

タイマーの状態遷移ロジックを担当する。副作用を持たない純粋な計算クラス。

### クラス定数

| 定数 | 値 | 説明 |
|---|---|---|
| `WORK_DURATION` | `1500`（25分） | 作業セッションの時間（秒） |
| `SHORT_BREAK` | `300`（5分） | 短い休憩の時間（秒） |
| `LONG_BREAK` | `900`（15分） | 長い休憩の時間（秒） |
| `LONG_BREAK_INTERVAL` | `4` | 長い休憩が発生するサイクル間隔 |
| `STATES` | `("idle", "working", "short_break", "long_break")` | 有効な状態の一覧 |

### コンストラクタ

```python
PomodoroTimer(state="idle", completed_count=0)
```

| 引数 | 型 | デフォルト | 説明 |
|---|---|---|---|
| `state` | `str` | `"idle"` | 初期状態。`STATES` に含まれない値を渡すと `ValueError` が発生する |
| `completed_count` | `int` | `0` | これまでに完了した作業セッションの数 |

### メソッド・プロパティ

#### `next_session() -> PomodoroTimer`

現在の状態から次のセッションへ遷移した**新しい** `PomodoroTimer` インスタンスを返す。元のインスタンスは変更されない（イミュータブル設計）。

| 現在の状態 | 次の状態 | `completed_count` の変化 |
|---|---|---|
| `idle` | `working` | 変化なし |
| `short_break` | `working` | 変化なし |
| `long_break` | `working` | 変化なし |
| `working` | `short_break` | `+1`（`new_count % 4 != 0` のとき） |
| `working` | `long_break` | `+1`（`new_count % 4 == 0` のとき） |

#### `duration` プロパティ

現在の状態に対応する時間を秒数で返す。

| 状態 | 返り値（秒） |
|---|---|
| `idle` | `1500`（25分） |
| `working` | `1500`（25分） |
| `short_break` | `300`（5分） |
| `long_break` | `900`（15分） |

### 使用例

```python
from src.timer import PomodoroTimer

# デフォルト（idle 状態）で作成
timer = PomodoroTimer()
print(timer.state)           # "idle"
print(timer.duration)        # 1500

# 作業開始
timer = timer.next_session()
print(timer.state)           # "working"
print(timer.completed_count) # 0

# 1回目の作業完了 → 短い休憩へ
timer = timer.next_session()
print(timer.state)           # "short_break"
print(timer.completed_count) # 1

# 4回目の作業完了 → 長い休憩へ
timer = PomodoroTimer(state="working", completed_count=3)
timer = timer.next_session()
print(timer.state)           # "long_break"
print(timer.completed_count) # 4
```

---

## PomodoroStats（未実装）

`src/stats.py` として実装予定。ポモドーロ完了の記録と集計を担当する。

---

## 注記

現時点では `PomodoroTimer` のみが実装されている。`PomodoroStats` は STEP 2 で追加予定。
