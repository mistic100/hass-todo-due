"""Utility helpers for the todo_due component."""

from __future__ import annotations

import datetime
import calendar
from zoneinfo import ZoneInfo

from .consts import TodoItemDueDay, TodoItemDueMode, TodoItemDueMonth, ENUM_TO_WEEKDAY, ENUM_TO_MONTH
    

def get_absolute_due_date(
    time_zone: str,
    mode: TodoItemDueMode,
    day: TodoItemDueDay | None,
    hour: int | None,
    minute: int | None,
) -> datetime.date | datetime.datetime:
    """Gets the due date from the requested day + hour + minute."""

    now = datetime.datetime.now(ZoneInfo(time_zone))
    due = now

    # apply time
    if hour is not None:
        if mode == TodoItemDueMode.PM and hour <= 12:
            hour += 12

        due = due.replace(hour=hour, minute=minute or 0, second=0, microsecond=0)

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


def get_absolute_due_date2(
    time_zone: str,
    mode: TodoItemDueMode,
    date: int,
    month: TodoItemDueMonth | None,
    hour: int | None,
    minute: int | None,
) -> datetime.date | datetime.datetime:
    """Gets the due date from the requested date + month + hour + minute."""
    
    now = datetime.datetime.now(ZoneInfo(time_zone))
    due = now

    # apply time
    if hour is not None:
        if mode == TodoItemDueMode.PM and hour <= 12:
            hour += 12

        due = due.replace(hour=hour, minute=minute or 0, second=0, microsecond=0)

    # apply date
    due = due.replace(day=date)

    # apply month
    if month is not None:
        due = due.replace(month=ENUM_TO_MONTH[month])

    # the time is passed
    if now > due:
        # month is provided: due is next year
        if month is not None:
            due = due.replace(year=due.year+1)
        # due is next month
        else:
            due = _add_one_month(due)

    # no time provided: return only the date part
    if hour is None:
        return due.date()
    return due


def get_relative_due_date(
    time_zone: str,
    day_offset: int | None,
    hour_offset: int | None,
    minute_offset: int | None,
) -> datetime.date | datetime.datetime:
    """Gets the due date from the requested offsets."""

    now = datetime.datetime.now(ZoneInfo(time_zone))
    due = now.replace(second=0, microsecond=0)

    # apply offsets
    if day_offset is not None:
        due += datetime.timedelta(days=day_offset)
    if hour_offset is not None:
        due += datetime.timedelta(hours=hour_offset)
    if minute_offset is not None:
        due += datetime.timedelta(minutes=minute_offset)

    # no time provided: return only the date part
    if day_offset is not None and hour_offset is None and minute_offset is None:
        return due.date()
    return due


def _add_one_month(orig_date):
    """Adds one month to a date."""

    # advance year and month by one month
    new_year = orig_date.year
    new_month = orig_date.month + 1
    if new_month > 12:
        new_year += 1
        new_month -= 12

    # ensure day is valid
    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)
