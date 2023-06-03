from tkinter import *
from Firebase import database
from datetime import datetime
from tkinter import messagebox
class regis:
    def __init__(self, license_plate, root):
        self.root = root
        self.root.geometry("1099x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Register")

        # Tạo frame chứa các thành phần trên màn hình trái
        self.left_frame = Frame(self.root, width=540, height=600, bg="white",bd=0, highlightthickness=5, highlightbackground="orange")
        self.left_frame.place(x=40,y=0,width=400,height=600)

        # Thêm tiêu đề "THÔNG TIN" và các ô nhập thông tin vào frame trái
        title_label = Label(self.left_frame, text="THÔNG TIN XE", font=("Arial", 20),bg="white")
        title_label.pack(pady=20)

        Label(self.left_frame, text="Tên chủ:", font=("Arial", 12),bg="white").pack(pady=10)
        self.ten_chu_entry = Entry(self.left_frame, font=("Arial", 12), width=30)
        self.ten_chu_entry.pack()

        Label(self.left_frame, text="ID:", font=("Arial", 12),bg="white").pack(pady=10)
        self.id_entry = Entry(self.left_frame, font=("Arial", 12), width=30)
        self.id_entry.pack()

        Label(self.left_frame, text="Số điện thoại:", font=("Arial", 12),bg="white").pack(pady=10)
        self.sdt_entry = Entry(self.left_frame, font=("Arial", 12), width=30)
        self.sdt_entry.pack()

        Label(self.left_frame, text="CCCD:", font=("Arial", 12),bg="white").pack(pady=10)
        self.cccd_entry = Entry(self.left_frame, font=("Arial", 12), width=30)
        self.cccd_entry.pack()

        Label(self.left_frame, text="Biển số:", font=("Arial", 12),bg="white").pack(pady=10)
        self.bien_so_entry = Entry(self.left_frame, font=("Arial", 12), width=30)
        self.bien_so_entry.pack()

        # Tạo frame chứa các thành phần trên màn hình phải
        self.right_frame = Frame(self.root, width=540, height=600, bg="white", bd=0, highlightthickness=5,
                                highlightbackground="orange")
        self.right_frame.place(x=480, y=0, width=600, height=600)

        # Thêm tiêu đề "ĐĂNG KÍ" vào frame phải
        title_label = Label(self.right_frame, text="ĐĂNG KÍ", font=("Arial", 20),bg="white")
        title_label.pack(pady=20)

        #Tạo frame chứa bảng giá
        price_frame = Frame(self.right_frame, bg="white", bd=0, highlightthickness=2,
                                highlightbackground="pink")
        price_frame.place(x=360 , y =70 , width=220,height=430)

        title_price_frame = Frame(price_frame,bg="white", bd=0, highlightthickness=2,
                                highlightbackground="white")
        title_price_frame.place(x=0,y=0,width=150,height=40)
        title_price = Label(title_price_frame, text="BẢNG GIÁ", font=("Arial", 14),bg="white")
        title_price.place(x=5 , y = 5 )
        # Giờ
        Label(price_frame, text="Giờ :", font=("Arial", 12),bg="white").place(x = 25 , y = 80 , width=50 , height=30)
        quantity_entry = Entry(price_frame, font=("Arial", 12), width=30)
        quantity_entry.place(x = 85 , y = 80, width=120 , height=30)
        quantity_entry.insert(0,"3000 VND")
        quantity_entry.configure(state='readonly')
        # Ngày
        Label(price_frame, text="Ngày :", font=("Arial", 12), bg="white").place(x=25, y=160, width=50, height=30)
        quantity_entry = Entry(price_frame, font=("Arial", 12), width=30)
        quantity_entry.place(x=85, y=160, width=120, height=30)
        quantity_entry.insert(0,"30000 VND")
        quantity_entry.configure(state='readonly')
        # Tuần
        Label(price_frame, text="Tuần :", font=("Arial", 12), bg="white").place(x=25, y=240, width=50, height=30)
        quantity_entry = Entry(price_frame, font=("Arial", 12), width=30)
        quantity_entry.place(x=85, y=240, width=120, height=30)
        quantity_entry.insert(0,"500000 VND")
        quantity_entry.configure(state='readonly')
        # Tháng
        Label(price_frame, text="Tháng :", font=("Arial", 12), bg="white").place(x=25, y=320, width=50, height=30)
        quantity_entry = Entry(price_frame, font=("Arial", 12), width=30)
        quantity_entry.place(x=85, y=320, width=120, height=30)
        quantity_entry.insert(0,"1500000 VND")
        quantity_entry.configure(state='readonly')
        # Tạo frame chứa các radio button
        radio_frame = Frame(self.right_frame, bg="white", bd=0, highlightthickness=2,
                                highlightbackground="pink")
        radio_frame.place(x=30 , y =70 , width=300,height=200)

        # Thêm 4 radio button vào frame mới
        self.time_var = StringVar()
        #time_var.set("Giờ")
        hour_radio = Radiobutton(radio_frame, text="Giờ", font=("Arial", 12), variable=self.time_var, value="Giờ",bg="white")
        hour_radio.place(x=80,y=10)
        day_radio = Radiobutton(radio_frame, text="Ngày", font=("Arial", 12), variable=self.time_var, value="Ngày",bg="white")
        day_radio.place(x=80,y=60)
        week_radio = Radiobutton(radio_frame, text="Tuần", font=("Arial", 12), variable=self.time_var, value="Tuần",bg="white")
        week_radio.place(x=80,y=110)
        month_radio = Radiobutton(radio_frame, text="Tháng", font=("Arial", 12), variable=self.time_var, value="Tháng",bg="white")
        month_radio.place(x=80,y=160)

        # Tạo frame chứa so luong va thanh tien
        frame = Frame(self.right_frame, bg="white", bd=0, highlightthickness=2,
                                highlightbackground="pink")
        frame.place(x=30 , y =300 , width=300,height=200)
        # Thêm ô nhập "số lượng"
        Label(frame, text="Số lượng:", font=("Arial", 12),bg="white").pack(pady=10)
        self.quantity_entry = Entry(frame, font=("Arial", 12), width=30)
        self.quantity_entry.pack()

        # Thêm ô nhập "Thành tiền"
        Button(frame, text="Thành tiền", font=("Arial", 12), bg="white", command=self.calculate_total).pack(pady=10)
        self.total_entry = Entry(frame, font=("Arial", 12), width=30)
        self.total_entry.pack()

        # Thêm button "Lưu"
        save = Button(self.right_frame, text="Save", bd=0, font=("Goudy old style", 15), bg="pink", fg="white",command=self.save_data)
        save.place(x=480, y=530, width=100, height=40)

        # Kết nối đến Firebase
        self.db = database()

        if (self.db.check_license_plate(license_plate)):
            list_info = self.db.get_car_info(license_plate)
            self.ten_chu_entry.insert(0, list_info['Owner-name'])
            self.ten_chu_entry.configure(state='readonly')
            self.id_entry.insert(0, list_info['ID_owner'])
            self.id_entry.configure(state='readonly')
            self.sdt_entry.insert(0, list_info['Phone'])
            self.sdt_entry.configure(state='readonly')
            self.cccd_entry.insert(0, list_info['CCCD'])
            self.cccd_entry.configure(state='readonly')
            self.bien_so_entry.insert(0, list_info['L_Plate'])
            self.bien_so_entry.configure(state='readonly')
        else:
            # chỉ load biển số
            self.bien_so_entry.configure(state='normal')
            self.bien_so_entry.delete(0, 'end')
            self.bien_so_entry.insert(0, license_plate)
            self.bien_so_entry.configure(state='readonly')
    # Hàm lấy giá tiền từ radiobutton
    def get_price(self):
        if self.time_var.get() == "Giờ":
            return 3000
        elif self.time_var.get() == "Ngày":
            return 30000
        elif self.time_var.get() == "Tuần":
            return 500000
        elif self.time_var.get() == "Tháng":
            return 1500000

    # Hàm tính tiền và hiển thị kết quả
    def calculate_total(self):
        price = self.get_price()
        quantity = int(self.quantity_entry.get())
        total = price * quantity
        self.total_entry.delete(0, END)
        self.total_entry.insert(0, str(total) + " VND")
    def save_data(self):
        if self.bien_so_entry.get() == "" or self.cccd_entry.get() == "" or self.ten_chu_entry.get() == "" or self.id_entry.get() == "" or self.sdt_entry.get() == "" or self.quantity_entry.get() == "" or self.total_entry.get() == "" :
            messagebox.showinfo("Thong bao","Vui long nhap day du thong tin") 
        else :
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
            name = self.ten_chu_entry.get()
            sdt = self.sdt_entry.get()
            cccd = self.cccd_entry.get()
            id_owner = self.id_entry.get()
            bs = self.bien_so_entry.get()
            if self.get_price() == 3000:
                period_time = self.quantity_entry.get() + "h"
            if self.get_price() == 30000:
                period_time = str(int(self.quantity_entry.get())*24) + "h"
            if self.get_price() == 500000:
                period_time = str(int(self.quantity_entry.get())*120) + "h"
            if self.get_price() == 1500000:
                period_time = str(int(self.quantity_entry.get())*720) + "h"
            # num_hours = int(period_time[:-1])  # Lấy phần số trong chuỗi "48h"
            total_money_string = self.total_entry.get()  # Chuyển sang kiểu chuỗi để lưu vào Firebase

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
                    "ID_owner": id_owner,
                    "Phone": sdt,
                    "CCCD": cccd,
                    "Time-register": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Period-time": period_time,
                    "Total-money": total_money_string
                }
                lp_car = {
                    "ID_owner": id_owner,
                    "L_Plate": bs
                }
                self.db.fb.put('/LP_Car',id2,lp_car)
                self.db.fb.put('/Car-management', id1, car_data)
                messagebox.showinfo("Success", "Đã thêm dữ liệu thành công.")
                self.root.destroy()