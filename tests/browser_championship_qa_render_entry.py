"""Run canonical workstation browser QA through the production entrypoint."""
from __future__ import annotations

import os
import browser_championship_qa as qa
import browser_championship_qa_stable as stable

qa.BASE_URL = os.getenv("URBION_APP_URL", "http://127.0.0.1:8765/championship.html")
stable.qa.BASE_URL = qa.BASE_URL

if __name__ == "__main__":
    qa.main()
