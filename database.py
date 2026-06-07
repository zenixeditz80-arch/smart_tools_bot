import sqlite3
from datetime import datetime

DB_NAME = "smarttools.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referrals INTEGER DEFAULT 0,
            premium INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0,
            joined_at TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            referrer_id INTEGER,
            created_at TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            conversion_type TEXT,
            created_at TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            created_at TEXT
        )
        """)

        conn.commit()


def add_user(user_id, username=""):

    with get_connection() as conn:

        conn.execute(
            """
            INSERT OR IGNORE INTO users(
                user_id,
                username,
                joined_at
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                username,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        conn.commit()


def get_user(user_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return cursor.fetchone()


def user_exists(user_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return cursor.fetchone() is not None


def get_user_info(user_id):

    return get_user(user_id)


def get_all_users():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT user_id
            FROM users
            """
        )

        return cursor.fetchall()


def get_total_users():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        )

        return cursor.fetchone()[0]


def ban_user_db(user_id):

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE users
            SET banned = 1
            WHERE user_id = ?
            """,
            (user_id,)
        )

        conn.commit()

    return True


def unban_user_db(user_id):

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE users
            SET banned = 0
            WHERE user_id = ?
            """,
            (user_id,)
        )

        conn.commit()

    return True


def is_banned(user_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT banned
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        if result:
            return result[0] == 1

        return False


def add_referral(
    user_id,
    referrer_id
):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO referrals(
                user_id,
                referrer_id,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                referrer_id,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        cursor.execute(
            """
            UPDATE users
            SET referrals = referrals + 1
            WHERE user_id = ?
            """,
            (referrer_id,)
        )

        conn.commit()


def get_referral_count(user_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT referrals
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return 0


def add_conversion(
    user_id,
    conversion_type
):

    with get_connection() as conn:

        conn.execute(
            """
            INSERT INTO conversions(
                user_id,
                conversion_type,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                conversion_type,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        conn.commit()


def get_total_conversions():

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM conversions
            """
        )

        return cursor.fetchone()[0]


def add_log(event):

    with get_connection() as conn:

        conn.execute(
            """
            INSERT INTO logs(
                event,
                created_at
            )
            VALUES (?, ?)
            """,
            (
                event,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        conn.commit()


def get_logs(limit=50):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()


def set_premium(
    user_id,
    enabled=True
):

    value = 1 if enabled else 0

    with get_connection() as conn:

        conn.execute(
            """
            UPDATE users
            SET premium = ?
            WHERE user_id = ?
            """,
            (
                value,
                user_id
            )
        )

        conn.commit()


def is_premium(user_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT premium
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        if result:
            return result[0] == 1

        return False


init_db()