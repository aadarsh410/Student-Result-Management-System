import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import hashlib
import os
import sys
import subprocess

from database import get_connection, initialize_database


# ======================================================
# Password Hashing
# ======================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ======================================================
# Login Function
# ======================================================

def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        )

        user = cur.fetchone()
        con.close()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome {username}")

            root.destroy()

            subprocess.Popen([sys.executable, "app.py"])

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ======================================================
# Open Register Window
# ======================================================

def open_register():
    root.destroy()
    subprocess.Popen([sys.executable, "register.py"])


# ======================================================
# Initialize Database
# ======================================================

initialize_database()


# ======================================================
# GUI
# ======================================================

root = tk.Tk()
root.title("Student Result Management System")
root.geometry("1366x768")
root.resizable(False, False)


# ======================================================
# Background
# ======================================================

if os.path.exists("background.jpg"):
    bg_img = Image.open("background.jpg")
    bg_img = bg_img.resize((1366, 768), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0)

else:
    root.config(bg="white")


# ======================================================
# Login Frame
# ======================================================

frame_login = tk.Frame(root, bg="white", bd=5, relief="ridge")
frame_login.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=400,
    height=350
)


# ======================================================
# Logo
# ======================================================

if os.path.exists("logo.png"):
    logo_img = Image.open("logo.png")
    logo_img = logo_img.resize((80, 80), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(
        frame_login,
        image=logo_photo,
        bg="white"
    )

    logo_label.image = logo_photo
    logo_label.pack(pady=10)


# ======================================================
# Title
# ======================================================

tk.Label(
    frame_login,
    text="Login",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#333333"
).pack(pady=10)


# ======================================================
# Username
# ======================================================

tk.Label(
    frame_login,
    text="Username",
    font=("Arial", 14),
    bg="white"
).pack(pady=5)

entry_username = tk.Entry(
    frame_login,
    font=("Arial", 14)
)

entry_username.pack(pady=5)


# ======================================================
# Password
# ======================================================

tk.Label(
    frame_login,
    text="Password",
    font=("Arial", 14),
    bg="white"
).pack(pady=5)

entry_password = tk.Entry(
    frame_login,
    font=("Arial", 14),
    show="*"
)

entry_password.pack(pady=5)


# ======================================================
# Buttons
# ======================================================

tk.Button(
    frame_login,
    text="Login",
    font=("Arial", 14),
    bg="#4CAF50",
    fg="white",
    width=15,
    command=login
).pack(pady=10)

tk.Button(
    frame_login,
    text="Register",
    font=("Arial", 14),
    bg="#2196F3",
    fg="white",
    width=15,
    command=open_register
).pack()


# ======================================================
# Run Application
# ======================================================

root.mainloop()