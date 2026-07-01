from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import hashlib
import os
import sys
import subprocess
import sqlite3

from database import get_connection, initialize_database


class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Result Management System")
        self.root.geometry("1366x768+0+0")
        self.root.resizable(False, False)

        # Ensure database exists
        initialize_database()

        # ================= Background =================
        try:
            bg = Image.open("background.jpg")
            bg = bg.resize((1366, 768), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg)

            Label(self.root, image=self.bg_photo).place(
                x=0, y=0, relwidth=1, relheight=1
            )
        except FileNotFoundError:
            self.root.config(bg="#dfe6e9")

        # ================= Register Frame =================
        frame = Frame(
            self.root,
            bg="white",
            bd=2,
            relief=RIDGE
        )

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER,
            width=400,
            height=450
        )

        # ================= Logo =================
        try:
            logo = Image.open("logo.png")
            logo = logo.resize((80, 80), Image.LANCZOS)

            self.logo_photo = ImageTk.PhotoImage(logo)

            Label(
                frame,
                image=self.logo_photo,
                bg="white"
            ).pack(pady=(15, 5))

        except FileNotFoundError:
            pass

        Label(
            frame,
            text="Register",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg="#2d3436"
        ).pack(pady=(0, 20))

        # ================= Variables =================
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_confirm = StringVar()

        # Username
        Label(frame, text="Username", bg="white",
              font=("Helvetica", 12)).pack(anchor="w", padx=20)

        Entry(
            frame,
            textvariable=self.var_username,
            font=("Helvetica", 12),
            bg="#f1f2f6"
        ).pack(fill=X, padx=20, pady=(0, 10))

        # Password
        Label(frame, text="Password", bg="white",
              font=("Helvetica", 12)).pack(anchor="w", padx=20)

        Entry(
            frame,
            textvariable=self.var_password,
            show="*",
            font=("Helvetica", 12),
            bg="#f1f2f6"
        ).pack(fill=X, padx=20, pady=(0, 10))

        # Confirm Password
        Label(
            frame,
            text="Confirm Password",
            bg="white",
            font=("Helvetica", 12)
        ).pack(anchor="w", padx=20)

        Entry(
            frame,
            textvariable=self.var_confirm,
            show="*",
            font=("Helvetica", 12),
            bg="#f1f2f6"
        ).pack(fill=X, padx=20, pady=(0, 20))

        # Register Button
        Button(
            frame,
            text="Register",
            command=self.register_user,
            font=("Helvetica", 12, "bold"),
            bg="#0984e3",
            fg="white"
        ).pack(ipadx=10, ipady=5)

        Button(
            frame,
            text="Back to Login",
            command=self.back_to_login,
            font=("Helvetica", 10),
            bg="white",
            fg="#0984e3"
        ).pack(pady=10)

    # ============================================

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ============================================

    def register_user(self):

        username = self.var_username.get().strip()
        password = self.var_password.get().strip()
        confirm = self.var_confirm.get().strip()

        if not username or not password or not confirm:
            messagebox.showerror(
                "Error",
                "All fields are required!",
                parent=self.root
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Error",
                "Passwords do not match!",
                parent=self.root
            )
            return

        con = None

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                "SELECT id FROM users WHERE username=?",
                (username,)
            )

            if cur.fetchone():
                messagebox.showerror(
                    "Error",
                    "Username already exists!",
                    parent=self.root
                )
                return

            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, self.hash_password(password))
            )

            con.commit()

            messagebox.showinfo(
                "Success",
                "Registration Successful!",
                parent=self.root
            )

            self.back_to_login()

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.root
            )

        finally:
            if con:
                con.close()

    # ============================================

    def back_to_login(self):

        self.root.destroy()

        subprocess.Popen([sys.executable, "login.py"])


if __name__ == "__main__":
    root = Tk()
    RegisterPage(root)
    root.mainloop()