from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import get_connection


class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        # ================= Variables =================
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search_type = StringVar(value="Roll")
        self.var_search = StringVar()

        self.selected_roll = None

        # ================= Title =================
        title = Label(
            self.root,
            text="Student Management",
            font=("goudy old style", 20, "bold"),
            bg="#080354",
            fg="white"
        )
        title.place(x=0, y=0, relwidth=1, height=50)

        # ================= Left Side =================
        left_x = 20
        top_y = 70

        self.make_label("Roll No.", left_x, top_y)
        self.make_entry(self.var_roll, left_x + 130, top_y)

        self.make_label("Name", left_x, top_y + 40)
        self.make_entry(self.var_name, left_x + 130, top_y + 40)

        self.make_label("Email", left_x, top_y + 80)
        self.make_entry(self.var_email, left_x + 130, top_y + 80)

        self.make_label("Gender", left_x, top_y + 120)

        self.txt_gender = ttk.Combobox(
            self.root,
            textvariable=self.var_gender,
            values=("Select", "Male", "Female", "Other"),
            font=("goudy old style", 14),
            state="readonly",
            justify=CENTER
        )

        self.txt_gender.place(
            x=left_x + 130,
            y=top_y + 120,
            width=200
        )

        self.txt_gender.current(0)

        self.make_label("State", left_x, top_y + 160)
        self.make_entry(self.var_state, left_x + 130, top_y + 160, 150)

        self.make_label("City", left_x + 300, top_y + 160)
        self.make_entry(self.var_city, left_x + 360, top_y + 160, 120)

        self.make_label("Pin", left_x + 500, top_y + 160)
        self.make_entry(self.var_pin, left_x + 550, top_y + 160, 120)

        self.make_label("Address", left_x, top_y + 200)

        self.txt_address = Text(
            self.root,
            font=("goudy old style", 14),
            bg="lightyellow"
        )

        self.txt_address.place(
            x=150,
            y=top_y + 200,
            width=520,
            height=80
        )

        # ================= Right Side =================
        right_x = 700

        self.make_label("D.O.B", right_x, top_y)
        self.make_entry(self.var_dob, right_x + 120, top_y)

        self.make_label("Contact", right_x, top_y + 40)
        self.make_entry(self.var_contact, right_x + 120, top_y + 40)

        self.make_label("Admission", right_x, top_y + 80)
        self.make_entry(self.var_a_date, right_x + 120, top_y + 80)

        self.make_label("Course", right_x, top_y + 120)

        self.txt_course = ttk.Combobox(
            self.root,
            textvariable=self.var_course,
            values=("B.Tech", "B.Sc", "B.Com", "MBA", "M.Tech"),
            font=("goudy old style", 14),
            state="readonly",
            justify=CENTER
        )

        self.txt_course.place(
            x=right_x + 120,
            y=top_y + 120,
            width=200
        )

        self.txt_course.current(0)

        # ================= Buttons =================
        btn_y = 400

        self.make_button("Save", 150, btn_y, "#080354", self.add)
        self.make_button("Update", 270, btn_y, "#4caf50", self.update)
        self.make_button("Delete", 390, btn_y, "#f44336", self.delete)
        self.make_button("Clear", 510, btn_y, "#607d8b", self.clear)

        # ================= Search =================
        Label(
            self.root,
            text="Search By",
            font=("goudy old style", 14, "bold"),
            bg="white"
        ).place(x=750, y=400)

        search_type = ttk.Combobox(
            self.root,
            textvariable=self.var_search_type,
            values=("Roll", "Name", "Course"),
            state="readonly",
            font=("goudy old style", 13)
        )

        search_type.place(x=850, y=400, width=100)
        search_type.current(0)

        Entry(
            self.root,
            textvariable=self.var_search,
            font=("goudy old style", 14),
            bg="lightyellow"
        ).place(x=960, y=400, width=180)

        self.make_button("Search", 1150, 400, "#03a9f4", self.search, 100, 30)
        self.make_button("Show All", 1260, 400, "#9c27b0", self.show, 100, 30)

        # ================= Table =================
        self.S_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.S_Frame.place(x=20, y=450, width=1320, height=280)

        scrollx = Scrollbar(self.S_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.S_Frame, orient=VERTICAL)

        self.StudentTable = ttk.Treeview(
            self.S_Frame,
            columns=(
                "roll",
                "name",
                "email",
                "gender",
                "dob",
                "contact",
                "admission",
                "course",
                "state",
                "city",
                "pin",
                "address"
            ),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        for col in (
            "roll",
            "name",
            "email",
            "gender",
            "dob",
            "contact",
            "admission",
            "course",
            "state",
            "city",
            "pin",
            "address"
        ):
            self.StudentTable.heading(col, text=col.capitalize())
            self.StudentTable.column(col, width=120)

        self.StudentTable["show"] = "headings"
        self.StudentTable.pack(fill=BOTH, expand=1)

        self.StudentTable.bind(
            "<ButtonRelease-1>",
            self.get_data
        )

        self.create_table()
        self.show()

    # ================= Helper Functions =================
    def make_label(self, text, x, y):
        Label(
            self.root,
            text=text,
            font=("goudy old style", 14, "bold"),
            bg="white"
        ).place(x=x, y=y)

    def make_entry(self, variable, x, y, width=200):
        Entry(
            self.root,
            textvariable=variable,
            font=("goudy old style", 14),
            bg="lightyellow"
        ).place(x=x, y=y, width=width)

    def make_button(self, text, x, y, color, command, width=110, height=35):
        Button(
            self.root,
            text=text,
            font=("goudy old style", 14, "bold"),
            bg=color,
            fg="white",
            cursor="hand2",
            command=command
        ).place(x=x, y=y, width=width, height=height)

    # ================= Create Table =================
    def create_table(self):
        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS student(
                roll TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                dob TEXT,
                contact TEXT,
                admission TEXT,
                course TEXT,
                state TEXT,
                city TEXT,
                pin TEXT,
                address TEXT
            )
        """)

        con.commit()
        con.close()
    # ================= Add Student =================

        # ================= Add Student =================
    def add(self):
        con = get_connection()
        cur = con.cursor()

        try:
            if self.var_roll.get().strip() == "":
                messagebox.showerror(
                    "Error",
                    "Roll Number is required",
                    parent=self.root
                )
                return

            cur.execute(
                "SELECT * FROM student WHERE roll=?",
                (self.var_roll.get(),)
            )

            row = cur.fetchone()

            if row:
                messagebox.showerror(
                    "Error",
                    "Roll Number already exists",
                    parent=self.root
                )
                return

            cur.execute("""
                INSERT INTO student
                (
                    roll,
                    name,
                    email,
                    gender,
                    dob,
                    contact,
                    admission,
                    course,
                    state,
                    city,
                    pin,
                    address
                )
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                self.var_roll.get(),
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_contact.get(),
                self.var_a_date.get(),
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                self.var_pin.get(),
                self.txt_address.get("1.0", END).strip()
            ))

            con.commit()

            messagebox.showinfo(
                "Success",
                "Student Added Successfully",
                parent=self.root
            )

            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex),
                parent=self.root
            )

        finally:
            con.close()

    # ================= Show Students =================
    def show(self):
        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM student")

            rows = cur.fetchall()

            self.StudentTable.delete(
                *self.StudentTable.get_children()
            )

            for row in rows:
                self.StudentTable.insert(
                    "",
                    END,
                    values=row
                )

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex),
                parent=self.root
            )

        finally:
            con.close()

    # ================= Get Selected Record =================
    def get_data(self, event):
        selected = self.StudentTable.focus()

        contents = self.StudentTable.item(selected)

        row = contents["values"]

        if len(row) != 0:

            self.selected_roll = row[0]

            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_a_date.set(row[6])
            self.var_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(row[10])

            self.txt_address.delete("1.0", END)
            self.txt_address.insert(
                END,
                row[11]
            )
       # ================= Update Student =================
    def update(self):
        if self.selected_roll is None:
            messagebox.showerror(
                "Error",
                "Please select a student",
                parent=self.root
            )
            return

        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute("""
                UPDATE student
                SET
                    name=?,
                    email=?,
                    gender=?,
                    dob=?,
                    contact=?,
                    admission=?,
                    course=?,
                    state=?,
                    city=?,
                    pin=?,
                    address=?
                WHERE roll=?
            """,
            (
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_contact.get(),
                self.var_a_date.get(),
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                self.var_pin.get(),
                self.txt_address.get("1.0", END).strip(),
                self.selected_roll
            ))

            con.commit()

            messagebox.showinfo(
                "Success",
                "Student Updated Successfully",
                parent=self.root
            )

            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex),
                parent=self.root
            )

        finally:
            con.close()

    # ================= Delete Student =================
    def delete(self):
        if self.selected_roll is None:
            messagebox.showerror(
                "Error",
                "Please select a student",
                parent=self.root
            )
            return

        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute(
                "DELETE FROM student WHERE roll=?",
                (self.selected_roll,)
            )

            con.commit()

            messagebox.showinfo(
                "Success",
                "Student Deleted Successfully",
                parent=self.root
            )

            self.show()
            self.clear()

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
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_a_date.set("")
        self.var_course.set("B.Tech")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")

        self.txt_address.delete("1.0", END)

        self.selected_roll = None

        self.StudentTable.selection_remove(
            self.StudentTable.selection()
        )

    # ================= Search =================
    def search(self):
        if self.var_search.get().strip() == "":
            self.show()
            return

        con = get_connection()
        cur = con.cursor()

        try:
            column = self.var_search_type.get().lower()

            if column == "roll":
                sql = "SELECT * FROM student WHERE roll LIKE ?"

            elif column == "name":
                sql = "SELECT * FROM student WHERE name LIKE ?"

            else:
                sql = "SELECT * FROM student WHERE course LIKE ?"

            cur.execute(
                sql,
                ('%' + self.var_search.get().strip() + '%',)
            )

            rows = cur.fetchall()

            self.StudentTable.delete(
                *self.StudentTable.get_children()
            )

            for row in rows:
                self.StudentTable.insert(
                    "",
                    END,
                    values=row
                )

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex),
                parent=self.root
            )

        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()