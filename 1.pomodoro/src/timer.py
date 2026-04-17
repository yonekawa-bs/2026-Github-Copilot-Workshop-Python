class PomodoroTimer:
    WORK_DURATION = 25 * 60       # 25分
    SHORT_BREAK = 5 * 60          # 5分
    LONG_BREAK = 15 * 60          # 15分
    LONG_BREAK_INTERVAL = 4       # 4回ごとに長い休憩

    STATES = ("idle", "working", "short_break", "long_break")

    def __init__(self, state="idle", completed_count=0):
        if state not in self.STATES:
            raise ValueError(f"Invalid state: {state}")
        self.state = state
        self.completed_count = completed_count

    def next_session(self):
        """現在の状態から次のセッションへ遷移した新しい PomodoroTimer を返す。"""
        if self.state in ("idle", "short_break", "long_break"):
            return PomodoroTimer(state="working", completed_count=self.completed_count)

        if self.state == "working":
            new_count = self.completed_count + 1
            if new_count % self.LONG_BREAK_INTERVAL == 0:
                return PomodoroTimer(state="long_break", completed_count=new_count)
            return PomodoroTimer(state="short_break", completed_count=new_count)

    @property
    def duration(self):
        """現在の状態に対応する時間（秒）を返す。"""
        durations = {
            "idle": self.WORK_DURATION,
            "working": self.WORK_DURATION,
            "short_break": self.SHORT_BREAK,
            "long_break": self.LONG_BREAK,
        }
        return durations[self.state]
