import customtkinter as ctk
import tkinter as tk
from tkinter import *
from Firebase import database
from datetime import datetime
from tkinter import messagebox
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
appWidth, appHeight = 1000, 550
class regis:
    def __init__(self, license_plate, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry(f"{appWidth}x{appHeight}")
        main_font = ctk.CTkFont(family="Helvetica", size=12)
        text_font = ctk.CTkFont(family="Helvetica",size=17)
        # Kết nối đến Firebase
        self.db = database()
        self.Thongtin = ctk.CTkLabel(self.root,text="Information",font=("Helvetica", 30),height=40,
            width=320).place(x = 50 , y = 20 )
        self.Regis = ctk.CTkLabel(self.root,text="Register",font=("Helvetica", 30),height=40,
            width=320).place(x = 530 , y = 20 )

        self.ten_chu = ctk.CTkLabel(self.root,text="Name",font=("Helvetica", 15)).place(x = 30,y = 100 )
        self.ten_chu_entry = ctk.CTkEntry(self.root,placeholder_text="Name",corner_radius=10,border_color="#FF9999",height=35,width=200)
        self.ten_chu_entry.place(x = 130,y = 100 )

        self.id = ctk.CTkLabel(self.root,text="ID",font=("Helvetica", 15)).place(x = 30 , y = 150 )
        self.id_entry = ctk.CTkEntry(self.root,placeholder_text="ID",corner_radius=10,border_color="#FF9999",height=35,width=200)
        self.id_entry.place(x = 130 , y = 150 )

        self.sdt = ctk.CTkLabel(self.root,text="SDT",font=("Helvetica", 15)).place(x = 30,y = 200 )
        self.sdt_entry = ctk.CTkEntry(self.root,placeholder_text="SDT",corner_radius=10,border_color="#FF9999",height=35,width=200)
        self.sdt_entry.place(x = 130,y = 200 )

        self.cccd = ctk.CTkLabel(self.root,text="CCCD",font=("Helvetica", 15)).place(x = 30,y = 250 )
        self.cccd_entry = ctk.CTkEntry(self.root,placeholder_text="CCCD",corner_radius=10,border_color="#FF9999",height=35,width=200)
        self.cccd_entry.place(x = 130,y = 250 )

        self.bs = ctk.CTkLabel(self.root,text="L_Plate",font=("Helvetica", 15)).place(x = 30,y = 300 )
        self.bien_so_entry = ctk.CTkEntry(self.root,placeholder_text="L_Plate",corner_radius=10,border_color="#FF9999",height=35,width=200)
        self.bien_so_entry.place(x=130, y=300)

        self.price_frame = ctk.CTkFrame(self.root,border_color="#FF99FF",fg_color="#EEEEEE",border_width=3,corner_radius=20,width=270 ,height=150).place(x=400,y=100)
        #Gender Radio Buttons
        self.time_var = tk.StringVar(value="")
        self.hour_radio = ctk.CTkRadioButton(master=self.root,text="Hour",variable=self.time_var, value="Giờ",radiobutton_height=30,radiobutton_width=30).place(x=420,y=120)

        self.day_radio = ctk.CTkRadioButton(self.root,text="Day",variable=self.time_var,width=70,value="Ngày",radiobutton_height=30,radiobutton_width=30).place(x=560,y=120)

        self.week_radio = ctk.CTkRadioButton(self.root,text="Week",variable=self.time_var,value="Tuần",radiobutton_height=30,radiobutton_width=30).place(x=420,y=200)

        self.month_radio = ctk.CTkRadioButton(self.root,text="Month",variable=self.time_var,width=70,value="Tháng",radiobutton_height=30,radiobutton_width=30).place(x=560,y=200)

        # Thanh toán
        self.thanhtoan = ctk.CTkFrame(self.root, border_color="#FF99FF", fg_color="#EEEEEE", border_width=3,
                                        corner_radius=20, width=270, height=200).place(x=400, y=280)
        self.quantity_entry = ctk.CTkEntry(self.root, placeholder_text="Quantity", corner_radius=10, border_color="#FF9999",
                                      width=220)
        self.quantity_entry.place(x=420, y=300)
        self.btn_client = ctk.CTkButton(master=self.root,text="Pay", command=self.calculate_total,font=("Helvetica", 15),text_color="white",hover=True,hover_color="#e06a61",
            height=40,width=120,border_width=2,corner_radius=20,border_color="#9e4a43",fg_color="#FF6666").place(x=470, y=345)
        self.total_entry = ctk.CTkTextbox(self.root,font=text_font, width=220,border_color="#FF9999", border_width=1,height=50,corner_radius=20)
        self.total_entry.place(x=420,y=400)
        # Bảng giá
        self.thanhtoan = ctk.CTkFrame(self.root, border_color="#33FFFF", fg_color="#EEEEEE", border_width=3,
                                      corner_radius=20, width=220, height=380).place(x=700, y=100)
        label = ctk.CTkLabel(master=self.root,text="Price List",width=140,height=45,fg_color="#FF99FF",font=text_font,corner_radius=10)
        label.place(x=742,y=115)
        data = self.db.get_price_list()
        data = list(filter(None, data))
        for item in data:
            price = item.get('Price', '')
            type = item.get('Type', '')

            # Kiểm tra loại và gán giá trị vào entry tương ứng
            if type == 'Giờ':
                self.label_hour = ctk.CTkLabel(self.root, text="Hour", font=text_font).place(x=720, y=200)
                self.entry_hour_value = price
                self.entry_hour = ctk.CTkEntry(self.root, font=text_font, corner_radius=15, border_color="#3399FF",
                                               width=120)
                self.entry_hour.insert(0, self.entry_hour_value)
                self.entry_hour.place(x=775, y=200)
                self.entry_hour.configure(state='readonly')
            elif type == 'Ngày':
                self.label_day = ctk.CTkLabel(self.root, text="Day", font=text_font).place(x=720, y=260)
                self.entry_day_value = price
                self.entry_day = ctk.CTkEntry(self.root, font=text_font, corner_radius=15, border_color="#3399FF",
                                              width=120)
                self.entry_day.insert(0, self.entry_day_value)
                self.entry_day.place(x=775, y=260)
                self.entry_day.configure(state='readonly')
            elif type == 'Tuần':
                self.label_day = ctk.CTkLabel(self.root, text="Week", font=text_font).place(x=720, y=320)
                self.entry_week_value = price
                self.entry_week = ctk.CTkEntry(self.root, font=text_font, corner_radius=15, border_color="#3399FF",
                                               width=120)
                self.entry_week.insert(0, self.entry_week_value)
                self.entry_week.place(x=775, y=320)
                self.entry_week.configure(state='readonly')
            elif type == 'Tháng':
                self.label_day = ctk.CTkLabel(self.root, text="Month", font=text_font).place(x=720, y=380)
                self.entry_month_value = price
                self.entry_month = ctk.CTkEntry(self.root, font=text_font, corner_radius=15, border_color="#3399FF",
                                                width=120)
                self.entry_month.insert(0, self.entry_month_value)
                self.entry_month.place(x=775, y=380)
                self.entry_month.configure(state='readonly')

        save = ctk.CTkButton(master=self.root,text="SAVE",font=("Helvetica", 15),command=self.save_data,text_color="white",hover=True,hover_color="#ffb557",
            height=40,width=120,border_width=2,corner_radius=20,border_color="#bc863f",fg_color="#eda850")\
            .place(x=160,y=380)
        # self.license_plate = "80X24331"
        # self.car_card = "458EEB2AA"
        if (self.db.check_license_plate(license_plate)):
            self.check = 1
            list_info = self.db.get_car_info(license_plate)
            self.ten_chu_entry.insert(0, "")
            self.ten_chu_entry.insert(0, list_info['Name'])
            self.ten_chu_entry.configure(state='readonly')
            self.id_entry.insert(0, "")
            self.id_entry.insert(0, list_info['ID_owner'])
            self.id_entry.configure(state='readonly')
            self.sdt_entry.insert(0, "")
            self.sdt_entry.insert(0, list_info['Phone'])
            self.sdt_entry.configure(state='readonly')
            self.cccd_entry.insert(0, "")
            self.cccd_entry.insert(0, list_info['CCCD'])
            self.cccd_entry.configure(state='readonly')
            self.bien_so_entry.insert(0, "")
            self.bien_so_entry.insert(0, list_info['L_Plate'])
            self.bien_so_entry.configure(state='readonly')
        else:
            self.check = 0
            #load id_owner
            result1 = self.db.fb.get('/Customer', None)
            if result1 is None:
                id2 = 1
            else:
                id2 = len(result1)
            self.id_entry.insert(0,"")
            self.id_entry.configure(state='normal')
            self.id_entry.delete(0, 'end')
            self.id_entry.insert(0, id2)
            self.id_entry.configure(state='readonly')
            # load biển số
            self.bien_so_entry.insert(0, "")
            self.bien_so_entry.configure(state='normal')
            self.bien_so_entry.delete(0, 'end')
            self.bien_so_entry.insert(0, license_plate)
            self.bien_so_entry.configure(state='readonly')
        # Hàm lấy giá tiền từ radiobutton

    def get_price(self):
        data = self.db.get_price_list()
        data = list(filter(None, data))
        for item in data:
            price = item.get('Price', '')
            type = item.get('Type', '')
            if self.time_var.get() == type:
                return int(price)
            elif self.time_var.get() == type:
                return int(price)
            elif self.time_var.get() == type:
                return int(price)
            elif self.time_var.get() == type:
                return int(price)

        # Hàm tính tiền và hiển thị kết quả

    def calculate_total(self):
        price = self.get_price()
        self.quantity_entry.insert(0,"")
        quantity = float(self.quantity_entry.get())
        total = price * quantity
        self.total_entry.delete(1.0, END)
        # self.total_entry.insert(0,"")
        self.total_entry.insert(1.0, str(total) + " VND")

    def validate_phone_number(self,phone_number):
        # Kiểm tra độ dài số điện thoại
        if len(phone_number) != 10:
            return False
        # Kiểm tra số điện thoại bắt đầu bằng các số từ 09 đến 08
        prefix = phone_number[:3]
        if prefix not in ["093", "090", "012", "089", "091", "094", "088", "096", "097", "098", "016", "086", "092",
                          "018",
                          "099", "019"]:
            return False
        # Số điện thoại hợp lệ
        return True
    def validate_phone_cccd(self,cccd):
        # Kiểm tra độ dài số điện thoại
        if len(cccd) != 10:
            return False
        # Số điện thoại hợp lệ
        return True
    def save_data(self):
        if self.bien_so_entry.get() == "" or self.cccd_entry.get() == "" or self.ten_chu_entry.get() == "" or self.id_entry.get() == "" or self.sdt_entry.get() == "" or self.quantity_entry.get() == "" or self.total_entry.get(1.0,END) == "":
            messagebox.showinfo("Thong bao", "Vui long nhap day du thong tin")
        else :
            # Connect firebase
            result = self.db.fb.get('/Car-management', None)
            if result is None:
                id1 = 1
            else:
                id1 = len(result)
            result1 = self.db.fb.get('/Customer', None)
            if result1 is None:
                id2 = 1
            else:
                id2 = len(result1)
            # Get input data
            name = self.ten_chu_entry.get()
            sdt = self.sdt_entry.get()
            cccd = self.cccd_entry.get()
            id_owner = self.id_entry.get()
            bs = self.bien_so_entry.get()
            if self.time_var.get() == "Giờ":
                period_time = str(float(self.quantity_entry.get())) + "h"
            if self.time_var.get() == "Ngày":
                period_time = str(float(self.quantity_entry.get()) * 24) + "h"
            if self.time_var.get() == "Tuần":
                period_time = str(float(self.quantity_entry.get()) * 120) + "h"
            if self.time_var.get() == "Tháng":
                period_time = str(float(self.quantity_entry.get()) * 720) + "h"
            # num_hours = int(period_time[:-1])  # Lấy phần số trong chuỗi "48h"
            total_money_string = self.total_entry.get("1.0", "end")  # Chuyển sang kiểu chuỗi để lưu vào Firebase

            # Check for duplicate CCCD or phone number
            duplicate_cccd = False
            duplicate_phone = False
            if result1 is not None:
                for data in result1:
                    if data is not None and 'CCCD' in data and data['CCCD'] == cccd:
                        duplicate_cccd = True
                        break
                    if data is not None and 'Phone' in data and data['Phone'] == sdt:
                        duplicate_phone = True
                        break
            # Add data to Firebase or show error message
            if self.check == 0:
                if duplicate_cccd:
                    messagebox.showerror("Duplicate", "Số CCCD đã tồn tại . Vui lòng nhập lại.")
                elif duplicate_phone:
                    messagebox.showerror("Duplicate", "Số điện thoại đã tồn tại . Vui lòng nhập lại.")
                elif self.validate_phone_number(sdt) == False:
                        messagebox.showerror("Duplicate", "Số điện thoại không hợp lệ . Vui lòng nhập lại.")
                elif self.validate_phone_cccd(cccd) == False:
                        messagebox.showerror("Duplicate", "Căn cước công dân không hợp lệ . Vui lòng nhập lại.")
                else:
                    car_data = {
                        "ID": id1,
                        "ID_owner": id_owner,
                        "Time-register": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "Period-time": period_time,
                        "Total-money": total_money_string
                    }
                    customer = {
                        "ID_owner": id_owner,
                        "Name": name,
                        "CCCD": cccd,
                        "Phone": sdt,
                    }
                    l_plate = {
                        "ID_owner": id_owner,
                        "L_Plate": bs
                    }
                    self.db.fb.put('/Car-management', id1, car_data)
                    self.db.fb.put('/Customer',id2,customer)
                    self.db.fb.put('/L_Plate', id2,l_plate)
                    # self.db.add_license_plate(self.car_card, self.license_plate)
                    messagebox.showinfo("Success", " Đăng kí thành công ")
                    self.root.destroy()
            else:
                car_data = {
                    "ID": id1,
                    "ID_owner": id_owner,
                    "Time-register": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Period-time": period_time,
                    "Total-money": total_money_string
                }
                customer = {
                    "ID_owner": id_owner,
                    "Name": name,
                    "CCCD": cccd,
                    "Phone": sdt,
                }
                l_plate = {
                    "ID_owner": id_owner,
                    "L_Plate": bs
                }
                self.db.fb.put('/Car-management', id1, car_data)
                # self.db.add_license_plate(self.car_card, self.license_plate)
                messagebox.showinfo("Success", " Đăng kí thành công ")
                self.root.destroy()
                # if self.check == 0:
                #     self.db.fb.put('/Car-management', id1, car_data)
                #     self.db.fb.put('/Customer',id2,customer)
                #     self.db.fb.put('/L_Plate', id2,l_plate)
                #     # self.db.add_license_plate(self.car_card, self.license_plate)
                #     messagebox.showinfo("Success", " Đăng kí thành công ")
                #     self.root.destroy()

