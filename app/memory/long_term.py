import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


class LongTermMemory:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )

    def save_memory(
        self,
        memory_type: str,
        memory_key: str,
        memory_value: str,
    ):
        """
        Create a new memory or update an existing memory.
        """

        cursor = self.connection.cursor()

        query = """
            INSERT INTO memories
            (memory_type, memory_key, memory_value)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                memory_value = VALUES(memory_value),
                is_active = TRUE
        """

        cursor.execute(
            query,
            (memory_type, memory_key, memory_value),
        )

        self.connection.commit()

        cursor.close()
        
    def save_memory_with_conflict_resolution(
        self,
        memory_type: str,
        memory_key: str,
        memory_value: str,
    ):
        """
        Save a memory while resolving conflicts with the
        currently active memory for the same type and key.
        """

        cursor = self.connection.cursor()

        query = """
        SELECT id, memory_value
        FROM memories
        WHERE memory_type = %s
          AND memory_key = %s
          AND is_active = TRUE
        ORDER BY id DESC
        LIMIT 1
        """

        cursor.execute(
            query,
            (memory_type, memory_key),
        )

        existing_memory = cursor.fetchone()

        # Same value already exists.
        if (
            existing_memory is not None
            and existing_memory[1] == memory_value
        ):
            cursor.close()
            return "unchanged"

        # Deactivate conflicting active memory.
        if existing_memory is not None:
            cursor.execute(
                """
                UPDATE memories
                SET is_active = FALSE
                WHERE id = %s
                """,
                (existing_memory[0],),
            )

        # Insert the new active memory.
        cursor.execute(
            """
            INSERT INTO memories
            (memory_type, memory_key, memory_value, is_active)
            VALUES (%s, %s, %s, TRUE)
            """,
            (
                memory_type,
                memory_key,
                memory_value,
            ),
        )

        self.connection.commit()

        cursor.close()

        if existing_memory is None:
            return "created"

        return "updated"

    def get_memory(self, memory_key: str):
        """
        Retrieve an active memory by its key.
        """

        cursor = self.connection.cursor()

        query = """
            SELECT memory_type, memory_key, memory_value
            FROM memories
            WHERE memory_key = %s
              AND is_active = TRUE
            ORDER BY id DESC
            LIMIT 1
        """

        cursor.execute(
            query,
            (memory_key,),
        )

        result = cursor.fetchone()

        cursor.close()

        return result
    def get_active_memories(self):
        """
        Retrieve all currently active long-term memories.
        """

        cursor = self.connection.cursor()

        query = """
            SELECT memory_type, memory_key, memory_value
            FROM memories
            WHERE is_active = TRUE
            ORDER BY id ASC
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()

        return [
            {
                "memory_type": row[0],
                "memory_key": row[1],
                "memory_value": row[2],
            }
            for row in rows
        ]

    def deactivate_memory(
        self,
        memory_type: str,
        memory_key: str,
    ):
        """
        Deactivate an existing memory without deleting it.
        """

        cursor = self.connection.cursor()

        query = """
            UPDATE memories
            SET is_active = FALSE
            WHERE memory_type = %s
              AND memory_key = %s
              AND is_active = TRUE
        """

        cursor.execute(
            query,
            (memory_type, memory_key),
        )

        self.connection.commit()

        rows_updated = cursor.rowcount

        cursor.close()

        return rows_updated

    def update_memory(
        self,
        memory_key: str,
        memory_value: str,
    ):
        """
        Update an existing active memory.
        """

        cursor = self.connection.cursor()

        query = """
            UPDATE memories
            SET memory_value = %s
            WHERE memory_key = %s
              AND is_active = TRUE
        """

        cursor.execute(
            query,
            (memory_value, memory_key),
        )

        self.connection.commit()

        rows_updated = cursor.rowcount

        cursor.close()

        return rows_updated