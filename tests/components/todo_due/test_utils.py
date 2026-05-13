"""Unit tests for `todo_due.utils`."""

from __future__ import annotations

import datetime
import pytest

from custom_components.todo_due.utils import get_absolute_due_date, get_relative_due_date, get_absolute_due_date2
from custom_components.todo_due.consts import TodoItemDueDay, TodoItemDueMode, TodoItemDueMonth


@pytest.fixture
def patch_datetime_now(monkeypatch: pytest.MonkeyPatch, request):
    """Setup mocked "now" method to datetime module."""

    def _patch(day: int):
        class fakedatetime(datetime.datetime):
            @classmethod
            def now(cls, tz: str | None):
                return datetime.datetime(2025, 1, day, 12, 0, 0)

        monkeypatch.setattr(datetime, "datetime", fakedatetime)

    return _patch


@pytest.mark.parametrize(
    ("mode", "day", "hour", "minute" ,"expected"),
    [
        # now = 2025/01/01 12:00:00 (Wednesday)
        (TodoItemDueMode.H24, TodoItemDueDay.TODAY, None, None, datetime.date(2025, 1, 1)),
        (TodoItemDueMode.H24, TodoItemDueDay.TOMORROW, None, None, datetime.date(2025, 1, 2)),
        (TodoItemDueMode.H24, TodoItemDueDay.MONDAY, None, None, datetime.date(2025, 1, 6)),
        (TodoItemDueMode.H24, TodoItemDueDay.TUESDAY, None, None, datetime.date(2025, 1, 7)),
        (TodoItemDueMode.H24, TodoItemDueDay.WEDNESDAY, None, None, datetime.date(2025, 1, 8)),
        (TodoItemDueMode.H24, TodoItemDueDay.THURSDAY, None, None, datetime.date(2025, 1, 2)),
        (TodoItemDueMode.H24, TodoItemDueDay.FRIDAY, None, None, datetime.date(2025, 1, 3)),
        (TodoItemDueMode.H24, TodoItemDueDay.SATURDAY, None, None, datetime.date(2025, 1, 4)),
        (TodoItemDueMode.H24, TodoItemDueDay.SUNDAY, None, None, datetime.date(2025, 1, 5)),

        (TodoItemDueMode.H24, None, 2, None, datetime.datetime(2025, 1, 2, 2, 0, 0)),
        (TodoItemDueMode.H24, None, 15, None, datetime.datetime(2025, 1, 1, 15, 0, 0)),
        (TodoItemDueMode.H24, None, 12, 30, datetime.datetime(2025, 1, 1, 12, 30, 0)),

        (TodoItemDueMode.H24, TodoItemDueDay.TODAY, 2, None,  datetime.datetime(2025, 1, 2, 2, 0, 0)),
        (TodoItemDueMode.H24, TodoItemDueDay.TOMORROW, 12, None, datetime.datetime(2025, 1, 2, 12, 0, 0)),
        (TodoItemDueMode.H24, TodoItemDueDay.WEDNESDAY, 11, None, datetime.datetime(2025, 1, 8, 11, 0, 0)),
        (TodoItemDueMode.H24, TodoItemDueDay.WEDNESDAY, 15, None, datetime.datetime(2025, 1, 1, 15, 0, 0)),

        (TodoItemDueMode.AM, TodoItemDueDay.TOMORROW, 8, None, datetime.datetime(2025, 1, 2, 8, 0, 0)),
        (TodoItemDueMode.PM, TodoItemDueDay.TOMORROW, 8, None, datetime.datetime(2025, 1, 2, 20, 0, 0)),
        (TodoItemDueMode.PM, TodoItemDueDay.TOMORROW, 18, None, datetime.datetime(2025, 1, 2, 18, 0, 0)),
    ],
)
def test_get_absolute_due_date(
    patch_datetime_now,
    mode, day, hour, minute, expected
):
    """Verify that ``get_absolute_due_date`` returns the calculated date/time."""
    patch_datetime_now(1)
    result = get_absolute_due_date("UTC", mode, day, hour, minute)
    assert result == expected


@pytest.mark.parametrize(
    ("date", "month", "hour","expected"),
    [
        # now = 2025/01/10 12:00:00
        (20, None, None, datetime.date(2025, 1, 20)),
        (2, TodoItemDueMonth.MARCH, None, datetime.date(2025, 3, 2)),
        (20, None, 10, datetime.datetime(2025, 1, 20, 10, 0, 0)),
        (2, TodoItemDueMonth.MARCH, 10, datetime.datetime(2025, 3, 2, 10, 0, 0)),

        (1, None, None, datetime.date(2025, 2, 1)),
        (1, TodoItemDueMonth.JANUARY, None, datetime.date(2026, 1, 1)),
        (10, None, 10, datetime.datetime(2025, 2, 10, 10, 0, 0)),
        (10, TodoItemDueMonth.JANUARY, 10, datetime.datetime(2026, 1, 10, 10, 0, 0)),
    ],
)
def test_get_absolute_due_date2(
    patch_datetime_now,
    date, month, hour, expected
):
    """Verify that ``get_absolute_due_date2`` returns the calculated date/time."""
    patch_datetime_now(10)
    result = get_absolute_due_date2("UTC", TodoItemDueMode.H24, date, month, hour, 0)
    assert result == expected


@pytest.mark.parametrize(
    ("day_offset", "hour_offset", "minute_offset", "expected"),
    [
        # now = 2025/01/01 12:00:00 (Wednesday)
        (1, None, None, datetime.date(2025, 1, 2)),
        (10, None, None, datetime.date(2025, 1, 11)),
        (None, 2, None, datetime.datetime(2025, 1, 1, 14, 0, 0)),
        (None, 48, None, datetime.datetime(2025, 1, 3, 12, 0, 0)),
        (None, None, 10, datetime.datetime(2025, 1, 1, 12, 10, 0)),
        (None, None, 120, datetime.datetime(2025, 1, 1, 14, 0, 0)),
        (None, 2, 20, datetime.datetime(2025, 1, 1, 14, 20, 0),),
        (3, 5, None, datetime.datetime(2025, 1, 4, 17, 0, 0)),
    ],
)
def test_get_relative_due_date(
    patch_datetime_now,
    day_offset, hour_offset, minute_offset, expected
):
    """Verify that ``get_relative_due_date`` returns the calculated date/time."""
    patch_datetime_now(1)
    result = get_relative_due_date("UTC", day_offset, hour_offset, minute_offset)
    assert result == expected
