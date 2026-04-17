import pytest
from src.timer import PomodoroTimer


class TestPomodoroTimerInit:
    def test_default_state(self):
        timer = PomodoroTimer()
        assert timer.state == "idle"
        assert timer.completed_count == 0

    def test_custom_state(self):
        timer = PomodoroTimer(state="working", completed_count=3)
        assert timer.state == "working"
        assert timer.completed_count == 3

    def test_invalid_state_raises(self):
        with pytest.raises(ValueError):
            PomodoroTimer(state="invalid")


class TestNextSession:
    def test_idle_to_working(self):
        timer = PomodoroTimer(state="idle")
        next_timer = timer.next_session()
        assert next_timer.state == "working"
        assert next_timer.completed_count == 0

    def test_working_to_short_break(self):
        timer = PomodoroTimer(state="working", completed_count=0)
        next_timer = timer.next_session()
        assert next_timer.state == "short_break"
        assert next_timer.completed_count == 1

    def test_short_break_to_working(self):
        timer = PomodoroTimer(state="short_break", completed_count=1)
        next_timer = timer.next_session()
        assert next_timer.state == "working"
        assert next_timer.completed_count == 1

    def test_fourth_work_to_long_break(self):
        timer = PomodoroTimer(state="working", completed_count=3)
        next_timer = timer.next_session()
        assert next_timer.state == "long_break"
        assert next_timer.completed_count == 4

    def test_long_break_to_working(self):
        timer = PomodoroTimer(state="long_break", completed_count=4)
        next_timer = timer.next_session()
        assert next_timer.state == "working"
        assert next_timer.completed_count == 4

    def test_full_cycle(self):
        """作業→短休憩→作業→短休憩→作業→短休憩→作業→長休憩 の1サイクルを検証"""
        timer = PomodoroTimer()

        # idle → working
        timer = timer.next_session()
        assert timer.state == "working"

        for i in range(1, 4):
            # working → short_break
            timer = timer.next_session()
            assert timer.state == "short_break"
            assert timer.completed_count == i

            # short_break → working
            timer = timer.next_session()
            assert timer.state == "working"

        # 4回目の working → long_break
        timer = timer.next_session()
        assert timer.state == "long_break"
        assert timer.completed_count == 4

        # long_break → working（次のサイクル開始）
        timer = timer.next_session()
        assert timer.state == "working"
        assert timer.completed_count == 4

    def test_eighth_work_to_long_break(self):
        """8回目の作業完了でも長休憩になることを確認"""
        timer = PomodoroTimer(state="working", completed_count=7)
        next_timer = timer.next_session()
        assert next_timer.state == "long_break"
        assert next_timer.completed_count == 8


class TestDuration:
    def test_idle_duration(self):
        timer = PomodoroTimer(state="idle")
        assert timer.duration == 25 * 60

    def test_working_duration(self):
        timer = PomodoroTimer(state="working")
        assert timer.duration == 25 * 60

    def test_short_break_duration(self):
        timer = PomodoroTimer(state="short_break")
        assert timer.duration == 5 * 60

    def test_long_break_duration(self):
        timer = PomodoroTimer(state="long_break")
        assert timer.duration == 15 * 60


class TestImmutability:
    def test_next_session_returns_new_instance(self):
        timer = PomodoroTimer(state="working", completed_count=0)
        next_timer = timer.next_session()
        assert timer is not next_timer
        assert timer.state == "working"
        assert timer.completed_count == 0
