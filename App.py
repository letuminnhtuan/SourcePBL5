from tkinter import *
from tkinter import ttk
import cv2
from firebase import firebase
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
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
        self.firebase = firebase.FirebaseApplication('https://test1-6422a-default-rtdb.firebaseio.com', None)
        self.login_path = 'Login'

    def check_function(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Vui long nhap tk mk ", parent=self.root)
        else:
            result = self.firebase.get(self.login_path, None)
            found = False
            for key in result.keys():
                if result[key]['username'] == self.username.get() and result[key]['password'] == self.password.get():
                    found = True
                    break
            if found:
                # messagebox.showinfo("Welcome", f"Chao`{self.username.get()}")
                self.open_new_screen()
            else:
                messagebox.showerror("Error", "tk hoac mk sai", parent=self.root)

    def open_new_screen(self):
        self.root.withdraw()  # Ẩn cửa sổ hiện tại
        self.new_window = Toplevel(self.root)
        self.app = Dashboard(self.new_window)

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Danh mục quản lí")
        # Form Dashboard
        Frame_dashboard = Frame(self.root, bg="white")
        Frame_dashboard.place(x=0, y=0, width=1199, height=600)

        title = Label(Frame_dashboard, text="Quản lí bãi đổ xe", font=("Impact", 35, "bold"), fg="#6162FF", bg="white",
                      bd=0, padx=10, pady=5, borderwidth=0)
        title.place(x=400, y=20)
        #khung title
        icon = Image.open("Picture/border.png")
        icon = icon.resize((450, 40), Image.ANTIALIAS)
        self.icon_image = ImageTk.PhotoImage(icon)
        icon_label = Label(Frame_dashboard, image=self.icon_image, bg="white")
        icon_label.place(x=355, y=75)
        #icon1
        icon1 = Image.open("Picture/moto.png")
        icon1 = icon1.resize((80, 60), Image.ANTIALIAS)
        self.icon_image1 = ImageTk.PhotoImage(icon1)
        icon_label1 = Label(Frame_dashboard, image=self.icon_image1, bg="white")
        icon_label1.place(x=150, y=115)
        #icon2
        icon2 = Image.open("Picture/moto.png")
        icon2 = icon2.resize((80, 60), Image.ANTIALIAS)
        self.icon_image2 = ImageTk.PhotoImage(icon2)
        icon_label2 = Label(Frame_dashboard, image=self.icon_image2, bg="white")
        icon_label2.place(x=430, y=115)
        # icon3
        icon3 = Image.open("Picture/moto.png")
        icon3 = icon3.resize((80, 60), Image.ANTIALIAS)
        self.icon_image3 = ImageTk.PhotoImage(icon3)
        icon_label2 = Label(Frame_dashboard, image=self.icon_image3, bg="white")
        icon_label2.place(x=730, y=115)
        # icon4
        icon4 = Image.open("Picture/barrier.png")
        icon4 = icon4.resize((100, 80), Image.ANTIALIAS)
        self.icon_image4 = ImageTk.PhotoImage(icon4)
        icon_label2 = Label(Frame_dashboard, image=self.icon_image4, bg="white")
        icon_label2.place(x=960, y=95)
        logout = Button(Frame_dashboard, text="Logout", bd=0, font=("Goudy old style", 15),bg="#6162FF", fg="white", command=self.logout_function).place(x=1050, y=30, width=100, height=40)
        form = Label(Frame_dashboard, text="", font=("Arial", 20), bg="white", bd=2, highlightthickness=2,highlightbackground="gray").place(x=100, y=200, width=980, height=300)
        style = ttk.Style()
        style.map("TButton", foreground=[('active', '#6162FF')], background=[('active', 'gray')])
        style.configure("TButton", padding=6, relief="flat", font=("Goudy old style", 15), background="#6162FF",
                        foreground="white")
        style.configure("TButton", borderwidth=0, focuscolor="none", highlightthickness=0, bordercolor="none")
        style.configure("TButton", bordercolor="none", focuscolor="none", borderwidth=0)
        style.configure("TButton", bordercolor="none", focuscolor="none", borderwidth=0, relief="flat",
                        background="#6162FF", foreground="white", padding=6)
        style.configure("TButton", bordercolor="none", focuscolor="none", borderwidth=0, relief="flat",
                        background="#6162FF", foreground="orange", padding=6, borderradius=80)

        QLxevao = ttk.Button(Frame_dashboard, command=self.tranfer_BS, text="QL Xe vào").place(x=130, y=220,
                                                                                                  width=160, height=40)
        AddNhanvien = ttk.Button(Frame_dashboard, text="Thêm Nhân Viên").place(x=530, y=220, width=160, height=40)
        QLxera = ttk.Button(Frame_dashboard,command=self.tranfer_BS1, text="QL Xe ra").place(x=530, y=320, width=160, height=40)
        QLNhanvien = ttk.Button(Frame_dashboard ,command=self.tranfer_staff,text="QL Nhân Viên").place(x=880, y=220, width=160, height=40)
    def tranfer_BS(self):
        self.open_new_screenBS()
    def open_new_screenBS(self):
        self.new_window = Toplevel(self.root)
        self.app = BS(self.new_window)
    def tranfer_BS1(self):
        self.open_new_screenBS1()
    def open_new_screenBS1(self):
        self.new_window = Toplevel(self.root)
        self.app = BS1(self.new_window)
    def tranfer_staff(self):
        self.open_new_screenstaff()
    def open_new_screenstaff(self):
        self.new_window = Toplevel(self.root)
        self.app = staff(self.new_window)
    def logout_function(self):
        root.destroy()

class staff:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lí sinh viên")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        # Header
        header_frame = Frame(self.root,bg="pink")
        header_frame.pack(side=TOP, fill=X)

        title = Label(header_frame, text="Danh sách sinh viên", font=("Impact", 20, "italic"), bg="pink")
        title.pack(side=LEFT, padx=260, pady=15)

        # Back button
        back = Button(header_frame, text="Back", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white",
                        command=self.logout_function)
        back.place(x=680, y=20, width=100, height=40)
        # Image
        icon1 = Image.open("Picture/staff3.png")
        icon1 = icon1.resize((80, 60), Image.ANTIALIAS)
        self.icon_image1 = ImageTk.PhotoImage(icon1)
        icon_label1 = Label(header_frame, image=self.icon_image1, bg="pink")
        icon_label1.place(x=25, y=5)
        # Table
        table_frame = Frame(self.root)
        table_frame.pack(side=TOP)
        table_frame.place(x=100,y=120)
        # Columns
        columns = ("ID", "Tên nhân viên", "Email", "Số điện thoại")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        tree.pack(side=LEFT)
        tree.column("ID", width=50, anchor=CENTER)
        tree.column("Tên nhân viên", width=200, anchor=CENTER)
        tree.column("Email", width=200, anchor=CENTER)
        tree.column("Số điện thoại", width=150, anchor=CENTER)
        tree.heading("ID", text="ID")
        tree.heading("Tên nhân viên", text="Tên nhân viên")
        tree.heading("Email", text="Email")
        tree.heading("Số điện thoại", text="Số điện thoại")

        # Firebase
        self.firebase = firebase.FirebaseApplication('https://test1-6422a-default-rtdb.firebaseio.com', None)
        data = self.firebase.get('nhanvien', None)
        if data is not None:
            for item in data:
                if item is not None:
                    id = item.get('id', '')
                    name = item.get('tên nhân viên', '')
                    email = item.get('email', '')
                    phone = item.get('sdt', '')
                    tree.insert("", END, values=(id, name, email, phone))
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.config(yscrollcommand=scrollbar.set)
    def logout_function(self):
        self.root.destroy()
class BS:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Quản lí xe vào")
        # Form Dashboard
        Frame_dashboard = Frame(self.root, bg="white", relief="groove", bd=1, highlightthickness=1,
                                highlightbackground="green")
        Frame_dashboard.place(x=0, y=0, width=1199, height=600)

        # Form left (display camera)
        Frame_left = Frame(Frame_dashboard, bg="white", bd=0, highlightthickness=1, highlightbackground="green")
        Frame_left.place(x=0, y=0, width=599, height=600)

        # Access the camera
        self.cap0 = cv2.VideoCapture(0)

        # Display the image from the camera
        self.label = Label(Frame_left)
        self.label.pack()
        self.update_image()  # call the update_image() function

        # Form right (car information)
        Frame_right = Frame(Frame_dashboard, bg="white", bd=0, highlightthickness=1, highlightbackground="green")
        Frame_right.place(x=600, y=0, width=599, height=600)
        Label(Frame_right, text="THÔNG TIN", font=("Goudy old style", 30, "bold"), fg="grey", bg="white").place(x=150,
                                                                                                                y=30)
        back = Button(Frame_right, text="Back", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white",
                        command=self.logout_function)
        back.place(x=480, y=30, width=100, height=40)

        Label(Frame_right, text="Id ", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30,
                                                                                                      y=130)
        self.id = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.id.place(x=150, y=130, width=320, height=35)

        Label(Frame_right, text="Time in", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30,
                                                                                                             y=230)
        self.timein = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.timein.place(x=150, y=230, width=320, height=35)

        Label(Frame_right, text="Biển số", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30, y=330)

        self.bienso = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.bienso.place(x=150, y=330, width=320, height=35)

        # Firebase
        self.firebase = firebase.FirebaseApplication('https://test1-6422a-default-rtdb.firebaseio.com', None)

        # Get data
        data = self.firebase.get('/timein/3', None)
        print(data)

        # Display data in the Entry widgets
        self.id.delete(0, END)
        self.id.insert(0, str(data['id']))
        self.id.configure(state="readonly")

        self.timein.delete(0, END)
        self.timein.insert(0, str(data['timein']))
        self.timein.configure(state="readonly")

        self.bienso.delete(0, END)
        self.bienso.insert(0, str(data['license_plate']))
        self.bienso.configure(state="readonly")

    def update_image(self):
        ret0, frame0 = self.cap0.read()
        frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame0)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(10, self.update_image)

    def logout_function(self):
        self.root.destroy()
class BS1:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        self.captured_images = []  # khởi tạo danh sách các ảnh đã chụp
        self.root.title("Quản lí xe ra")
        # Form Dashboard
        Frame_dashboard = Frame(self.root, bg="white", relief="groove", bd=1, highlightthickness=1,
                                highlightbackground="green")
        Frame_dashboard.place(x=0, y=0, width=1199, height=600)

        # Form left (display camera)
        Frame_left = Frame(Frame_dashboard, bg="white", bd=0, highlightthickness=1, highlightbackground="green")
        Frame_left.place(x=0, y=0, width=599, height=600)

        # Access the camera
        self.cap1 = cv2.VideoCapture(1)

        # Display the image from the camera
        self.label = Label(Frame_left)
        self.label.pack()
        self.update_image()  # call the update_image() function

        # Form right (car information)
        Frame_right = Frame(Frame_dashboard, bg="white", bd=0, highlightthickness=1, highlightbackground="green")
        Frame_right.place(x=600, y=0, width=599, height=600)
        Label(Frame_right, text="THÔNG TIN", font=("Goudy old style", 30, "bold"), fg="grey", bg="white").place(x=150,
                                                                                                                y=30)
        logout = Button(Frame_right, text="Back", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white",
                        command=self.logout_function)
        logout.place(x=480, y=30, width=100, height=40)

        Label(Frame_right, text="Id ", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30,
                                                                                                      y=130)
        self.id = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.id.place(x=150, y=130, width=320, height=35)

        Label(Frame_right, text="Time out", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30,
                                                                                                             y=230)
        self.timeout = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.timeout.place(x=150, y=230, width=320, height=35)

        Label(Frame_right, text="Biển số", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30, y=330)

        self.bienso = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.bienso.place(x=150, y=330, width=320, height=35)

        # Firebase
        self.firebase = firebase.FirebaseApplication('https://test1-6422a-default-rtdb.firebaseio.com', None)

        # Get data
        data = self.firebase.get('/timeout/3', None)
        print(data)

        # Display data in the Entry widgets
        self.id.delete(0, END)
        self.id.insert(0, str(data['id']))
        self.id.configure(state="readonly")

        self.timeout.delete(0, END)
        self.timeout.insert(0, str(data['timeout']))
        self.timeout.configure(state="readonly")

        self.bienso.delete(0, END)
        self.bienso.insert(0, str(data['license_plate']))
        self.bienso.configure(state="readonly")

    def update_image(self):
        ret1, frame1 = self.cap1.read()
        if ret1 == True:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        # rest of the code
        else:
            print("No image")
        img = Image.fromarray(frame1)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(10, self.update_image)

    def logout_function(self):
        self.root.destroy()
root = Tk()
obj = Login(root)
root.mainloop()