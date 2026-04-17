import pytest
from datetime import datetime


@pytest.fixture
def mock_clock():
    """固定時刻を返すクロック関数を生成するファクトリフィクスチャ。"""
    def _factory(dt: datetime):
        return lambda: dt
    return _factory
