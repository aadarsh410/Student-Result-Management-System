from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from database import get_connection


class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        # ================= Variables =================
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.var_percentage = StringVar()
        self.var_grade = StringVar()

        # ================= Title =================
        title = Label(
            self.root,
            text="ADD STUDENT RESULT",
            font=("goudy old style", 24, "bold"),
            bg="#080354",
            fg="white"
        )
        title.pack(side=TOP, fill=X)

        # ================= Labels =================
        self.make_label("Roll No.", 50, 100)

        Entry(
            self.root,
            textvariable=self.var_roll,
            font=("goudy old style", 16),
            bg="lightyellow"
        ).place(x=220, y=100, width=220)

        self.make_label("Name", 50, 160)

        Entry(
            self.root,
            textvariable=self.var_name,
            font=("goudy old style", 16),
            state="readonly",
            bg="lightyellow"
        ).place(x=220, y=160, width=300)

        self.make_label("Course", 50, 220)

        Entry(
            self.root,
            textvariable=self.var_course,
            font=("goudy old style", 16),
            state="readonly",
            bg="lightyellow"
        ).place(x=220, y=220, width=220)

        self.make_label("Marks Obtained", 50, 280)

        Entry(
            self.root,
            textvariable=self.var_marks,
            font=("goudy old style", 16),
            bg="lightyellow"
        ).place(x=220, y=280, width=220)

        self.make_label("Full Marks", 50, 340)

        Entry(
            self.root,
            textvariable=self.var_full_marks,
            font=("goudy old style", 16),
            bg="lightyellow"
        ).place(x=220, y=340, width=220)

        self.make_label("Percentage", 50, 400)

        Entry(
            self.root,
            textvariable=self.var_percentage,
            font=("goudy old style", 16),
            state="readonly",
            bg="lightyellow"
        ).place(x=220, y=400, width=220)

        self.make_label("Grade", 50, 460)

        Entry(
            self.root,
            textvariable=self.var_grade,
            font=("goudy old style", 16),
            state="readonly",
            bg="lightyellow"
        ).place(x=220, y=460, width=220)

        # ================= Image =================
        try:
            self.re_img = Image.open("images/result img 1.jpg")
            self.re_img = self.re_img.resize((600, 400))
            self.re_img = ImageTk.PhotoImage(self.re_img)

            Label(
                self.root,
                image=self.re_img,
                bd=0
            ).place(x=650, y=150)

        except:
            pass

        # ================= Buttons =================
        Button(
            self.root,
            text="Search",
            font=("goudy old style", 15, "bold"),
            bg="#03a9f4",
            fg="white",
            cursor="hand2",
            command=self.search_student
        ).place(x=470, y=100, width=120, height=35)

        Button(
            self.root,
            text="Save",
            font=("goudy old style", 15, "bold"),
            bg="#080354",
            fg="white",
            cursor="hand2",
            command=self.add
        ).place(x=80, y=540, width=140, height=40)

        Button(
            self.root,
            text="Clear",
            font=("goudy old style", 15, "bold"),
            bg="gray",
            fg="white",
            cursor="hand2",
            command=self.clear
        ).place(x=250, y=540, width=140, height=40)

        self.create_table()

    # ================= Helper =================
    def make_label(self, text, x, y):
        Label(
            self.root,
            text=text,
            font=("goudy old style", 16, "bold"),
            bg="white"
        ).place(x=x, y=y)

    # ================= Database =================
    def create_table(self):
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS result(
                rid INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT,
                course TEXT,
                marks_obtained INTEGER,
                full_marks INTEGER,
                percentage REAL,
                grade TEXT
            )
        """)

        con.commit()
        con.close()
     # ================= Search Student =================
    def search_student(self):
        if self.var_roll.get().strip() == "":
            messagebox.showerror(
                "Error",
                "Please enter Roll Number",
                parent=self.root
            )
            return

        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute(
                "SELECT name, course FROM student WHERE roll=?",
                (self.var_roll.get(),)
            )

            row = cur.fetchone()

            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror(
                    "Error",
                    "Student not found",
                    parent=self.root
                )

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex),
                parent=self.root
            )

        finally:
            con.close()

    # ================= Save Result =================
    def add(self):
        if (
            self.var_roll.get() == "" or
            self.var_marks.get() == "" or
            self.var_full_marks.get() == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required",
                parent=self.root
            )
            return

        try:
            marks = float(self.var_marks.get())
            full = float(self.var_full_marks.get())

            percentage = (marks / full) * 100

            self.var_percentage.set(f"{percentage:.2f}")

            # Grade Calculation
            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 50:
                grade = "D"
            else:
                grade = "F"

            self.var_grade.set(grade)

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                "SELECT * FROM result WHERE roll=?",
                (self.var_roll.get(),)
            )

            row = cur.fetchone()

            if row:
                messagebox.showerror(
                    "Error",
                    "Result already exists",
                    parent=self.root
                )

            else:
                cur.execute("""
                    INSERT INTO result
                    (
                        roll,
                        course,
                        marks_obtained,
                        full_marks,
                        percentage,
                        grade
                    )
                    VALUES(?,?,?,?,?,?)
                """,
                (
                    self.var_roll.get(),
                    self.var_course.get(),
                    int(marks),
                    int(full),
                    percentage,
                    grade
                ))

                con.commit()

                messagebox.showinfo(
                    "Success",
                    "Result Added Successfully",
                    parent=self.root
                )

                self.clear()

            con.close()

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex),
                parent=self.root
            )

    # ================= Clear =================
    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        self.var_percentage.set("")
        self.var_grade.set("")


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()