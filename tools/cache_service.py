import sqlite3
import json
import os
import numpy as np
from llama_index.embeddings.ollama import OllamaEmbedding
from datetime import datetime, timedelta

class CacheService:
    def __init__(self, embed_model: OllamaEmbedding, db_path="./roberto_cache.db", similarity_threshold=0.7, ttl_minutes=15):
        self.db_path = db_path
        self.embed_model = embed_model
        self.similarity_threshold = similarity_threshold
        self.ttl_minutes = ttl_minutes
        self._create_table()

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                query TEXT PRIMARY KEY,
                query_embedding BLOB,
                response TEXT,
                timestamp INTEGER,
                is_temporary INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def _get_embedding(self, text: str) -> list[float]:
        return self.embed_model.get_text_embedding(text)

    def get(self, query: str) -> str | None:
        query_embedding = np.array(self._get_embedding(query))

        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT query, query_embedding, response, timestamp, is_temporary FROM responses")
        rows = cursor.fetchall()
        conn.close()

        best_match_response = None
        highest_similarity = -1
        current_time = datetime.now().timestamp()

        for row in rows:
            # Check for expiration if it's a temporary entry
            if row["is_temporary"] == 1:
                if current_time - row["timestamp"] > self.ttl_minutes * 60:
                    # Entry expired, skip it
                    continue

            stored_query_embedding = np.frombuffer(row["query_embedding"], dtype=np.float32)
            similarity = np.dot(query_embedding, stored_query_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(stored_query_embedding))

            if similarity > highest_similarity and similarity >= self.similarity_threshold:
                highest_similarity = similarity
                best_match_response = row["response"]
        
        return best_match_response

    def set(self, query: str, response: str, is_temporary: bool = False):
        query_embedding = np.array(self._get_embedding(query)).astype(np.float32).tobytes()
        timestamp = datetime.now().timestamp()
        temp_flag = 1 if is_temporary else 0

        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO responses (query, query_embedding, response, timestamp, is_temporary) VALUES (?, ?, ?, ?, ?)", (query, query_embedding, response, timestamp, temp_flag))
        except sqlite3.IntegrityError:
            # If query already exists, update it
            cursor.execute("UPDATE responses SET query_embedding = ?, response = ?, timestamp = ?, is_temporary = ? WHERE query = ?", (query_embedding, response, timestamp, temp_flag, query))
        conn.commit()
        conn.close()

    def clear(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM responses")
        conn.commit()
        conn.close()
        print(f"Cache cleared from {self.db_path}")



