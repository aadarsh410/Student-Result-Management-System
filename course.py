from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")
        self.root.geometry("1200x600+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        self.selected_cid = None  # For update & delete

        # Title
        title = Label(self.root, text="Manage Course Details",
                      font=("goudy old style", 20, "bold"),
                      bg="#080354", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Labels & Entry Fields
        Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        Label(self.root, text="Duration", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        Label(self.root, text="Charges", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        Label(self.root, text="Description", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)

        Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=60, width=200)
        Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=100, width=200)
        Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=140, width=200)

        self.txt_description = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_description.place(x=150, y=180, width=500, height=130)

        # Buttons
        Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#080354", fg="white", cursor="hand2", command=self.add).place(x=150, y=400, width=110, height=40)
        Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update).place(x=270, y=400, width=110, height=40)
        Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete).place(x=390, y=400, width=110, height=40)
        Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear).place(x=510, y=400, width=110, height=40)

        # Search Panel
        Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=60)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15), bg="lightyellow").place(x=870, y=60, width=180)
        Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=1070, y=60, width=120, height=28)

        # Course Table
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"),
                                        xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = "headings"
        self.CourseTable.column("cid", width=70)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.create_table()
        self.show()

    # Create table
    def create_table(self):
        con = sqlite3.connect(database="yadavproject.db")
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS course (
                cid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                duration TEXT,
                charges TEXT,
                description TEXT
            )
        """)
        con.commit()
        con.close()

    # Add course
    def add(self):
        con = sqlite3.connect(database="yadavproject.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "Course Name already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO course(name, duration, charges, description) VALUES(?,?,?,?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END).strip()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Show courses
    def show(self):
        con = sqlite3.connect(database="yadavproject.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Get data
    def get_data(self, event):
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        if row:
            self.selected_cid = row[0]
            self.var_course.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])
            self.txt_description.delete("1.0", END)
            self.txt_description.insert(END, row[4])

    # Update course
    def update(self):
        if self.selected_cid is None:
            messagebox.showerror("Error", "Please select a course to update", parent=self.root)
            return
        con = sqlite3.connect(database="yadavproject.db")
        cur = con.cursor()
        try:
            cur.execute("UPDATE course SET name=?, duration=?, charges=?, description=? WHERE cid=?", (
                self.var_course.get(),
                self.var_duration.get(),
                self.var_charges.get(),
                self.txt_description.get("1.0", END).strip(),
                self.selected_cid
            ))
            con.commit()
            messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Delete course
    def delete(self):
        if self.selected_cid is None:
            messagebox.showerror("Error", "Please select a course to delete", parent=self.root)
            return
        con = sqlite3.connect(database="yadavproject.db")
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM course WHERE cid=?", (self.selected_cid,))
            con.commit()
            messagebox.showinfo("Success", "Course Deleted Successfully", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Clear fields
    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0", END)
        self.selected_cid = None

    # Search course
    def search(self):
        con = sqlite3.connect(database="yadavproject.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
