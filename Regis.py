from tkinter import *
from Firebase import database
from datetime import datetime
from tkinter import messagebox

class Form(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Register")
        self.pack()
        self.create_widgets()
        self.total_money = 0

    def create_widgets(self):
        self.label_owner = Label(self, text="Tên chủ:", width=15)
        self.label_owner.grid(row=0, column=0, padx=5, pady=5)

        self.entry_owner = Entry(self, width=30)
        self.entry_owner.grid(row=0, column=1, padx=5, pady=5)

        self.label_id = Label(self, text="ID :", width=15)
        self.label_id.grid(row=1, column=0, padx=5, pady=5)

        self.entry_id = Entry(self, width=30)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        self.label_phone = Label(self, text="Số điện thoại:", width=15)
        self.label_phone.grid(row=2, column=0, padx=5, pady=5)

        self.entry_phone = Entry(self, width=30)
        self.entry_phone.grid(row=2, column=1, padx=5, pady=5)

        self.label_cccd = Label(self, text="CCCD:", width=15)
        self.label_cccd.grid(row=3, column=0, padx=5, pady=5)

        self.entry_cccd = Entry(self, width=30)
        self.entry_cccd.grid(row=3, column=1, padx=5, pady=5)

        self.label_lp = Label(self, text="Biển số :", width=15)
        self.label_lp.grid(row=4, column=0, padx=5, pady=5)

        self.entry_lp = Entry(self, width=30)
        self.entry_lp.grid(row=4, column=1, padx=5, pady=5)

        self.label_period_time = Label(self, text="Thời hạn đăng ký (giờ):", width=15)
        self.label_period_time.grid(row=5, column=0, padx=5, pady=5)

        self.period_time_entry = Entry(self, width=30)
        self.period_time_entry.grid(row=5, column=1, padx=5, pady=5)

        self.label_price_per_day = Label(self, text="Giá tiền mỗi giờ:", width=15)
        self.label_price_per_day.grid(row=6, column=0, padx=5, pady=5)

        self.entry_price_per_day = Entry(self, width=30)
        self.entry_price_per_day.insert(0, "3000")
        self.entry_price_per_day.grid(row=6, column=1, padx=5, pady=5)

        self.submit_button = Button(self, text="Lưu thông tin", command=self.save_data, width=20)
        self.submit_button.grid(row=7, column=1, padx=5, pady=5)
        #Kết nối đến Firebase
        self.db = database()

        license_plate = "22F51411"
        if(self.db.check_license_plate(license_plate)):
            list_info = self.db.get_car_info(license_plate)
            self.entry_owner.insert(0,list_info['Owner-name'])
            self.entry_owner.configure(state='readonly')
            self.entry_id.insert(0,list_info['ID_owner'])
            self.entry_id.configure(state='readonly')
            self.entry_phone.insert(0,list_info['Phone'])
            self.entry_phone.configure(state='readonly')
            self.entry_cccd.insert(0,list_info['CCCD'])
            self.entry_cccd.configure(state='readonly')
            self.entry_lp.insert(0,list_info['L_Plate'])
            self.entry_lp.configure(state='readonly')
        else :
            # chỉ load biển số
            self.entry_lp.configure(state='normal')
            self.entry_lp.delete(0, 'end')
            self.entry_lp.insert(0, license_plate)
            self.entry_lp.configure(state='readonly')
        # print(self.db.get_car_info(license_plate))
        # print(self.db.get())
    def save_data(self):
        # Connect firebase
        result = self.db.fb.get('/Car-management', None)
        if result is None:
            id1 = 1
        else:
            id1 = len(result)
        result = self.db.fb.get('/LP_Car', None)
        if result is None:
            id2 = 1
        else:
            id2 = len(result)
        # Get input data
        name = self.entry_owner.get()
        sdt = self.entry_phone.get()
        cccd = self.entry_cccd.get()
        id_owner = self.entry_id.get()
        bs = self.entry_lp.get()
        period_time = self.period_time_entry.get() + "h"
        num_hours = int(period_time[:-1])  # Lấy phần số trong chuỗi "48h"
        price_per_hour = int(self.entry_price_per_day.get())  # Giá 1 giờ
        total_money = num_hours * price_per_hour
        total_money_string = str(total_money) + " VND"  # Chuyển sang kiểu chuỗi để lưu vào Firebase

        # Check for duplicate CCCD or phone number
        duplicate_cccd = False
        duplicate_phone = False
        if result is not None:
            for data in result:
                if data is not None and 'CCCD' in data and data['CCCD'] == cccd:
                    duplicate_cccd = True
                    break
                if data is not None and 'Phone' in data and data['Phone'] == sdt:
                    duplicate_phone = True
                    break

        # Add data to Firebase or show error message
        if duplicate_cccd:
            messagebox.showerror("Duplicate", "Số CCCD đã tồn tại trong cơ sở dữ liệu. Vui lòng nhập lại.")
        elif duplicate_phone:
            messagebox.showerror("Duplicate", "Số điện thoại đã tồn tại trong cơ sở dữ liệu. Vui lòng nhập lại.")
        else:
            car_data = {
                "Id": id1,
                "Owner-name": name,
                "ID_owner":id_owner,
                "Phone": sdt,
                "CCCD": cccd,
                "Time-register": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Period-time": period_time,
                "Total-money": total_money_string
            }
            lp_car = {
                "Id_owner":id_owner,
                "L_Plate":bs
            }
            self.db.fb.put('/LP_Car',id2,lp_car)
            self.db.fb.put('/Car-management', id1, car_data)
            messagebox.showinfo("Success", "Đã thêm dữ liệu thành công.")
root = Tk()
obj = Form(root)
root.mainloop()