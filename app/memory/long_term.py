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