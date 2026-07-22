import os
import tempfile
import unittest

from managers.database_manager import DatabaseManager


class DatabaseManagerTests(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.mkdtemp(prefix="style_studio_", dir=".")
        self.db_path = os.path.join(temp_dir, "test_wardrobe.db")
        self.manager = DatabaseManager(self.db_path)

    def test_create_tables_and_add_user(self):
        self.manager.create_tables()
        self.manager.add_user("alice", "secret")

        user = self.manager.get_user("alice")
        self.assertEqual(user["username"], "alice")
        self.assertEqual(user["coins"], 100)
        self.assertEqual(user["xp"], 0)

    def test_add_clothing_and_fetch_by_season(self):
        self.manager.create_tables()
        self.manager.add_clothing(
            name="Rain Jacket",
            category="outerwear",
            price=50,
            season="winter",
            image_path="assets/clothes/jacket.png",
        )

        clothes = self.manager.get_clothes(season="winter")
        self.assertEqual(len(clothes), 1)
        self.assertEqual(clothes[0]["name"], "Rain Jacket")

    def test_save_outfit(self):
        self.manager.create_tables()
        self.manager.add_user("bob", "pass")
        outfit_id = self.manager.save_outfit(1, "Casual", ["top", "bottom", "shoes"])
        self.assertTrue(outfit_id > 0)


if __name__ == "__main__":
    unittest.main()
