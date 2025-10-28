# db.py
import sqlite3
import hashlib
import os

# Tên file database SQLite (sẽ tự động tạo nếu chưa có)
DB_NAME = "users.db"

def get_connection():
    """Kết nối đến database (nếu chưa có thì SQLite sẽ tự tạo)."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Khởi tạo bảng users nếu chưa có."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def hash_password(pw: str) -> str:
    """Mã hoá mật khẩu bằng SHA-256."""
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def create_user(email: str, password: str) -> bool:
    """
    Thêm tài khoản mới.
    Trả về True nếu tạo thành công.
    Trả về False nếu email đã tồn tại.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Email bị trùng (UNIQUE)
        return False

def check_login(email: str, password: str) -> bool:
    """
    Kiểm tra đăng nhập.
    Trả về True nếu email và password đúng.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT password_hash FROM users WHERE email = ?",
        (email,)
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return False

    stored_hash = row[0]
    return stored_hash == hash_password(password)
