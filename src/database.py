import sqlite3
from pathlib import Path

from PySide6.QtCore import QStandardPaths


class Database:
    def __init__(self):
        app_data_path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.AppDataLocation
            )
        )

        app_data_path.mkdir(parents=True, exist_ok=True)

        self.db_path = app_data_path / "wavemap.db"

        self.connection = sqlite3.connect(self.db_path)

        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE
            )
        """)

        self.connection.commit()

    def close(self):
        self.connection.close()