import sqlite3
import json

class PersonaService:
    def __init__(self, db_path="./roberto_personas.db"):
        self.db_path = db_path
        self._create_table()

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                name TEXT PRIMARY KEY,
                description TEXT
            )
        """)
        conn.commit()
        conn.close()

    def set_persona(self, name: str, description: str):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO personas (name, description) VALUES (?, ?)", (name, description))
        except sqlite3.IntegrityError:
            cursor.execute("UPDATE personas SET description = ? WHERE name = ?", (description, name))
        conn.commit()
        conn.close()

    def get_persona(self, name: str) -> str | None:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM personas WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row["description"]
        return None

    def list_personas(self) -> list[str]:
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM personas")
        rows = cursor.fetchall()
        conn.close()
        return [row["name"] for row in rows]

    def delete_persona(self, name: str):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas WHERE name = ?", (name,))
        conn.commit()
        conn.close()

    def clear_all_personas(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personas")
        conn.commit()
        conn.close()
