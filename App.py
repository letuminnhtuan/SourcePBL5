from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
from Firebase import database
from Camera import QL_Camera
from Camera_client import camera_client
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        # Background
        self.bg = ImageTk.PhotoImage(file="Picture/logo.webp")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        # Form Login
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=300, y=90, width=600, height=400)
        title = Label(Frame_login, text="Quản lí bãi giữ xe", font=("Impact", 35, "bold"), fg="#6162FF",bg="white").place(x=90, y=30)
        # Username
        lbl_user = Label(Frame_login, text="UserName", font=("Goudy old style", 15, "bold"), fg="grey",bg="white").place(x=90, y=140)
        self.username = Entry(Frame_login, font=("Goudy old style", 15), bg="#E7E6E6")
        self.username.place(x=90, y=170, width=320, height=35)
        # Password
        lbl_pw = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="grey",bg="white").place(x=90, y=210)
        self.password = Entry(Frame_login, font=("Goudy old style", 15), bg="#E7E6E6", show="*")
        self.password.place(x=90, y=240, width=320, height=35)
        # Button
        submit = Button(Frame_login, command=self.check_function, text="Login", bd=0, font=("Goudy old style", 15),bg="#6162FF", fg="white").place(x=90, y=310, width=180, height=40)
        # Firebase
        self.firebase = database()
        self.login_path = 'Login'

    def check_function(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Vui long nhap tk mk ", parent=self.root)
        else:
            found, user_role = self.firebase.check_login(self.username.get(), self.password.get())
            print(type(user_role))
            print(user_role)
            if found:
                if user_role == "1":
                    self.open_new_screen_manager()
                else:
                    self.open_new_screen_client()
            else:
                messagebox.showerror("Error", "tk hoac mk sai", parent=self.root)
    def open_new_screen_manager(self):
        self.root.withdraw()  # Ẩn cửa sổ hi1ện tại
        self.new_window = Toplevel(self.root)
        self.app = QL_Camera(self.new_window)
    def open_new_screen_client(self):
        self.root.withdraw()  # Ẩn cửa sổ hi1ện tại
        self.new_window = Toplevel(self.root)
        self.app = camera_client(self.new_window)
root = Tk()
obj = Login(root)
root.mainloop()