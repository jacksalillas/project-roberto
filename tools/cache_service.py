import sqlite3
import json
import os
import numpy as np
from llama_index.embeddings.ollama import OllamaEmbedding

class CacheService:
    def __init__(self, embed_model: OllamaEmbedding, db_path="./roberto_cache.db", similarity_threshold=0.7):
        self.db_path = db_path
        self.embed_model = embed_model
        self.similarity_threshold = similarity_threshold
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
                response TEXT
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
        cursor.execute("SELECT query, query_embedding, response FROM responses")
        rows = cursor.fetchall()
        conn.close()

        best_match_response = None
        highest_similarity = -1

        for row in rows:
            stored_query_embedding = np.frombuffer(row["query_embedding"], dtype=np.float32)
            similarity = np.dot(query_embedding, stored_query_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(stored_query_embedding))

            if similarity > highest_similarity and similarity >= self.similarity_threshold:
                highest_similarity = similarity
                best_match_response = row["response"]
        
        return best_match_response

    def set(self, query: str, response: str):
        query_embedding = np.array(self._get_embedding(query)).astype(np.float32).tobytes()

        conn = self._get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO responses (query, query_embedding, response) VALUES (?, ?, ?)", (query, query_embedding, response))
        except sqlite3.IntegrityError:
            # If query already exists, update it
            cursor.execute("UPDATE responses SET query_embedding = ?, response = ? WHERE query = ?", (query_embedding, response, query))
        conn.commit()
        conn.close()

    def clear(self):
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM responses")
        conn.commit()
        conn.close()
        print(f"Cache cleared from {self.db_path}")



