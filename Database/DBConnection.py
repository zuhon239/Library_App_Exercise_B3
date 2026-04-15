"""
Layer 4 - Database Layer
Responsible for managing the SQLite database connection.
All other layers use this module to get a connection.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    """Create all tables if they do not exist yet."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Books (
            BookId    INTEGER PRIMARY KEY AUTOINCREMENT,
            Title     TEXT    NOT NULL,
            Author    TEXT    NOT NULL,
            Quantity  INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS Members (
            MemberId  INTEGER PRIMARY KEY AUTOINCREMENT,
            FullName  TEXT    NOT NULL,
            Email     TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS BorrowRecords (
            RecordId   INTEGER PRIMARY KEY AUTOINCREMENT,
            BookId     INTEGER NOT NULL,
            MemberId   INTEGER NOT NULL,
            BorrowDate TEXT    NOT NULL,
            ReturnDate TEXT,
            FOREIGN KEY (BookId)   REFERENCES Books(BookId),
            FOREIGN KEY (MemberId) REFERENCES Members(MemberId)
        );
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")
