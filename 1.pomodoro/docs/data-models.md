# データモデル仕様

現在の実装に基づいたデータモデルドキュメントです。

## PomodoroTimer (`src/timer.py`)

ポモドーロタイマーの状態を表すクラス。イミュータブル設計。

### クラス定数

| 定数 | 値 | 説明 |
|---|---|---|
| `WORK_DURATION` | `1500`（25分） | 作業セッションの秒数 |
| `SHORT_BREAK` | `300`（5分） | 短い休憩の秒数 |
| `LONG_BREAK` | `900`（15分） | 長い休憩の秒数 |
| `LONG_BREAK_INTERVAL` | `4` | 長い休憩が発生する作業完了回数の間隔 |
| `STATES` | `("idle", "working", "short_break", "long_break")` | 有効な状態値 |

### インスタンス属性

| 属性 | 型 | デフォルト値 | 説明 |
|---|---|---|---|
| `state` | `str` | `"idle"` | 現在のタイマー状態。`STATES` のいずれかでなければならない |
| `completed_count` | `int` | `0` | 作業セッション完了回数 |

### コンストラクタ

```python
PomodoroTimer(state="idle", completed_count=0)
```

- `state` が `STATES` に含まれない値の場合、`ValueError` を送出する

### メソッド

#### `next_session() -> PomodoroTimer`

現在の状態から次のセッションへ遷移した新しい `PomodoroTimer` インスタンスを返す。

| 現在の状態 | 次の状態 | completed_count の変化 |
|---|---|---|
| `idle` | `working` | 変化なし |
| `short_break` | `working` | 変化なし |
| `long_break` | `working` | 変化なし |
| `working` | `short_break`（`completed_count % 4 != 0`） | +1 |
| `working` | `long_break`（`completed_count % 4 == 0`） | +1 |

#### `duration` プロパティ

現在の状態に対応する時間を秒数で返す。

| 状態 | 戻り値（秒） |
|---|---|
| `idle` | `1500`（25分） |
| `working` | `1500`（25分） |
| `short_break` | `300`（5分） |
| `long_break` | `900`（15分） |

### 使用例

```python
from src.timer import PomodoroTimer

# デフォルト（idle状態）で生成
timer = PomodoroTimer()
print(timer.state)           # "idle"
print(timer.duration)        # 1500

# 次のセッションへ遷移（idle → working）
timer = timer.next_session()
print(timer.state)           # "working"

# 作業完了（working → short_break）
timer = timer.next_session()
print(timer.state)           # "short_break"
print(timer.completed_count) # 1

# 4回目の作業完了時は長い休憩へ
timer = PomodoroTimer(state="working", completed_count=3)
timer = timer.next_session()
print(timer.state)           # "long_break"
print(timer.completed_count) # 4
```

## 未実装モデル

以下のデータモデルは設計ドキュメントに記載されているが、現時点では未実装：

- **PomodoroStats** (`src/stats.py`) — 進捗記録・集計クラス
