"""Pytest configuration fixtures for the todo_due tests."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

# Mocks
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.config_validation"] = MagicMock()
sys.modules["homeassistant.helpers.intent"] = MagicMock()
sys.modules["homeassistant.components"] = MagicMock()
sys.modules["homeassistant.components.todo"] = MagicMock()
