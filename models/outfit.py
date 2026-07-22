from dataclasses import dataclass, field
from pathlib import Path
from shutil import copyfile


@dataclass
class Outfit:
    top: str = ""
    bottom: str = ""
    shoes: str = ""
    bag: str = ""
    accessories: str = ""
    name: str = "casual"
    items: list = field(default_factory=list)

    def save(self):
        return {"name": self.name, "items": self.items}

    def export(self, destination: str):
        source = self._find_outfit_image()
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        copyfile(source, target)
        return str(target)

    def _find_outfit_image(self) -> Path:
        downloads_path = Path.home() / "Downloads" / "pinkdress.png"
        asset_path = Path(__file__).parent.parent / "assets" / "images" / "pinkdress.png"
        for path in (downloads_path, asset_path):
            if path.exists() and path.stat().st_size > 0:
                return path
        raise FileNotFoundError("No outfit picture found. Add pinkdress.png to Downloads or assets/images.")

    def calculate_style_score(self):
        return len(self.items) * 10
