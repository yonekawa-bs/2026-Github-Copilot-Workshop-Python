from datetime import datetime

from src.stats import PomodoroStats


class TestRecordCompletion:
    def test_single_record(self, mock_clock):
        clock = mock_clock(datetime(2026, 4, 17, 10, 0))
        stats = PomodoroStats(clock=clock)
        stats.record_completion(1500)
        summary = stats.today_summary()
        assert summary["completed_count"] == 1
        assert summary["total_focus_sec"] == 1500

    def test_multiple_records(self, mock_clock):
        clock = mock_clock(datetime(2026, 4, 17, 10, 0))
        stats = PomodoroStats(clock=clock)
        stats.record_completion(1500)
        stats.record_completion(1500)
        stats.record_completion(1500)
        summary = stats.today_summary()
        assert summary["completed_count"] == 3
        assert summary["total_focus_sec"] == 4500


class TestTodaySummary:
    def test_empty_records(self, mock_clock):
        clock = mock_clock(datetime(2026, 4, 17, 10, 0))
        stats = PomodoroStats(clock=clock)
        summary = stats.today_summary()
        assert summary["completed_count"] == 0
        assert summary["total_focus_sec"] == 0

    def test_returns_dict_with_expected_keys(self, mock_clock):
        clock = mock_clock(datetime(2026, 4, 17, 10, 0))
        stats = PomodoroStats(clock=clock)
        summary = stats.today_summary()
        assert "completed_count" in summary
        assert "total_focus_sec" in summary


class TestDateBoundary:
    def test_records_across_dates(self):
        """日付またぎ: 昨日の記録は今日の集計に含まれない。"""
        times = iter([
            datetime(2026, 4, 16, 23, 30),  # record_completion (昨日)
            datetime(2026, 4, 17, 0, 30),    # record_completion (今日)
            datetime(2026, 4, 17, 0, 30),    # today_summary
        ])
        clock = lambda: next(times)
        stats = PomodoroStats(clock=clock)
        stats.record_completion(1500)  # 昨日の記録
        stats.record_completion(1500)  # 今日の記録

        summary = stats.today_summary()
        assert summary["completed_count"] == 1
        assert summary["total_focus_sec"] == 1500

    def test_midnight_boundary(self):
        """23:59 に記録し、00:00 で集計すると前日の記録は含まれない。"""
        times = iter([
            datetime(2026, 4, 16, 23, 59),  # record_completion 時
            datetime(2026, 4, 17, 0, 0),     # today_summary 時
        ])
        clock = lambda: next(times)
        stats = PomodoroStats(clock=clock)
        stats.record_completion(1500)
        summary = stats.today_summary()
        assert summary["completed_count"] == 0
        assert summary["total_focus_sec"] == 0

    def test_same_day_after_midnight(self):
        """0:01 に記録し、同日中に集計すると含まれる。"""
        clock = lambda: datetime(2026, 4, 17, 0, 1)
        stats = PomodoroStats(clock=clock)
        stats.record_completion(1500)
        summary = stats.today_summary()
        assert summary["completed_count"] == 1
        assert summary["total_focus_sec"] == 1500


class TestClockDefault:
    def test_default_clock_uses_datetime_now(self):
        """clock 未指定時は datetime.now が使われる。"""
        stats = PomodoroStats()
        stats.record_completion(1500)
        summary = stats.today_summary()
        assert summary["completed_count"] == 1
        assert summary["total_focus_sec"] == 1500
