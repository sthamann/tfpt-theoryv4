"""TFPT Starobinsky/scalaron inflation predictions vs CMB data."""

from __future__ import annotations

from . import constants
from .inflation_test import InflationResult, run_inflation

__all__ = ["constants", "InflationResult", "run_inflation"]
__version__ = "0.1.0"
