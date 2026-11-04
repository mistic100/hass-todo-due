"""Pytest configuration fixtures for the todo_due tests."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

# Mocks
sys.modules["homeassistant.config_entries"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock(intent=MagicMock(IntentHandleError=Exception))
sys.modules["homeassistant.util"] = MagicMock(dt=MagicMock(now=MagicMock()))
