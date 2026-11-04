"""Utility helpers for the todo_due component."""

from __future__ import annotations

import datetime

from homeassistant.helpers import intent
from homeassistant.util import dt

from .consts import (
    TodoItemDueDay,
    TodoItemDueMode,
    TodoItemDueMonth,
    ENUM_TO_WEEKDAY,
    ENUM_TO_MONTH
)


def get_due_date_by_weekday(
    mode: TodoItemDueMode,
    day: TodoItemDueDay | None,
    hour: int | None,
    minute: int | None,
) -> datetime.date | datetime.datetime:
    """Gets the due date from the requested day + hour + minute."""

    now = dt.now().replace(second=0, microsecond=0)
    due = now

    # apply time
    if hour is not None:
        due = due.replace(
            hour=_convert_hour(mode, hour),
            minute=minute or 0,
        )

    # default day is today
    if day is None:
        day = TodoItemDueDay.TODAY

    # apply date
    match day:
        case TodoItemDueDay.TODAY:
            # no time provided: return only the date part
            if hour is None:
                return due.date()
            # the time is passed: due is tomorrow
            if now > due:
                due += datetime.timedelta(days=1)
            return due

        case TodoItemDueDay.TOMORROW:
            due += datetime.timedelta(days=1)
            # no time provided: return only the date part
            if hour is None:
                return due.date()
            return due

        case _:
            # add the corresponding number of days
            due += datetime.timedelta(
                days=(ENUM_TO_WEEKDAY[day] - due.weekday() + 7) % 7
            )
            # no time provided: return only the date part
            if hour is None:
                # if same day: due is next week
                if due.date() == now.date():
                    due += datetime.timedelta(weeks=1)
                return due.date()
            # the time is passed: due is next week
            if now > due:
                due += datetime.timedelta(weeks=1)
            return due


def get_due_date_by_date(
    mode: TodoItemDueMode,
    date: int,
    month: TodoItemDueMonth | None,
    hour: int | None,
    minute: int | None,
) -> datetime.date | datetime.datetime:
    """Gets the due date from the requested date + month + hour + minute."""
    now = dt.now().replace(second=0, microsecond=0)

    due_month = ENUM_TO_MONTH[month] if month is not None else now.month
    due_year = now.year
    due_hour = now.hour if hour is None else _convert_hour(mode, hour)
    due_minute = now.minute if hour is None else minute or 0

    due = _build_absolute_datetime(
        now,
        due_year,
        due_month,
        date,
        due_hour,
        due_minute
    )

    # Move a past date to the next occurrence.
    if now > due:
        if month is not None:
            due_year += 1
        else:
            due_year, due_month = _next_month(due_year, due_month)
        due = _build_absolute_datetime(
            now,
            due_year,
            due_month,
            date,
            due_hour,
            due_minute
        )

    # no time provided: return only the date part
    if hour is None:
        return due.date()
    return due


def get_due_date_by_offset(
    day_offset: int | None,
    hour_offset: int | None,
    minute_offset: int | None,
) -> datetime.date | datetime.datetime:
    """Gets the due date from the requested offsets."""

    now = dt.now().replace(second=0, microsecond=0)
    due = now

    # apply offsets
    if day_offset is not None:
        due += datetime.timedelta(days=day_offset)
    if hour_offset is not None:
        due += datetime.timedelta(hours=hour_offset)
    if minute_offset is not None:
        due += datetime.timedelta(minutes=minute_offset)

    # no time provided: return only the date part
    if (
        day_offset is not None
        and hour_offset is None
        and minute_offset is None
    ):
        return due.date()
    return due


def _convert_hour(mode: TodoItemDueMode, hour: int) -> int:
    """Convert a 12-hour clock hour to 24-hour time."""
    if mode == TodoItemDueMode.PM and hour < 12:
        return hour + 12
    if mode == TodoItemDueMode.AM and hour == 12:
        return 0
    return hour


def _build_absolute_datetime(
    now: datetime.datetime,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
) -> datetime.datetime:
    """Build a due datetime after validating its calendar date."""
    try:
        return now.replace(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
        )
    except ValueError:
        raise intent.IntentHandleError(
            "Supplied date does not exist",
            "invalid_date",
        )


def _next_month(year: int, month: int) -> tuple[int, int]:
    """Return the year and month following the given month."""
    if month == 12:
        return year + 1, 1
    return year, month + 1
