"""SQLite-сховище записів."""
import sqlite3
from datetime import datetime

FMT = "%Y-%m-%d %H:%M"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    phone TEXT
);
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    barber_id TEXT NOT NULL,
    service_id TEXT NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    reminded INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_bookings_start ON bookings(start);
"""


class DB:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    # --- users ---
    def upsert_user(self, user_id: int, name: str, username: str | None):
        self.conn.execute(
            "INSERT INTO users(user_id, name, username) VALUES(?,?,?) "
            "ON CONFLICT(user_id) DO UPDATE SET name=excluded.name, username=excluded.username",
            (user_id, name, username))
        self.conn.commit()

    def set_phone(self, user_id: int, phone: str):
        self.conn.execute("UPDATE users SET phone=? WHERE user_id=?", (phone, user_id))
        self.conn.commit()

    def get_user(self, user_id: int):
        return self.conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()

    # --- bookings ---
    def busy(self, barber_id: str, day: str) -> list[tuple[datetime, datetime]]:
        rows = self.conn.execute(
            "SELECT start, end FROM bookings WHERE barber_id=? AND status='active' AND start LIKE ?",
            (barber_id, day + "%")).fetchall()
        return [(datetime.strptime(r["start"], FMT), datetime.strptime(r["end"], FMT)) for r in rows]

    def is_free(self, barber_id: str, start: datetime, end: datetime) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM bookings WHERE barber_id=? AND status='active' AND start < ? AND end > ?",
            (barber_id, end.strftime(FMT), start.strftime(FMT))).fetchone()
        return row is None

    def create(self, user_id, barber_id, service_id, start: datetime, end: datetime,
               now: datetime, reminded: int = 0) -> int | None:
        """Створює запис, якщо час досі вільний (атомарно). Повертає id або None."""
        with self.conn:
            self.conn.execute("BEGIN IMMEDIATE")
            if not self.is_free(barber_id, start, end):
                return None
            cur = self.conn.execute(
                "INSERT INTO bookings(user_id, barber_id, service_id, start, end, reminded, created_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (user_id, barber_id, service_id, start.strftime(FMT), end.strftime(FMT),
                 reminded, now.strftime(FMT)))
            return cur.lastrowid

    def get(self, booking_id: int):
        return self.conn.execute(
            "SELECT b.*, u.name AS user_name, u.username, u.phone FROM bookings b "
            "LEFT JOIN users u ON u.user_id=b.user_id WHERE b.id=?", (booking_id,)).fetchone()

    def cancel(self, booking_id: int) -> bool:
        cur = self.conn.execute(
            "UPDATE bookings SET status='cancelled' WHERE id=? AND status='active'", (booking_id,))
        self.conn.commit()
        return cur.rowcount == 1

    def user_upcoming(self, user_id: int, now: datetime):
        return self.conn.execute(
            "SELECT * FROM bookings WHERE user_id=? AND status='active' AND start >= ? ORDER BY start",
            (user_id, now.strftime(FMT))).fetchall()

    def between(self, start: datetime, end: datetime):
        return self.conn.execute(
            "SELECT b.*, u.name AS user_name, u.username, u.phone FROM bookings b "
            "LEFT JOIN users u ON u.user_id=b.user_id "
            "WHERE b.status='active' AND b.start >= ? AND b.start < ? ORDER BY b.start",
            (start.strftime(FMT), end.strftime(FMT))).fetchall()

    def set_reminded(self, booking_id: int, level: int):
        self.conn.execute("UPDATE bookings SET reminded=? WHERE id=?", (level, booking_id))
        self.conn.commit()

    def stats(self, since: datetime):
        return self.conn.execute(
            "SELECT COUNT(*) AS n, COUNT(DISTINCT user_id) AS clients FROM bookings "
            "WHERE status='active' AND created_at >= ?", (since.strftime(FMT),)).fetchone()
