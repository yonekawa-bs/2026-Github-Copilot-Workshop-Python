from datetime import datetime


class PomodoroStats:
    def __init__(self, clock=None):
        self._clock = clock or datetime.now
        self._records = []

    def record_completion(self, duration_sec: int):
        """ポモドーロ完了を記録する。"""
        self._records.append({
            "completed_at": self._clock(),
            "duration_sec": duration_sec,
        })

    def today_summary(self) -> dict:
        """今日の完了数と合計集中時間を返す。"""
        today = self._clock().date()
        today_records = [
            r for r in self._records if r["completed_at"].date() == today
        ]
        return {
            "completed_count": len(today_records),
            "total_focus_sec": sum(r["duration_sec"] for r in today_records),
        }
