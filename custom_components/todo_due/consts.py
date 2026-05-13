from enum import StrEnum

DOMAIN = "todo_due"

class TodoItemDueDay(StrEnum):
    """Day value for todo_due."""

    TODAY = "today"
    TOMORROW = "tomorrow"
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"

class TodoItemDueMonth(StrEnum):
    """Month value for toto_due."""

    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"


class TodoItemDueMode(StrEnum):
    """Time mode for todo_due."""

    H24 = "h24"
    AM = "am"
    PM = "pm"


ENUM_TO_WEEKDAY = {
    TodoItemDueDay.MONDAY: 0,
    TodoItemDueDay.TUESDAY: 1,
    TodoItemDueDay.WEDNESDAY: 2,
    TodoItemDueDay.THURSDAY: 3,
    TodoItemDueDay.FRIDAY: 4,
    TodoItemDueDay.SATURDAY: 5,
    TodoItemDueDay.SUNDAY: 6,
}

ENUM_TO_MONTH = {
    TodoItemDueMonth.JANUARY: 1,
    TodoItemDueMonth.FEBRUARY: 2,
    TodoItemDueMonth.MARCH: 3,
    TodoItemDueMonth.APRIL: 4,
    TodoItemDueMonth.MAY: 5,
    TodoItemDueMonth.JUNE: 6,
    TodoItemDueMonth.JULY: 7,
    TodoItemDueMonth.AUGUST: 8,
    TodoItemDueMonth.SEPTEMBER: 9,
    TodoItemDueMonth.OCTOBER: 10,
    TodoItemDueMonth.NOVEMBER: 11,
    TodoItemDueMonth.DECEMBER: 12,
}
