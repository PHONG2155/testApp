import sqlite3
import hashlib
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


DB_NAME = "auth.db"


def hash_password(raw):
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            fullname TEXT
        )
    """)
    conn.commit()
    conn.close()


def register_user(username, password, confirm, fullname):
    if not username or not password or not confirm:
        return False, "Vui lòng nhập đầy đủ thông tin."
    if password != confirm:
        return False, "Mật khẩu nhập lại không khớp."
    if len(password) < 4:
        return False, "Mật khẩu phải >= 4 ký tự."
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password, fullname) VALUES (?, ?, ?)",
            (username, hash_password(password), fullname)
        )
        conn.commit()
        conn.close()
        return True, "Đăng ký thành công! Hãy đăng nhập."
    except sqlite3.IntegrityError:
        return False, "Tên đăng nhập đã tồn tại."
    except Exception as e:
        return False, f"Lỗi hệ thống: {e}"


def login_user(username, password):
    if not username or not password:
        return False, "Vui lòng nhập username & mật khẩu."
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT fullname FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    row = cur.fetchone()
    conn.close()
    if row:
        fullname = row[0] if row[0] else username
        return True, fullname
    else:
        return False, "Sai tài khoản hoặc mật khẩu."


# =======================
# Kivy Screens
# =======================

class LoginScreen(Screen):
    def do_login(self):
        u = self.ids.login_username.text.strip()
        p = self.ids.login_password.text
        ok, msg = login_user(u, p)
        if ok:
            # chuyển qua dashboard
            app = MDApp.get_running_app()
            app.current_user = msg
            self.manager.current = "dashboard"
        else:
            self.show_msg("Đăng nhập thất bại", msg)

    def go_register(self):
        self.manager.current = "register"

    def show_msg(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


class RegisterScreen(Screen):
    def do_register(self):
        u = self.ids.reg_username.text.strip()
        f = self.ids.reg_fullname.text.strip()
        p = self.ids.reg_password.text
        c = self.ids.reg_confirm.text

        ok, msg = register_user(u, p, c, f)
        self.show_msg("Kết quả", msg)

        if ok:
            # nếu đăng ký ok thì clear field và quay lại login
            self.ids.reg_username.text = ""
            self.ids.reg_fullname.text = ""
            self.ids.reg_password.text = ""
            self.ids.reg_confirm.text = ""
            self.manager.current = "login"

    def back_login(self):
        self.manager.current = "login"

    def show_msg(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


class DashboardScreen(Screen):
    welcome_text = StringProperty("")

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        self.welcome_text = f"Xin chào {app.current_user} 👋\nBạn đã đăng nhập thành công!"

    def logout(self):
        self.manager.current = "login"


class AuthApp(MDApp):
    current_user = ""

    def build(self):
        self.title = "AuthApp"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"  # bạn có thể đổi "Dark"

        init_db()
        return Builder.load_file("auth.kv")


if __name__ == "__main__":
    AuthApp().run()
