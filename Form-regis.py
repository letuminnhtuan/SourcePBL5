import tkinter as tk
from Firebase import database
from datetime import datetime
class Form(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.total_money = 0

    def create_widgets(self):
        self.label_owner = tk.Label(self, text="Tên chủ:")
        self.label_owner.grid(row=0, column=0, padx=5, pady=5)

        self.entry_owner = tk.Entry(self)
        self.entry_owner.grid(row=0, column=1, padx=5, pady=5)

        self.label_phone = tk.Label(self, text="Số điện thoại:")
        self.label_phone.grid(row=1, column=0, padx=5, pady=5)

        self.entry_phone = tk.Entry(self)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        self.label_cccd = tk.Label(self, text="CCCD:")
        self.label_cccd.grid(row=2, column=0, padx=5, pady=5)

        self.entry_cccd = tk.Entry(self)
        self.entry_cccd.grid(row=2, column=1, padx=5, pady=5)

        self.label_period_time = tk.Label(self, text="Thời hạn đăng ký (giờ):")
        self.label_period_time.grid(row=3, column=0, padx=5, pady=5)

        self.period_time_entry = tk.Entry(self)
        self.period_time_entry.grid(row=3, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(self, text="Lưu thông tin", command=self.save_data)
        self.submit_button.grid(row=5, column=1, padx=5, pady=5)

        self.label_price_per_day = tk.Label(self, text="Giá tiền mỗi giờ:")
        self.label_price_per_day.grid(row=4, column=0, padx=5, pady=5)

        self.entry_price_per_day = tk.Entry(self)
        self.entry_price_per_day.grid(row=4, column=1, padx=5, pady=5)

    def save_data(self):
        # Connect firebase
        self.firebase = database()
        result = self.firebase.fb.get('/Car-management', None)
        if result is None:
            id = 1
        else:
            id = len(result)
        name = self.entry_owner.get()
        sdt = self.entry_phone.get()
        cccd = self.entry_cccd.get()
        period_time = self.period_time_entry.get() + "h"
        num_hours = int(period_time[:-1])  # Lấy phần số trong chuỗi "48h"
        price_per_hour = int(self.entry_price_per_day.get())  # Giá 1 giờ
        total_money = num_hours * price_per_hour
        total_money_string = str(total_money) + " VND"  # Chuyển sang kiểu chuỗi để lưu vào Firebase
        car_data = {
            "Id": id,
            "Owner-name": name,
            "Phone": sdt,
            "CCCD": cccd,
            "Time-register": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Period-time": period_time,
            "Total-money": total_money_string
        }
        # Thêm đối tượng vào Firebase
        self.firebase.fb.put('/Car-management', id, car_data)
root = tk.Tk()
my_gui = Form(root)
root.mainloop()