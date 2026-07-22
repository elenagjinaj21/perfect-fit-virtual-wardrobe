from dataclasses import dataclass


@dataclass
class Clothing:
    id: int = 0
    name: str = ""
    category: str = ""
    color: str = ""
    brand: str = ""
    price: int = 0
    rarity: str = "common"
    season: str = "all"
    image: str = ""

    def wear(self):
        return True

    def remove(self):
        return True

    def sell(self):
        return True

    def preview(self):
        return self.name
