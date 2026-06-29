from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        self.root.focus_force()
 
        # Title
        title = Label(self.root, text="VIEW STUDENT RESULTS", font=("goudy old style", 24, "bold"),
                      bg="#080354", fg="white")
        title.pack(side=TOP, fill=X)
        
        # Search
        self.var_search = StringVar()
        Label(self.root, text="Search By Roll No.", font=("goudy old style", 20, "bold"), bg="white").place(x=280, y=100)
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20), bg="lightyellow").place(x=560, y=100, width=150)
        Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white",
               cursor="hand2", command=self.search_student).place(x=720, y=100, width=100, height=35)
        Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="gray", fg="white",
               cursor="hand2", command=self.clear).place(x=840, y=100, width=100, height=35)

        # Result labels
        Label(self.root, text="Roll No", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=200, y=230, width=150, height=50)
        Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=350, y=230, width=150, height=50)
        Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=500, y=230, width=150, height=50)
        Label(self.root, text="Marks Obtained", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=650, y=230, width=150, height=50)
        Label(self.root, text="Total Marks", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=800, y=230, width=150, height=50)
        Label(self.root, text="Percentage", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=950, y=230, width=150, height=50)

        self.roll = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.roll.place(x=200, y=280, width=150, height=50)
        self.name = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.name.place(x=350, y=280, width=150, height=50)
        self.course = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.course.place(x=500, y=280, width=150, height=50)
        self.marks = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.marks.place(x=650, y=280, width=150, height=50)
        self.full = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.full.place(x=800, y=280, width=150, height=50)
        self.per = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.per.place(x=950, y=280, width=150, height=50)
 
        # Delete button
        Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="red", fg="white",
               cursor="hand2", command=self.delete_result).place(x=580, y=350, width=150, height=40)

    def search_student(self):
        con = sqlite3.connect("yadavproject.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
        row = cur.fetchone()
        con.close()
        if row is not None:
            # Adjust these indexes according to your table's column order
            self.roll.config(text=row[0])   # Roll No
            self.name.config(text=row[1])   # Name
            self.course.config(text=row[2]) # Course
            self.marks.config(text=row[3])  # Marks
            self.full.config(text=row[4])   # Total Marks
            self.per.config(text=row[5])    # Percentage
        else:
            messagebox.showerror("Error", "No record found for this Roll No.", parent=self.root)

    def clear(self):
        self.var_search.set("")
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")

    def delete_result(self):
        con = sqlite3.connect("yadavproject.db")
        cur = con.cursor()
        cur.execute("DELETE FROM result WHERE roll=?", (self.var_search.get(),))
        con.commit()
        con.close()
        messagebox.showinfo("Deleted", "Result deleted successfully!", parent=self.root)
        self.clear()

# Run the program
if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()
