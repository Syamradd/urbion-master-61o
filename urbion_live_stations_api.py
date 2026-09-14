"""Station evidence import adapter.

The production ``/station-intelligence`` route is owned by ``urbion_gateway``.
This module remains importable for the championship server's live-station
builders without registering a second route owner.
"""
from __future__ import annotations

# Importing these symbols preserves the established adapter surface for callers
# that import this module directly, while route ownership stays canonical.
from urbion_station_intelligence import build_station_intelligence

__all__ = ["build_station_intelligence"]
