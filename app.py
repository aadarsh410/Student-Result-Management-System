from tkinter import *
from PIL import Image, ImageTk
from course import CourseClass
from student import StudentClass
from result import ResultClass
from report import reportClass
from database import initialize_database
import subprocess
import sys
import os

# ----------------- Logout Function -----------------
def logout(root):
    root.destroy()
    # Replace 'login.py' with your actual login file name
    subprocess.Popen([sys.executable, "login.py"])

class YADAVPROJECT:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Result Management System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")

        # Title
        title = Label(self.root, text=f"Welcome {username} - Result Management System", padx=10,
                      font=("goudy old style", 20, "bold"),
                      bg="#080354", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Menu Frame
        M_Frame = LabelFrame(self.root, text="Menus",
                             font=("times new roman", 15), bg="white")
        M_Frame.place(x=10, y=70, width=1340, height=80)

        btn_course = Button(M_Frame, text="Course", font=("goudy old style", 15, "bold"),
                            bg="#080354", fg="white", cursor="hand2",
                            command=self.add_course)
        btn_course.place(x=20, y=5, width=200, height=40)

        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"),
                             bg="#080354", fg="white", cursor="hand2",
                             command=self.add_student)
        btn_student.place(x=240, y=5, width=200, height=40)

        btn_result = Button(M_Frame, text="Result", font=("goudy old style", 15, "bold"),
                            bg="#080354", fg="white", cursor="hand2",
                            command=self.add_result)
        btn_result.place(x=460, y=5, width=200, height=40)

        btn_view_result = Button(M_Frame, text="View Student Result", font=("goudy old style", 15, "bold"),
                                 bg="#080354", fg="white", cursor="hand2", command=self.add_report)
        btn_view_result.place(x=680, y=5, width=200, height=40)

        btn_logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"),
                            bg="#080354", fg="white", cursor="hand2",
                            command=lambda: logout(self.root))
        btn_logout.place(x=900, y=5, width=200, height=40)

        btn_exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"),
                          bg="#080354", fg="white", cursor="hand2",
                          command=self.root.destroy)
        btn_exit.place(x=1120, y=5, width=200, height=40)

        # Background Image
        try:
            self.re_img = Image.open("images/result image 2.avif")
            self.re_img = self.re_img.resize((920, 350))
            self.re_img = ImageTk.PhotoImage(self.re_img)
            self.lbl_bg = Label(self.root, image=self.re_img)
            self.lbl_bg.place(x=400, y=180, width=800, height=200)
        except Exception as e:
            print("Image not found or error loading:", e)

        # Stats Labels
        self.lbl_Course = Label(self.root, text="Total Courses\n[ 0 ]",
                                font=("goudy old style", 20),
                                bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_Course.place(x=400, y=530, width=300, height=100)

        self.lbl_Student = Label(self.root, text="Total Students\n[ 0 ]",
                                 font=("goudy old style", 20),
                                 bd=10, relief=RIDGE, bg="#0676ad", fg="white")
        self.lbl_Student.place(x=710, y=530, width=300, height=100)

        self.lbl_Result = Label(self.root, text="Total Results\n[ 0 ]",
                                font=("goudy old style", 20),
                                bd=10, relief=RIDGE, bg="#038074", fg="white")
        self.lbl_Result.place(x=1020, y=530, width=300, height=100)

        # Footer
        footer = Label(self.root, text="SRMS - Result Management System\nContact Us: 926xxxxx02",
                       font=("goudy old style", 12), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ResultClass(self.new_win)

    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)

# Function to start dashboard after login
def open_dashboard(username):
    # Initialize database and create all tables if they don't exist
    initialize_database()

    root = Tk()
    app = YADAVPROJECT(root, username)
    root.mainloop()

if __name__ == "__main__":
    open_dashboard("TestUser")
