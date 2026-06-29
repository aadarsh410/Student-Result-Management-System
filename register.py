from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys
import hashlib

class RegisterPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Result Management System")
        self.root.geometry("1366x768+0+0")
        self.root.resizable(False, False)

        # Load background image
        try:
            self.bg_image = Image.open("background.jpg")
            self.bg_image = self.bg_image.resize((1366, 768), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            self.root.config(bg="#dfe6e9")

        # Center frame
        frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=450)

        # Logo
        try:
            self.logo_img = Image.open("logo.png")
            self.logo_img = self.logo_img.resize((80, 80), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
            self.logo_label = Label(frame, image=self.logo_photo, bg="white")
            self.logo_label.image = self.logo_photo
            self.logo_label.pack(pady=(15, 5))
        except FileNotFoundError:
            pass

        title = Label(frame, text="Register", font=("Helvetica", 20, "bold"), bg="white", fg="#2d3436")
        title.pack(pady=(0, 20))

        # Variables
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_confirm = StringVar()

        # Username
        Label(frame, text="Username", font=("Helvetica", 12), bg="white").pack(anchor="w", padx=20)
        Entry(frame, textvariable=self.var_username, font=("Helvetica", 12), bg="#f1f2f6").pack(padx=20, pady=(0, 10), fill=X)

        # Password
        Label(frame, text="Password", font=("Helvetica", 12), bg="white").pack(anchor="w", padx=20)
        Entry(frame, textvariable=self.var_password, font=("Helvetica", 12), bg="#f1f2f6", show="*").pack(padx=20, pady=(0, 10), fill=X)

        # Confirm Password
        Label(frame, text="Confirm Password", font=("Helvetica", 12), bg="white").pack(anchor="w", padx=20)
        Entry(frame, textvariable=self.var_confirm, font=("Helvetica", 12), bg="#f1f2f6", show="*").pack(padx=20, pady=(0, 20), fill=X)

        # Register Button
        Button(frame, text="Register", font=("Helvetica", 12, "bold"), bg="#0984e3", fg="white",
               command=self.register_user).pack(pady=5, ipadx=10, ipady=5)

        # Back to login
        Button(frame, text="Back to Login", font=("Helvetica", 10), bg="white", fg="#0984e3",
               command=self.back_to_login).pack(pady=(10, 0))

        # Create DB table if not exists
        self.create_db()

    def create_db(self):
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self):
        username = self.var_username.get().strip()
        password = self.var_password.get().strip()
        confirm = self.var_confirm.get().strip()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.root)
            return

        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        (username, self.hash_password(password)))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!", parent=self.root)
            self.back_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!", parent=self.root)

    def back_to_login(self):
        self.root.destroy()
        os.system(f'"{sys.executable}" login.py')

if __name__ == "__main__":
    root = Tk()
    app = RegisterPage(root)
    root.mainloop()
