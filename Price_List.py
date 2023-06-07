import customtkinter as ctk
import tkinter as tk
from tkinter import *
from Firebase import database
from tkinter import messagebox
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
appWidth, appHeight = 350, 550
class Price:
    def __init__(self, root):
        self.root = root
        self.root.title("Bảng giá")
        self.root.geometry(f"{appWidth}x{appHeight}")
        self.root.configure(bg="#EEEEEE")
        # Kết nối đến Firebase
        self.db = database()
        data = self.db.get_price_list()
        data = list(filter(None, data))
        self.Thongtin = ctk.CTkLabel(self.root, text="BẢNG GIÁ", font=("Helvetica", 30), height=40,
                                     width=320, text_color="#444444").place(x=30, y=20)
        for item in data:
            price = item.get('Price', '')
            type = item.get('Type', '')
            if type == "Giờ":
                self.hour = ctk.CTkLabel(self.root,text="Giờ",font=("Helvetica", 25)).place(x = 30,y = 110 )
                self.hour_entry_value = price
                self.hour_entry = ctk.CTkEntry(self.root,placeholder_text="3000",font=("Helvetica",25),corner_radius=20,border_color="#FF9999",height=55,width=200)
                self.hour_entry.insert(0,self.hour_entry_value)
                self.hour_entry.place(x = 130,y = 100 )

            if type == "Ngày":
                self.day = ctk.CTkLabel(self.root, text="Ngày", font=("Helvetica", 25)).place(x=30, y=210)
                self.day_entry_value = price
                self.day_entry = ctk.CTkEntry(self.root, placeholder_text="30000", font=("Helvetica", 25), corner_radius=20,
                                              border_color="#FF9999", height=55, width=200)
                self.day_entry.insert(0, self.day_entry_value)
                self.day_entry.place(x=130, y=200)

            if type == "Tuần":
                self.week = ctk.CTkLabel(self.root, text="Tuần", font=("Helvetica", 25)).place(x=30, y=310)
                self.week_entry_value = price
                self.week_entry = ctk.CTkEntry(self.root, placeholder_text="30000", font=("Helvetica", 25), corner_radius=20,
                                              border_color="#FF9999", height=55, width=200)
                self.week_entry.insert(0, self.week_entry_value)
                self.week_entry.place(x=130, y=300)

            if type == "Tháng":
                self.month = ctk.CTkLabel(self.root, text="Tháng", font=("Helvetica", 25)).place(x=30, y=410)
                self.month_entry_value = price
                self.month_entry = ctk.CTkEntry(self.root, placeholder_text="30000", font=("Helvetica", 25), corner_radius=20,
                                              border_color="#FF9999", height=55, width=200)
                self.month_entry.insert(0, self.month_entry_value)
                self.month_entry.place(x=130, y=400)

        save = ctk.CTkButton(master=self.root,text="LƯU",font=("Helvetica", 18),command=self.save,text_color="white",hover=True,hover_color="#ffb557",
            height=40,width=120,border_width=2,corner_radius=20,border_color="#bc863f",fg_color="#eda850")\
            .place(x=120,y=500)
    def save(self):
        price_hour = self.hour_entry.get()
        price_day = self.day_entry.get()
        price_week = self.week_entry.get()
        price_month = self.month_entry.get()
        data = [
            {'Type': 'Giờ', 'Price': price_hour},
            {'Type': 'Ngày', 'Price': price_day},
            {'Type': 'Tuần', 'Price': price_week},
            {'Type': 'Tháng', 'Price': price_month}
        ]
        self.db.fb.put('/','Price_List', data)
        messagebox.showinfo("Success", " Sửa thành công \U0001F604 ")
        self.root.destroy()

