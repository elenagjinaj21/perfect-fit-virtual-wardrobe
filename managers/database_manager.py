import sqlite3
from pathlib import Path
from typing import Optional

from config import DB_PATH
from utils.security import hash_password


class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path or DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE COLLATE NOCASE NOT NULL,
                password TEXT NOT NULL,
                coins INTEGER DEFAULT 100,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                avatar TEXT DEFAULT 'default'
            );

            CREATE TABLE IF NOT EXISTS clothes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER DEFAULT 0,
                season TEXT DEFAULT 'all',
                image_path TEXT DEFAULT '',
                owned INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS outfits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                items TEXT NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                clothing_id INTEGER NOT NULL
            );
            """
        )
        self.connection.commit()
        return True

    def seed_demo_clothes(self):
        cursor = self.connection.cursor()
        count = cursor.execute("SELECT COUNT(*) AS count FROM clothes").fetchone()["count"]
        if count == 0:
            sample_items = [
                ("Rain Jacket", "outerwear", 50, "winter", "assets/clothes/rain_jacket.png", 1),
                ("Classic Tee", "top", 20, "all", "assets/clothes/tee.png", 1),
                ("Denim Skirt", "bottom", 35, "summer", "assets/clothes/skirt.png", 1),
                ("Leather Boots", "shoes", 40, "winter", "assets/clothes/boots.png", 1),
            ]
            cursor.executemany(
                "INSERT INTO clothes (name, category, price, season, image_path, owned) VALUES (?, ?, ?, ?, ?, ?)",
                sample_items,
            )
            self.connection.commit()
            return True
        return False

    def add_user(self, username: str, password: str):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, coins, xp, level) VALUES (?, ?, 100, 0, 1)",
            (username.strip(), hash_password(password)),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_user(self, username: str):
        row = self.connection.execute(
            "SELECT * FROM users WHERE username COLLATE NOCASE = ?",
            (username.strip(),),
        ).fetchone()
        return dict(row) if row else None

    def update_password(self, user_id: int, password: str):
        self.connection.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hash_password(password), user_id),
        )
        self.connection.commit()

    def add_clothing(self, name: str, category: str, price: int, season: str = "all", image_path: str = ""):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO clothes (name, category, price, season, image_path, owned) VALUES (?, ?, ?, ?, ?, 1)",
            (name, category, price, season, image_path),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_clothes(self, season: Optional[str] = None, search: Optional[str] = None):
        query = "SELECT * FROM clothes WHERE 1=1"
        params = []
        if season:
            query += " AND season = ?"
            params.append(season)
        if search:
            query += " AND name LIKE ?"
            params.append(f"%{search}%")
        rows = self.connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def save_outfit(self, user_id: int, name: str, items: list):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO outfits (user_id, name, items) VALUES (?, ?, ?)",
            (user_id, name, ",".join(items)),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_outfits(self, user_id: int):
        rows = self.connection.execute(
            "SELECT * FROM outfits WHERE user_id = ? ORDER BY id DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def add_achievement(self, user_id: int, title: str):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO achievements (user_id, title, completed) VALUES (?, ?, 1)",
            (user_id, title),
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_achievements(self, user_id: int):
        rows = self.connection.execute(
            "SELECT * FROM achievements WHERE user_id = ? ORDER BY id DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def buy_clothing(self, user_id: int, clothing_id: int):
        user_row = self.connection.execute("SELECT coins FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user_row:
            return False
        clothing_row = self.connection.execute("SELECT price FROM clothes WHERE id = ?", (clothing_id,)).fetchone()
        if not clothing_row:
            return False
        price = clothing_row["price"]
        if user_row["coins"] < price:
            return False
        self.connection.execute("UPDATE users SET coins = coins - ? WHERE id = ?", (price, user_id))
        self.connection.execute("INSERT INTO inventory (user_id, clothing_id) VALUES (?, ?)", (user_id, clothing_id))
        self.connection.commit()
        return True

    def update_user_coins(self, user_id: int, delta: int):
        self.connection.execute("UPDATE users SET coins = coins + ? WHERE id = ?", (delta, user_id))
        self.connection.commit()

    def get_inventory(self, user_id: int):
        rows = self.connection.execute(
            "SELECT clothing_id FROM inventory WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        return [row["clothing_id"] for row in rows]
