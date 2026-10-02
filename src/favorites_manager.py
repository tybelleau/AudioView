from pathlib import Path

class FavoritesManager:
    def __init__(self, database):
        self.database = database

    def is_favorite(self, file_path):
        cursor = self.database.connection.cursor()

        cursor.execute(
            "SELECT 1 FROM favorites WHERE file_path = ?",
            (str(file_path),)
        )

        return cursor.fetchone() is not None

    def add_favorite(self, file_path):
        cursor = self.database.connection.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO favorites (file_path) VALUES (?)",
            (str(file_path),)
        )

        self.database.connection.commit()

    def remove_favorite(self, file_path):
        cursor = self.database.connection.cursor()

        cursor.execute(
            "DELETE FROM favorites WHERE file_path = ?",
            (str(file_path),)
        )

        self.database.connection.commit()

    def toggle_favorite(self, file_path):
        if self.is_favorite(file_path):
            self.remove_favorite(file_path)
        else:
            self.add_favorite(file_path)

    def get_favorites(self):
        cursor = self.database.connection.cursor()
        cursor.execute("SELECT file_path FROM favorites")

        return {
            Path(row[0])
            for row in cursor.fetchall()
        }