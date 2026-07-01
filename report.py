from tkinter import *
from tkinter import messagebox
from database import get_connection


class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        # =========================
        # Variables
        # =========================
        self.var_search = StringVar()

        # =========================
        # Title
        # =========================
        title = Label(
            self.root,
            text="VIEW STUDENT RESULT",
            font=("goudy old style", 24, "bold"),
            bg="#080354",
            fg="white"
        )
        title.pack(side=TOP, fill=X)

        # =========================
        # Search Section
        # =========================
        Label(
            self.root,
            text="Enter Roll No.",
            font=("goudy old style", 18, "bold"),
            bg="white"
        ).place(x=250, y=90)

        Entry(
            self.root,
            textvariable=self.var_search,
            font=("goudy old style", 18),
            bg="lightyellow"
        ).place(x=470, y=90, width=200)

        Button(
            self.root,
            text="Search",
            font=("goudy old style", 15, "bold"),
            bg="#03A9F4",
            fg="white",
            cursor="hand2",
            command=self.search_student
        ).place(x=700, y=88, width=120, height=35)

        Button(
            self.root,
            text="Clear",
            font=("goudy old style", 15, "bold"),
            bg="gray",
            fg="white",
            cursor="hand2",
            command=self.clear
        ).place(x=840, y=88, width=120, height=35)

        # =========================
        # Headings
        # =========================
        headers = [
            "Roll No",
            "Name",
            "Course",
            "Marks",
            "Total",
            "Percentage"
        ]

        x = 180

        for h in headers:
            Label(
                self.root,
                text=h,
                font=("goudy old style", 15, "bold"),
                bg="#080354",
                fg="white",
                relief=RIDGE
            ).place(x=x, y=220, width=160, height=40)

            x += 160

        # =========================
        # Value Labels
        # =========================
        self.roll = Label(self.root, bg="white", relief=RIDGE)
        self.roll.place(x=180, y=260, width=160, height=45)

        self.name = Label(self.root, bg="white", relief=RIDGE)
        self.name.place(x=340, y=260, width=160, height=45)

        self.course = Label(self.root, bg="white", relief=RIDGE)
        self.course.place(x=500, y=260, width=160, height=45)

        self.marks = Label(self.root, bg="white", relief=RIDGE)
        self.marks.place(x=660, y=260, width=160, height=45)

        self.full = Label(self.root, bg="white", relief=RIDGE)
        self.full.place(x=820, y=260, width=160, height=45)

        self.per = Label(self.root, bg="white", relief=RIDGE)
        self.per.place(x=980, y=260, width=160, height=45)

        # =========================
        # Delete Button
        # =========================
        Button(
            self.root,
            text="Delete Result",
            font=("goudy old style", 15, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            command=self.delete_result
        ).place(x=570, y=360, width=180, height=45)
    def search_student(self):
        con = get_connection()

        try:
            cur = con.cursor()

            cur.execute(
                "SELECT * FROM result WHERE roll=?",
                (self.var_search.get(),)
            )

            row = cur.fetchone()

            if row:
                self.roll.config(text=row[0])
                self.name.config(text=row[1])
                self.course.config(text=row[2])
                self.marks.config(text=row[3])
                self.full.config(text=row[4])
                self.per.config(text=row[5])
            else:
                messagebox.showerror(
                    "Error",
                    "No Record Found",
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

    # ================= Clear =================
    def clear(self):
        self.var_search.set("")

        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")

    # ================= Delete =================
    def delete_result(self):

        if self.var_search.get() == "":
            messagebox.showerror(
                "Error",
                "Please enter Roll Number",
                parent=self.root
            )
            return

        con = get_connection()

        try:
            cur = con.cursor()

            cur.execute(
                "DELETE FROM result WHERE roll=?",
                (self.var_search.get(),)
            )

            con.commit()

            if cur.rowcount > 0:
                messagebox.showinfo(
                    "Success",
                    "Result Deleted Successfully",
                    parent=self.root
                )
                self.clear()
            else:
                messagebox.showerror(
                    "Error",
                    "Record Not Found",
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


# ================= Main =================
if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()