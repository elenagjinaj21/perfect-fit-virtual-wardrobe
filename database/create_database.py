from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from managers.database_manager import DatabaseManager


if __name__ == "__main__":
    manager = DatabaseManager()
    manager.create_tables()
    print("Database created successfully.")
