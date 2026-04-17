# ポモドーロタイマー Web アプリケーション アーキテクチャ

## ディレクトリ構成

```
1.pomodoro/
├── app.py                    # Flask アプリのエントリポイント
├── src/
│   ├── __init__.py           # アプリファクトリ (create_app)
│   ├── timer.py              # タイマー状態遷移ロジック
│   ├── stats.py              # 進捗記録・集計ロジック
│   └── routes.py             # Flask ルート定義 (Blueprint)
├── static/
│   ├── css/
│   │   └── style.css         # UIスタイル（円形プログレス等）
│   └── js/
│       └── timer.js          # フロントエンドのタイマー制御
├── templates/
│   └── index.html            # メインページテンプレート
└── tests/
    ├── conftest.py           # pytest fixtures (app, client, mock clock 等)
    ├── test_timer.py         # PomodoroTimer の状態遷移テスト
    ├── test_stats.py         # PomodoroStats の記録・集計テスト
    └── test_routes.py        # API レスポンスのテスト
```

## API エンドポイント

| エンドポイント | メソッド | 役割 |
|---|---|---|
| `/` | GET | `index.html` を返す |
| `/api/stats` | GET | 今日の進捗（完了数・集中時間）を取得 |
| `/api/stats` | POST | ポモドーロ完了時に記録を追加 |

## バックエンド設計

### アプリファクトリパターン (`src/__init__.py`)

テストごとに独立したアプリインスタンスを生成し、テスト間の状態汚染を防ぐ。

```python
def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    from .routes import bp
    app.register_blueprint(bp)
    return app
```

### クラス設計

#### PomodoroTimer (`src/timer.py`)

タイマーの状態遷移ロジックのみを担当する。副作用を持たない純粋な計算クラス。

```python
class PomodoroTimer:
    WORK_DURATION = 25 * 60       # 25分
    SHORT_BREAK = 5 * 60          # 5分
    LONG_BREAK = 15 * 60          # 15分
    LONG_BREAK_INTERVAL = 4       # 4回ごとに長い休憩
```

- コンストラクタで `completed_count` と `state` を注入可能にし、任意の状態からテスト開始できるようにする
- `next_session()` は新しい状態を返すだけで内部状態を変更しない（イミュータブル設計）

#### PomodoroStats (`src/stats.py`)

進捗記録（完了数・集中時間の集計）を担当する。時刻依存をコンストラクタで注入。

```python
class PomodoroStats:
    def __init__(self, clock=None):
        self._clock = clock or datetime.now
        self._records = []

    def record_completion(self, duration_sec: int):
        ...

    def today_summary(self) -> dict:
        ...
```

- テスト時に `clock=lambda: datetime(2026, 4, 17, 23, 59)` のように固定時刻を渡せる
- 日付またぎや集計ロジックを確実にテスト可能

#### ルート (`src/routes.py`)

Blueprint を使用。依存オブジェクトは `app.config` 経由で差し替え可能。

```python
bp = Blueprint("pomodoro", __name__)

def get_stats() -> PomodoroStats:
    return current_app.config["stats"]
```

### 状態遷移

```
[作業中 25:00] --完了--> [休憩 5:00] --完了--> [作業中 25:00]
      ↑                                              |
      +--- 4回ごとに長い休憩 (15:00) へ遷移 ---+
```

状態: `idle` → `working` → `short_break` → `working` → ... → `long_break`

## フロントエンド設計

タイマーのカウントダウンはフロントエンド（JavaScript）で処理する。サーバーとの通信遅延に左右されず正確にカウントダウンできる。

| 層 | ファイル | 責務 |
|---|---|---|
| 構造 | `index.html` | セマンティックな HTML。円形プログレスバー用の SVG 要素を含む |
| 見た目 | `style.css` | 紫基調のグラデーション背景、カード型レイアウト、ボタンスタイル |
| 動作 | `timer.js` | カウントダウン制御、状態遷移、プログレスバー更新、API 呼び出し |

### UI 要素と実装方法

| UI 要素 | 実装方法 |
|---|---|
| 円形プログレスバー | SVG `<circle>` + CSS `stroke-dashoffset` アニメーション |
| 中央の「25:00」 | `<span>` でオーバーレイ表示、JS で毎秒更新 |
| 「作業中」ラベル | 状態に応じて「作業中」「休憩中」を切替 |
| 開始 / リセットボタン | `click` イベントで `timer.js` の関数を呼び出し |
| 今日の進捗セクション | `/api/stats` からデータ取得して表示 |

### ボタン動作

- **「開始」ボタン**: タイマー開始 / 一時停止のトグル
- **「リセット」ボタン**: 現在のセッションを初期値に戻す

## テスト戦略

| テストファイル | 対象 | テスト内容 |
|---|---|---|
| `test_timer.py` | `PomodoroTimer` | 状態遷移の正しさ（作業→休憩→作業、4回目で長い休憩等） |
| `test_stats.py` | `PomodoroStats` | 記録の追加、今日の完了数・集中時間の集計、日付またぎ |
| `test_routes.py` | API ルート | ステータスコード、JSON レスポンス形式 |

### テストの依存注入

```python
# tests/conftest.py
@pytest.fixture
def app():
    return create_app({"TESTING": True})

@pytest.fixture
def client(app):
    return app.test_client()
```

## テスタビリティ設計方針

| 観点 | 設計 | 効果 |
|---|---|---|
| アプリ生成 | ファクトリ関数 `create_app()` | テストごとに独立したインスタンス |
| タイマー + 進捗 | `PomodoroTimer` と `PomodoroStats` に分離 | 単一責務で個別テスト可能 |
| 時刻依存 | コンストラクタで `clock` を注入 | テスト時に固定時刻を使用可能 |
| 初期状態 | コンストラクタで任意の状態を注入 | 任意の状態からテスト開始可能 |
| ルートの依存 | `app.config` 経由で差し替え可能 | モック/スタブの注入が容易 |

## 技術選定

| 技術 | 理由 |
|---|---|
| Flask | 軽量で学習コストが低い。ワークショップ用途に最適 |
| SVG (円形プログレス) | Canvas より DOM 操作が簡単で CSS アニメーションと組み合わせやすい |
| JS でタイマー処理 | サーバー通信遅延に左右されず正確にカウントダウン可能 |
| インメモリデータ管理 | ワークショップ用途のため DB 不要でシンプルに保つ |
