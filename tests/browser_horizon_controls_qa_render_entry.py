"""Run HORIZON controls QA against the canonical workstation URL."""
from __future__ import annotations

import os
import browser_horizon_controls_qa as qa

qa.BASE_URL = os.getenv("URBION_APP_URL", "http://127.0.0.1:8765/championship.html")

if __name__ == "__main__":
    qa.main()
