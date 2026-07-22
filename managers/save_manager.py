import json
from pathlib import Path
from typing import Optional

from config import SAVES_DIR


class SaveManager:
    def __init__(self, save_dir: Optional[str] = None):
        self.save_dir = Path(save_dir or SAVES_DIR)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def save_state(self, data: dict, name: str = "save.json"):
        path = self.save_dir / name
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return str(path)

    def load_state(self, name: str = "save.json"):
        path = self.save_dir / name
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))
