from database.db import JarvisDB


class MemoryRepository:

    def __init__(self):

        self.db = JarvisDB()

    def save(self, category, key, value):

        self.db.cursor.execute(
            """
            INSERT INTO memory(category,key,value)
            VALUES(?,?,?)
            """,
            (category, key, value)
        )

        self.db.conn.commit()

    def get(self, key):

        self.db.cursor.execute(
            """
            SELECT value
            FROM memory
            WHERE key=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (key,)
        )

        row = self.db.cursor.fetchone()

        if row:
            return row[0]

        return None

    def all(self):

        self.db.cursor.execute(
            "SELECT category,key,value FROM memory"
        )

        return self.db.cursor.fetchall()