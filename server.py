from pathlib import Path

server = Path("/content/URBION_GITHUB_BACKEND/server.py")

print(server.read_text(encoding="utf-8"))
