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
