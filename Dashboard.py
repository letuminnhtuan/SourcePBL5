from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from Car import car
from Account_Client import Account
from Price_List import Price
from Revenue import dt
class db:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Danh mục quản lí")
        # Form Dashboard
        Frame_dashboard = Frame(self.root, bg="white")
        Frame_dashboard.place(x=0, y=0, width=1199, height=600)

        title = Label(Frame_dashboard, text="Quản lí bãi đổ xe", font=("Helvetica", 35, "bold"), fg="#6162FF", bg="white",
                      bd=0, padx=10, pady=5, borderwidth=0)
        title.place(x=400, y=20)
        #khung title
        icon = Image.open("Picture/border.png")
        icon = icon.resize((450, 40), Image.LANCZOS)
        self.icon_image = ImageTk.PhotoImage(icon)
        icon_label = Label(Frame_dashboard, image=self.icon_image, bg="white")
        icon_label.place(x=355, y=75)
        #icon1
        icon1 = Image.open("Picture/moto.png")
        icon1 = icon1.resize((80, 60), Image.LANCZOS)
        self.icon_image1 = ImageTk.PhotoImage(icon1)
        icon_label1 = Label(Frame_dashboard, image=self.icon_image1, bg="white")
        icon_label1.place(x=150, y=115)
        #icon2
        icon2 = Image.open("Picture/moto.png")
        icon2 = icon2.resize((80, 60), Image.LANCZOS)
        self.icon_image2 = ImageTk.PhotoImage(icon2)
        icon_label2 = Label(Frame_dashboard, image=self.icon_image2, bg="white")
        icon_label2.place(x=430, y=115)
        # icon3
        icon3 = Image.open("Picture/moto.png")
        icon3 = icon3.resize((80, 60), Image.LANCZOS)
        self.icon_image3 = ImageTk.PhotoImage(icon3)
        icon_label2 = Label(Frame_dashboard, image=self.icon_image3, bg="white")
        icon_label2.place(x=730, y=115)
        # icon4
        icon4 = Image.open("Picture/barrier.png")
        icon4 = icon4.resize((100, 80), Image.LANCZOS)
        self.icon_image4 = ImageTk.PhotoImage(icon4)
        icon_label2 = Label(Frame_dashboard, image=self.icon_image4, bg="white")
        icon_label2.place(x=960, y=95)
        logout = Button(Frame_dashboard, text="Thoát", bd=0, font=("Helvetica", 15),bg="#6162FF", fg="white", command=self.logout_function).place(x=1050, y=30, width=100, height=40)
        form = Label(Frame_dashboard, text="", font=("Helvetica", 20), bg="white", bd=2, highlightthickness=2,highlightbackground="gray").place(x=100, y=200, width=980, height=300)
        style = ttk.Style()
        style.map("TButton", foreground=[('active', '#6162FF')], background=[('active', 'gray')])
        style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 15), background="#6162FF",
                        foreground="white")
        style.configure("TButton", borderwidth=0, focuscolor="none", highlightthickness=0, bordercolor="none")
        style.configure("TButton", bordercolor="none", focuscolor="none", borderwidth=0)
        style.configure("TButton", bordercolor="none", focuscolor="none", borderwidth=0, relief="flat",
                        background="#6162FF", foreground="white", padding=6)
        style.configure("TButton", bordercolor="none", focuscolor="none", borderwidth=0, relief="flat",
                        background="#6162FF", foreground="orange", padding=6, borderradius=80)
        # Button quản lí doanh thu
        ttk.Button(Frame_dashboard, text="Quản lí doanh thu", command=self.transfer_DoanhThu).place(x=130, y=220,width=200, height=40)
        # Button quản lí client
        ttk.Button(Frame_dashboard, text="Quản lí tài khoản",command=self.tranfer_Client).place(x=530, y=220, width=200, height=40)
        # Button quản lí xe
        ttk.Button(Frame_dashboard,text="Quản lí ra vào",command=self.tranfer_QLcar).place(x=880, y=220, width=200, height=40)
        # Button quản lí PriceList
        ttk.Button(Frame_dashboard, text="Quản lí bảng giá", command=self.tranfer_Price).place(x=530, y=320, width=200, height=40)
    # Chuyển sang trang quản lí xe đăng kí
    def tranfer_QLcar(self):
        self.open_new_QLcar()
    def open_new_QLcar(self):
        self.new_window = Toplevel(self.root)
        self.app = car(self.new_window)
    #Chuyển sang form đăng kí
    def tranfer_Client(self):
        self.open_new_Client()
    def open_new_Client(self):
        self.new_window = Toplevel(self.root)
        self.app = Account(self.new_window)
    def tranfer_Price(self):
        self.open_new_Price()
    def open_new_Price(self):
        self.new_window = Toplevel(self.root)
        self.app = Price(self.new_window)
    def transfer_DoanhThu(self):
        self.open_DoanhThu()
    def open_DoanhThu(self):
        self.new_window = Toplevel(self.root)
        self.app = dt(self.new_window)
    def logout_function(self):
        self.root.destroy()

# root = Tk()
# obj = db(root)
# root.mainloop()