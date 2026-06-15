"""TFPT ringdown echo-amplitude-ratio test on the LVK GWTC catalogue."""

from __future__ import annotations

from . import constants
from .echo_forecast import EchoForecast, forecast

__all__ = ["constants", "EchoForecast", "forecast"]
__version__ = "0.1.0"
