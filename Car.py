from tkinter import *
from tkinter import ttk
from Firebase import database
from PIL import Image
from PIL import ImageTk

class car: # class quản lí nhân viên
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lí sinh viên")
        self.root.geometry("1200x500")
        self.root.resizable(False, False)
        # Header
        header_frame = Frame(self.root,bg="pink")
        header_frame.pack(side=TOP, fill=X)

        title = Label(header_frame, text="Quản lí xe ", font=("Impact", 25, "italic"), bg="pink")
        title.pack( padx=410, pady=15)

        # Back button
        back = Button(header_frame, text="Back", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white",
                        command=self.logout_function)
        back.place(x=1080, y=20, width=100, height=40)
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
        # Columns
        columns = ("ID", "Tên chủ", "SDT", "CCCD", "Time-register", "Period-time", "Tổng tiền")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        tree.pack(side=LEFT)
        tree.column("ID", width=50, anchor=CENTER)
        tree.column("Tên chủ", width=200, anchor=CENTER)
        tree.column("SDT", width=150, anchor=CENTER)
        tree.column("CCCD", width=150, anchor=CENTER)
        tree.column("Time-register", width=150, anchor=CENTER)
        tree.column("Period-time", width=150, anchor=CENTER)
        tree.column("Tổng tiền", width=150, anchor=CENTER)
        tree.heading("ID", text="ID")
        tree.heading("Tên chủ", text="Tên chủ")
        tree.heading("SDT", text="SDT")
        tree.heading("CCCD", text="CCCD")
        tree.heading("Time-register", text="Time-register")
        tree.heading("Period-time", text="Period-time")
        tree.heading("Tổng tiền", text="Tổng tiền")

        # Lấy thông tin danh sách xe đăng kí
        self.firebase = database()
        car_manager_info =self.firebase.get_car_manager_info()

        for info in car_manager_info:
            tree.insert("", END, values=info)
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.config(yscrollcommand=scrollbar.set)
    def logout_function(self):
        self.root.destroy()
# root = Tk()
# obj = car(root)
# root.mainloop()