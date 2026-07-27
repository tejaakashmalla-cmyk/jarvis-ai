import sqlite3


class JarvisDB:

    def __init__(self):

        self.conn = sqlite3.connect(
            "jarvis.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS memory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT,

            key TEXT,

            value TEXT

        )

        """)

        self.conn.commit()