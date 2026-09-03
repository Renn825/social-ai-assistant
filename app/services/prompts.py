from pathlib import Path


def load_prompt(name: str) -> str:
    path = Path("prompts") / name
    return path.read_text(encoding="utf-8")
