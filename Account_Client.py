import customtkinter as ctk
import tkinter as tk
from tkinter import *
from Firebase import database
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
appWidth, appHeight = 550, 200

class Account:
    def __init__(self, root):
        self.root = root
        self.root.title("Tài khoản")
        self.root.geometry(f"{appWidth}x{appHeight}")
        self.root.configure(bg="#EEEEEE")

        # Kết nối đến Firebase
        self.db = database()

        self.Thongtin = ctk.CTkLabel(self.root, text="Tài khoản", font=("Helvetica", 40), height=40,
                                     width=320, text_color="#444444").place(x=105, y=20)

        self.list = ctk.CTkLabel(self.root, text="Danh sách", font=("Helvetica", 20), text_color="#444444").place(x=50, y=100)

        account_list = self.get_account()
        self.selected_account = tk.StringVar()
        self.list_option = ctk.CTkOptionMenu(self.root, width=200, font=("Helvetica", 18),
                                             values=account_list, variable=self.selected_account).place(x=170, y=100)

        self.showbutton = ctk.CTkButton(master=self.root, text="Hiển thị", font=("Helvetica", 18, 'bold'), command=self.show,
                                        text_color="white", hover=True, hover_color="#ffb557",
                                        height=40, width=120, border_width=2, corner_radius=20, border_color="#bc863f",
                                        fg_color="#eda850") \
            .place(x=400, y=95)

    def show(self):
        selected_account = self.selected_account.get()
        account_info = None
        data = self.db.get_account()
        for account in data.values():
            if account['username'].lower() == selected_account.lower():
                account_info = account
                break
        self.root.geometry(f"{appWidth}x{appHeight + 300}")
        self.tkLabel = ctk.CTkLabel(self.root, text="Tên đăng nhập", font=("Helvetica", 18), text_color="#444444").place(
                x=50, y=200)
        self.tkEntry = ctk.CTkEntry(self.root, width=250, font=("Helvetica", 18))
        self.tkEntry.insert(0,account_info['username'])
        self.tkEntry.place(x=200, y=200)
        self.pwLabel = ctk.CTkLabel(self.root, text="Mật khẩu", font=("Helvetica", 18), text_color="#444444").place(
                x=50, y=270)
        self.pwEntry = ctk.CTkEntry(self.root, width=250, font=("Helvetica", 18))
        self.pwEntry.insert(0,account_info['password'])
        self.pwEntry.place(x=200, y=270)

        self.tkLabel = ctk.CTkLabel(self.root, text="Quyền", font=("Helvetica", 18), text_color="#444444").place(
                x=50, y=340)
        self.value = tk.StringVar()
        self.Client_radio = ctk.CTkRadioButton(master=self.root, text="Nhân viên", font=("Helvetica", 18), variable=self.value, value="0",
                                                   radiobutton_height=30, radiobutton_width=30,text_color="#444444")
        self.Client_radio.place(x=150, y=340)
        self.manager_radio = ctk.CTkRadioButton(self.root, text="Quản lí", font=("Helvetica", 18), variable=self.value, width=70, value="1",text_color="#444444",
                                                    radiobutton_height=30, radiobutton_width=30)
        self.manager_radio.place(x=300, y=340)
        if account_info['role'] == "1":
            self.manager_radio.select()
        else:
            self.Client_radio.select()

        save_button = ctk.CTkButton(master=self.root, text="Lưu", font=("Helvetica", 18, 'bold'),
                                    text_color="white", hover=True, hover_color="#0099FF",
                                    height=40, width=120, border_width=2, corner_radius=20, border_color="#3399FF",
                                    fg_color="#66CCFF", command=self.save)
        save_button.place(x=230, y=400)

        self.save_button = save_button  # Lưu lại tham chiếu đến nút "Save"

        self.root.update()
    def get_account(self):
        data = self.db.get_account()  # Truy xuất dữ liệu từ Firebase
        # Xử lý dữ liệu và trả về danh sách các tài khoản
        account_list = []
        if data is not None:
            for key, value in data.items():
                if isinstance(value, dict) and "username" in value:
                    account_list.append(value["username"])
        return account_list

    def save(self):
        selected_account = self.selected_account.get()
        tk_new = self.tkEntry.get()
        mk_new = self.pwEntry.get()
        value_new = self.value.get()
        data = self.db.get_account()
        for acc_name, acc_info in data.items():
            if acc_info['username'] == selected_account:
                acc_number = int(acc_name.split('-')[1])
                self.db.save_account(acc_number,tk_new,mk_new,value_new)
                messagebox.showinfo("Success", " Sửa thành công \U0001F604 ")
                break
        self.root.destroy()
# root = tk.Tk()
# app = Account(root)
# root.mainloop()
