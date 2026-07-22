from dataclasses import dataclass


@dataclass
class User:
    id: int = 0
    username: str = ""
    password: str = ""
    coins: int = 100
    xp: int = 0
    level: int = 1
    avatar: str = "default"

    def login(self):
        return True

    def logout(self):
        return True

    def gain_xp(self, amount: int):
        self.xp += amount
        self.level = max(1, self.xp // 100 + 1)

    def buy_item(self, price: int):
        if self.coins >= price:
            self.coins -= price
            return True
        return False

    def save_outfit(self, name: str):
        return {"name": name, "user": self.username}
