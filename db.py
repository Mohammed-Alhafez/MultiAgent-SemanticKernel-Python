"""
Database Module for Multi-Agent Task Management System

This module handles all database operations including task management and
chat history storage. It provides functions for initializing the database,
managing tasks, and storing conversation history.

Author: MultiAgent-SemanticKernel-Python
"""

import sqlite3
from typing import List, Tuple, Optional

# Database file path
DB_PATH = "tasks.db"


def init_chat_history_table():
    """
    Initialize the chat history table in the database.
    
    Creates a table to store conversation history including session IDs,
    roles (user/agent), agent names, content, and timestamps.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                agent_name TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def init_db():
    """
    Initialize the main database and create the tasks table.
    
    Creates a table to store task information including employee assignments,
    descriptions, due dates, and completion status.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee TEXT NOT NULL,
                description TEXT NOT NULL,
                due_date TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.commit()


def execute_query(query: str, params: Tuple = (), fetch: bool = False) -> List[Tuple]:
    """
    Execute a database query with optional parameter binding.
    
    Args:
        query: SQL query string
        params: Tuple of parameters for the query
        fetch: Whether to fetch and return results
        
    Returns:
        List of tuples containing query results if fetch=True, empty list otherwise
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetch:
            return cursor.fetchall()
        return []


def store_chat_message(session_id: str, role: str, agent_name: Optional[str], content: str):
    """
    Store a chat message in the database.
    
    Args:
        session_id: Unique identifier for the conversation session
        role: Role of the message sender (user, agent, function)
        agent_name: Name of the agent (None for user messages)
        content: The message content
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (session_id, role, agent_name, content)
            VALUES (?, ?, ?, ?)
        """, (session_id, role, agent_name, content))
        conn.commit()


def get_chat_history(session_id: str) -> List[Tuple]:
    """
    Retrieve chat history for a specific session.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        List of tuples containing role, agent_name, content, and timestamp
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, agent_name, content, timestamp
            FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """, (session_id,))
        return cursor.fetchall()
