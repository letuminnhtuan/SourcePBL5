from tkinter import *
import cv2
from PIL import Image, ImageTk
import threading
import tkinter as tk
from Dashboard import db
class camera_client:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lí bãi xe")
        self.root.geometry("1500x800")
        self.root.resizable(False, False)
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
        # Button
        back = Button(self.frame_right, text="Out", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white",
                      command=self.logout_function)
        back.place(x=620, y=20, width=100, height=40)
        #title_left
        icon2 = Image.open("Picture/title1.png")
        icon2 = icon2.resize((360, 140), Image.ANTIALIAS)
        self.icon_image2 = ImageTk.PhotoImage(icon2)
        icon_label2 = Label(self.frame_left, image=self.icon_image2,bg="white")
        icon_label2.place(x=220,y=0)
        #title_right
        icon1 = Image.open("Picture/title1.png")
        icon1 = icon1.resize((360, 140), Image.ANTIALIAS)
        self.icon_image1 = ImageTk.PhotoImage(icon1)
        icon_label2 = Label(self.frame_right, image=self.icon_image1, bg="white")
        icon_label2.place(x=220, y=0)
        # Title
        label_xe_vao = Label(self.frame_left, text="Xe vào", font=("Impact", 22, "italic"), fg="gray",bg="white").place(x=350, y=40, width=90, height=50)
        label_xe_ra = Label(self.frame_right, text="Xe ra", font=("Impact", 22, "italic"), fg="gray",bg="white").place(x=350, y=40, width=90, height=50)

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

        # Khởi tạo camera trái
        self.cap_left = cv2.VideoCapture(0)
        # Khởi tạo thread để chạy hàm update_camera_left()
        self.thread_left = threading.Thread(target=self.update_camera_left)
        self.thread_left.daemon = True
        self.thread_left.start()

        # Khởi tạo camera phải
        self.cap_right = cv2.VideoCapture(0)
        # Khởi tạo thread để chạy hàm update_camera_right()
        self.thread_right = threading.Thread(target=self.update_camera_right)
        self.thread_right.daemon = True
        self.thread_right.start()

        # THÔNG TIN CAMERA
        #Camera phải
        Label(self.frame_right, text="Id ", font=("Goudy old style", 14, "bold"), fg="grey", bg="white").place(x=60,
                                                                                                          y=625)
        self.id = Entry(self.frame_right, font=("Goudy old style", 7), bg="#E7E6E6", state="normal")
        self.id.place(x=270, y=620, width=320, height=35)

        Label(self.frame_right, text="Time out", font=("Goudy old style", 14, "bold"), fg="grey", bg="white").place(x=60,
                                                                                                               y=675)
        self.timeout = Entry(self.frame_right, font=("Goudy old style", 7), bg="#E7E6E6", state="normal")
        self.timeout.place(x=270, y=670, width=320, height=35)

        Label(self.frame_right, text="Biển số", font=("Goudy old style", 14, "bold"), fg="grey", bg="white").place(x=60,
                                                                                                              y=725)
        self.bienso = Entry(self.frame_right, font=("Goudy old style", 7), bg="#E7E6E6", state="normal")
        self.bienso.place(x=270, y=720, width=320, height=35)

        #Camera trái
        Label(self.frame_left, text="Id ", font=("Goudy old style", 14, "bold"), fg="grey", bg="white").place(x=60,
                                                                                                               y=625)
        self.id = Entry(self.frame_left, font=("Goudy old style", 7), bg="#E7E6E6", state="normal")
        self.id.place(x=270, y=620, width=320, height=35)

        Label(self.frame_left, text="Time in", font=("Goudy old style", 14, "bold"), fg="grey", bg="white").place(
            x=60,
            y=675)
        self.timein = Entry(self.frame_left, font=("Goudy old style", 7), bg="#E7E6E6", state="normal")
        self.timein.place(x=270, y=670, width=320, height=35)

        Label(self.frame_left, text="Biển số", font=("Goudy old style", 14, "bold"), fg="grey", bg="white").place(x=60,
                                                                                                                   y=725)
        self.bienso = Entry(self.frame_left, font=("Goudy old style", 7), bg="#E7E6E6", state="normal")
        self.bienso.place(x=270, y=720, width=320, height=35)
    def update_camera_left(self):
        while True:
            # Lấy hình ảnh từ camera
            ret, frame = self.cap_left.read()
            if ret:
                # Chuyển đổi hình ảnh sang định dạng PIL
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                # Hiển thị hình ảnh trong Label
                self.label_camera_left.configure(image=image)
                self.label_camera_left.image = image
    def update_camera_right(self):
        while True:
            # Lấy hình ảnh từ camera
            ret, frame = self.cap_right.read()
            if ret:
                # Chuyển đổi hình ảnh sang định dạng PIL
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                # Hiển thị hình ảnh trong Label
                self.label_camera_right.configure(image=image)
                self.label_camera_right.image = image
    def tranfer_DB(self):
        self.open_new_DB()
    def open_new_DB(self):
        self.new_window = Toplevel(self.root)
        self.app = db(self.new_window)
    def logout_function(self):
        self.root.destroy()

