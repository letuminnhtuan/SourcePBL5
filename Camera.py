from tkinter import *
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import threading
import tkinter as tk
from Dashboard import db
from Firebase import database
from Register import regis
from Handle import *
import time
import customtkinter

class QL_Camera:
    def __init__(self, master):
        self.root = master
        self.root.title("Quản lí bãi xe")
        self.root.geometry("1500x800")
        self.root.resizable(False, False)
        self.database = database()
        # self.root.attributes("-fullscreen", True)
        # Tạo PanedWindow và chia màn hình thành hai bên
        self.paned_window = PanedWindow(self.root, orient=HORIZONTAL, sashwidth=5,bg="pink")
        self.paned_window.pack(fill=BOTH, expand=True)

        # Tạo hai Frame để đặt vào hai bên của thanh chia đôi
        self.frame_left = Frame(self.paned_window, width=750, height=800,bg="white")
        self.frame_right = Frame(self.paned_window, width=750, height=800,bg="white")

        # Thêm Frame chia đôi vào thanh chia đôi
        self.split_frame = Frame(self.paned_window, background="gray", width=5, height=500)
        self.paned_window.add(self.frame_left)
        self.paned_window.add(self.split_frame)
        self.paned_window.add(self.frame_right)
        # Button 1
        manager = Button(self.frame_left, text="Quản lí", bd=0, font=("Helvetica", 18), bg="#6162FF", fg="white",
                         command=self.tranfer_DB)
        manager.place(x=50, y=30, width=100, height=40)
        # Button 2
        back = Button(self.frame_right, text="Thoát", bd=0, font=("Helvetica", 18), bg="#6162FF", fg="white",
                      command=self.logout_function)
        back.place(x=620, y=20, width=100, height=40)
        #title_left
        icon2 = Image.open("Picture/title1.png")
        icon2 = icon2.resize((360, 140), Image.LANCZOS)
        self.icon_image2 = ImageTk.PhotoImage(icon2)
        icon_label2 = Label(self.frame_left, image=self.icon_image2,bg="white")
        icon_label2.place(x=220,y=0)
        #title_right
        icon1 = Image.open("Picture/title1.png")
        icon1 = icon1.resize((360, 140), Image.LANCZOS)
        self.icon_image1 = ImageTk.PhotoImage(icon1)
        icon_label2 = Label(self.frame_right, image=self.icon_image1, bg="white")
        icon_label2.place(x=220, y=0)
        # Title
        label_xe_vao = Label(self.frame_left, text="Xe vào", font=("Helvetica", 30, "bold"), fg="gray",bg="white").place(x=320, y=40, width=130, height=50)
        label_xe_ra = Label(self.frame_right, text="Xe ra", font=("Helvetica", 30, "bold"), fg="gray",bg="white").place(x=340, y=40, width=100, height=50)

        # Thêm Label để hiển thị hình ảnh từ camera trái
        self.label_camera_left = tk.Label(self.frame_left,width=650,height=430,bg="white")
        self.label_camera_left.pack(padx=10, pady=10)
        self.label_camera_left.place(relx=0.5, rely=0.47, anchor=CENTER) # Chỉnh vị trí label chứa camera ra giữa
        self.label_camera_left.config(width=650,height=430)

        # Thêm Label để hiển thị hình ảnh từ camera phải
        self.label_camera_right = tk.Label(self.frame_right, width=650, height=430, bg="white")
        self.label_camera_right.pack(padx=10, pady=10)
        self.label_camera_right.place(relx=0.5, rely=0.47, anchor=CENTER)  # Chỉnh vị trí label chứa camera ra giữa
        self.label_camera_right.config(width=650, height=430) # Chỉnh kích thước camera

        # --------- KHỞI TẠO CAMERA TRÁI ------------
        self.cap_left = cv2.VideoCapture(0) # khởi tạo biến cap_left để lấy camera bên trái
        # --------- KHỞI TẠO THREAD ĐỂ CHẠY HÀM Updata_camera_left---------
        self.thread_left = threading.Thread(target=self.update_camera_left)
        self.thread_left.daemon = True
        self.thread_left.start()

        # ---------- KHỞI TẠO CAMERA PHẢI --------------
        self.cap_right = cv2.VideoCapture(1) # Khởi tạo biến cap_right để lấy camera bên phải
        # --------- KHỞI TẠO THREAD ĐỂ CHẠY HÀM Updata_camera_right-----------
        self.thread_right = threading.Thread(target=self.update_camera_right)
        self.thread_right.daemon = True
        self.thread_right.start()

        data_thread = threading.Thread(target=self.data_handler, args=(arData, self.cap_left, self.cap_right,))
        data_thread.start()

        button_open_vao = customtkinter.CTkButton(
            master=self.frame_left,
            command=self.open_vao,
            text="Mở cổng vào",
            font=("Helvetica", 20, "bold"),
            text_color="white",
            hover=True,
            hover_color="#6fb9d5",
            height=55,
            width=160,
            border_width=2,
            corner_radius=20,
            border_color="#528aa0",
            fg_color="#6162FF").place(x = 300 , y = 700)
        button_open_ra = customtkinter.CTkButton(
            master=self.frame_right,
            command=self.open_ra,
            text="Mở cổng ra",
            font=("Helvetica", 20, "bold"),
            text_color="white",
            hover=True,
            hover_color="#6fb9d5",
            height=55,
            width=160,
            border_width=2,
            corner_radius=20,
            border_color="#528aa0",
            fg_color="#6162FF").place(x=330, y=700)
    
    def open_vao(self):
        SendData('6')
        time.sleep(.1)

    def open_ra(self):
        SendData('5')
        time.sleep(.1)

    # Hàm cập nhật camera xe vào lên giao điện
    def update_camera_left(self):
        # data_thread = threading.Thread(target=self.data_handler_in, args=(arData, self.cap_left,))
        # data_thread.start()
        while True: # Lặp vô hạn để lấy hình ảnh từ camera
            ret, frame = self.cap_left.read() # Gọi phương thức read của đối tượng cap_left ở trên để lấy hình ảnh từ camera trái
            if ret: # Kiểm tra xem có lấy được ảnh từ camera không
                # Chuyển đổi hình ảnh vừa lấy được từ camera sang định dạng PIL để hiển thị lên giao diện
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                # Hiển thị hình ảnh trong Label ( cập nhật hình ảnh mới nhật lên label )
                self.label_camera_left.configure(image=image)
                self.label_camera_left.image = image
    def update_camera_right(self):
        # data_thread = threading.Thread(target=self.data_handler_out, args=(arData, self.cap_right,))
        # data_thread.start()
        while True:# Lặp vô hạn để lấy hình ảnh từ camera
            # Lấy hình ảnh từ camera
            ret, frame = self.cap_right.read()# Gọi phương thức read của đối tượng cap_left ở trên để lấy hình ảnh từ camera phải
            if ret:# Kiểm tra xem có lấy được ảnh từ camera không
                # Chuyển đổi hình ảnh vừa lấy được từ camera sang định dạng PIL để hiển thị lên giao diện
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                # Hiển thị hình ảnh trong Label ( cập nhật hình ảnh mới nhật lên label )
                self.label_camera_right.configure(image=image)
                self.label_camera_right.image = image
    def data_handler(self, arData, cap_left, cap_right):
        while True:
            if arData.in_waiting == 0:
                continue
            else:
                data1 = arData.readline().decode().rstrip().upper()
                time.sleep(1)
                data2 = arData.readline().decode().rstrip().upper()
                if data1 == "IN":
                    _, img = cap_left.read()
                    num_plate = plate(img)
                    num = list(num_plate)
                    temp = self.database.get_Plate(data2)
                    if(len(num) != 0):
                        if temp == "":
                            self.tranfer_Regis(num[0])
                            self.database.add_license_plate(card=data2, license_plate=num[0])
                        else:
                            print("Co")
                        SendData('1')
                    else:
                        SendData('0')
                elif data1 == "OUT":
                    _, img = cap_right.read()
                    num_plate = plate(img)
                    num = list(num_plate)
                    if len(num) != 0:
                        mess, check = self.database.check_card_license_plate(card=data2, license_plate=num[0])
                        print(check)
                        if(check != None):
                            if(check >= 0):
                                self.database.set_Plate(data2)
                        messagebox.showinfo("Thông báo", mess)
                        if(mess != 'Không hợp lệ!!'):
                            SendData('3')
                        else:
                            SendData('2')
                    else:
                        SendData('2')
                time.sleep(.5)
    # Hàm chuyển sang trang Quản lí
    def tranfer_DB(self):
        self.open_new_DB()
    def open_new_DB(self):
        self.new_window = Toplevel(self.root)
        self.app = db(self.new_window)
    def logout_function(self):
        self.root.withdraw()
    def tranfer_Regis(self, plate):
        self.open_new_Regis(plate)
    def open_new_Regis(self, plate):
        self.new_window = Toplevel(self.root)
        self.app = regis(plate, self.new_window)