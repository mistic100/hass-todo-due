"""Config flow for todo_due."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .consts import DOMAIN


class TodoDueConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for todo_due."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="To-do list due date Assist intent",
                data={}
            )

        return self.async_show_form(step_id="user")
