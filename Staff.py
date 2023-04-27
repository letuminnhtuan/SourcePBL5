from tkinter import *
from tkinter import ttk
from firebase import firebase
from PIL import Image
from PIL import ImageTk

class staff: # class quản lí nhân viên
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