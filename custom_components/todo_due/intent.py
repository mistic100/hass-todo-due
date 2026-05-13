"""The todo_due intent handlers."""

import datetime
import logging
from typing import Any
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, intent
from homeassistant.components.todo import TodoItem, TodoItemStatus, TodoListEntity, DATA_COMPONENT, DOMAIN as TODO_DOMAIN

from .utils import get_absolute_due_date, get_relative_due_date, get_absolute_due_date2
from .consts import TodoItemDueDay, TodoItemDueMode, TodoItemDueMonth, DOMAIN


LOGGER = logging.getLogger("todo_due")


async def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up todo_due intents."""
    intent.async_register(hass, TodoDueAddItem())


class TodoDueAddItem(intent.IntentHandler):
    """Handle TodoDueAddItem intents."""

    intent_type =  "TodoDueAddItem"
    platforms = {DOMAIN}
    description = "Add item to a todo list."

    slot_schema = {
        vol.Required("name"): intent.non_empty_string,
        vol.Required("item"): intent.non_empty_string,
        # absolute due datetime
        vol.Optional("mode"): vol.In([d.value for d in TodoItemDueMode]),
        vol.Optional("due_day"): vol.In([d.value for d in TodoItemDueDay]),
        vol.Optional("due_hour"): cv.positive_int,
        vol.Optional("due_minute"): cv.positive_int,
        vol.Optional("due_date"): cv.positive_int,
        vol.Optional("due_month"): vol.In([d.value for d in TodoItemDueMonth]),
        # relative due datetime
        vol.Optional("due_day_offset"): cv.positive_int,
        vol.Optional("due_hour_offset"): cv.positive_int,
        vol.Optional("due_minute_offset"): cv.positive_int,
    }

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        hass = intent_obj.hass

        slots = self.async_validate_slots(intent_obj.slots)
        list_name = slots["name"]["value"]

        target_list: TodoListEntity | None = None

        # Find matching list
        LOGGER.info(f"Search list {list_name}")
        match_constraints = intent.MatchTargetsConstraints(
            name=list_name, domains=[TODO_DOMAIN], assistant=intent_obj.assistant
        )
        match_result = intent.async_match_targets(hass, match_constraints)
        if not match_result.is_match:
            raise intent.MatchFailedError(
                result=match_result, constraints=match_constraints
            )

        target_list = hass.data[DATA_COMPONENT].get_entity(
            match_result.states[0].entity_id
        )
        if target_list is None:
            raise intent.IntentHandleError(
                f"No to-do list: {list_name}", "list_not_found"
            )

        # Execute specific action
        await self._async_do_handle(target_list, slots, intent_obj)

        # Build intent response
        response: intent.IntentResponse = intent_obj.create_response()
        response.async_set_results(
            [
                intent.IntentResponseTarget(
                    type=intent.IntentResponseTargetType.ENTITY,
                    name=list_name,
                    id=target_list.entity_id,
                )
            ]
        )
        return response

    async def _async_do_handle(
        self,
        target_list: TodoListEntity,
        slots: dict[str, Any],
        intent_obj: intent.Intent,
    ) -> None:
        """Execute action specific to this intent handler."""
        hass = intent_obj.hass

        item = slots["item"]["value"].strip()

        mode: TodoItemDueMode = TodoItemDueMode.H24
        if "mode" in slots:
            mode = slots["mode"]["value"]
        due_day: TodoItemDueDay | None = None
        if "due_day" in slots:
            due_day = slots["due_day"]["value"]
        due_hour: int | None = None
        if "due_hour" in slots:
            due_hour = slots["due_hour"]["value"]
        due_minute: int | None = None
        if "due_minute" in slots:
            due_minute = slots["due_minute"]["value"]
        due_date: int | None = None
        if "due_date" in slots:
            due_date = slots["due_date"]["value"]
        due_month: TodoItemDueMonth | None = None
        if "due_month" in slots:
            due_month = slots["due_month"]["value"]
        due_day_offset: int | None = None
        if "due_day_offset" in slots:
            due_day_offset = slots["due_day_offset"]["value"]
        due_hour_offset: int | None = None
        if "due_hour_offset" in slots:
            due_hour_offset = slots["due_hour_offset"]["value"]
        due_minute_offset: int | None = None
        if "due_minute_offset" in slots:
            due_minute_offset = slots["due_minute_offset"]["value"]

        # Compute due date
        due: datetime.date | datetime.datetime | None = None
        if due_date is not None:
            due = get_absolute_due_date2(
                hass.config.time_zone,
                mode,
                due_date,
                due_month,
                due_hour,
                due_minute,
            )
        elif due_day is not None or due_hour is not None:
            due = get_absolute_due_date(
                hass.config.time_zone,
                mode,
                due_day,
                due_hour,
                due_minute,
            )
        elif (
            due_day_offset is not None
            or due_hour_offset is not None
            or due_minute_offset is not None
        ):
            due = get_relative_due_date(
                hass.config.time_zone,
                due_day_offset,
                due_hour_offset,
                due_minute_offset,
            )

        # Add to list
        await target_list.async_create_todo_item(
            TodoItem(summary=item, status=TodoItemStatus.NEEDS_ACTION, due=due)
        )
