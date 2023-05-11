from tkinter import *
from tkinter import ttk
from Firebase import database
from PIL import Image
from PIL import ImageTk

class car: # class quản lí car
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lí Xe")
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
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.pack(side=LEFT)
        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.column("Tên chủ", width=200, anchor=CENTER)
        self.tree.column("SDT", width=150, anchor=CENTER)
        self.tree.column("CCCD", width=150, anchor=CENTER)
        self.tree.column("Time-register", width=150, anchor=CENTER)
        self.tree.column("Period-time", width=150, anchor=CENTER)
        self.tree.column("Tổng tiền", width=150, anchor=CENTER)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên chủ", text="Tên chủ")
        self.tree.heading("SDT", text="SDT")
        self.tree.heading("CCCD", text="CCCD")
        self.tree.heading("Time-register", text="Time-register")
        self.tree.heading("Period-time", text="Period-time")
        self.tree.heading("Tổng tiền", text="Tổng tiền")

        # Lấy thông tin danh sách xe đăng kí
        self.firebase = database()
        car_manager_info = self.firebase.get_car_manager_info()

        for info in car_manager_info:
            self.tree.insert("", END, values=info)
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        self.update_car_info()
    def update_car_info(self):
        car_manager_info = self.firebase.get_car_manager_info()
        self.tree.delete(*self.tree.get_children())
        for info in car_manager_info:
            self.tree.insert("", END, values=info)
         # Schedule the next update in 3 seconds
        self.root.after(2000, self.update_car_info)
    def logout_function(self):
        self.root.destroy()
# root = Tk()
# obj = car(root)
# root.mainloop()