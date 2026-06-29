from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")

        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.var_percentage = StringVar()

        # Title
        title = Label(self.root, text="ADD STUDENT RESULT", font=("goudy old style", 24, "bold"),
              bg="#080354", fg="white")
        title.pack(side=TOP, fill=X)


        # Labels & Entries
        self.make_label("Roll No.", 50, 100)
        Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 16), bg="lightyellow").place(x=200, y=100, width=250)

        self.make_label("Name", 50, 160)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 16), bg="lightyellow", state="readonly").place(x=200, y=160, width=350)

        self.make_label("Course", 50, 220)
        Entry(self.root, textvariable=self.var_course, font=("goudy old style", 16), bg="lightyellow", state="readonly").place(x=200, y=220, width=250)

        self.make_label("Marks Obtained", 50, 280)
        Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 16), bg="lightyellow").place(x=230, y=280, width=180)

        self.make_label("Full Marks", 50, 340)
        Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 16), bg="lightyellow").place(x=230, y=340, width=180)

        self.make_label("Percentage", 50, 400)
        Entry(self.root, textvariable=self.var_percentage, font=("goudy old style", 16), bg="lightyellow", state="readonly").place(x=200, y= 400, width=180)
 
        # Image (Adjusted to fit bigger resolution)
        try:
            self.re_img = Image.open("images/result img 1.jpg")
            self.re_img = self.re_img.resize((500, 300))
            self.re_img = ImageTk.PhotoImage(self.re_img)
            self.lbl_bg = Label(self.root, image=self.re_img, bd=0)
            self.lbl_bg.place(x=630, y=180, width=780, height=450)
        except:
            pass 

        # Buttons
        self.make_button("Search", 500, 100, "#03a9f4", self.search_student, 120, 35)
        self.make_button("Save", 50, 460, "#080354", self.add)
        self.make_button("Clear", 200, 460, "#607d8b", self.clear)

        # Create database table
        self.create_table()

    def make_label(self, text, x, y):
        Label(self.root, text=text, font=("goudy old style", 16, "bold"), bg="white").place(x=x, y=y)

    def make_button(self, text, x, y, color, command, width=130, height=40):
        Button(self.root, text=text, font=("goudy old style", 16, "bold"), bg=color, fg="white", cursor="hand2",
               command=command).place(x=x, y=y, width=width, height=height)

    def create_table(self):
        con = sqlite3.connect("yadavproject.db")
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS result")
        cur.execute("""CREATE TABLE result (
                        roll TEXT PRIMARY KEY,
                        name TEXT,
                        course TEXT,
                        marks TEXT,
                        full_marks TEXT,
                        percentage TEXT)""")
        con.commit()
        con.close()

    def search_student(self):
        con = sqlite3.connect("yadavproject.db")
        cur = con.cursor()
        cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
        row = cur.fetchone()
        con.close()
        if row:
            self.var_name.set(row[0])
            self.var_course.set(row[1])
        else:
            messagebox.showerror("Error", "No record found for this Roll No.", parent=self.root)

    def add(self):
        if self.var_roll.get() == "" or self.var_marks.get() == "" or self.var_full_marks.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return
        try:
            percentage = (float(self.var_marks.get()) / float(self.var_full_marks.get())) * 100
            self.var_percentage.set(f"{percentage:.2f}%")
            con = sqlite3.connect("yadavproject.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Result already exists for this Roll No.", parent=self.root)
            else:
                cur.execute("INSERT INTO result VALUES(?,?,?,?,?,?)",
                            (self.var_roll.get(), self.var_name.get(), self.var_course.get(),
                             self.var_marks.get(), self.var_full_marks.get(), self.var_percentage.get()))
                con.commit()
                messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
                self.clear()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self.root)

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        self.var_percentage.set("")


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()
