from tkinter import *

import cv2
from firebase import firebase
from PIL import Image
from PIL import ImageTk
from Firebase import fb
class Check_car_in: # Quản lí xe vào
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Quản lí xe vào")
        # Form Dashboard
        Frame_dashboard = Frame(self.root, bg="white", relief="groove", bd=1, highlightthickness=1,
                                highlightbackground="green")
        Frame_dashboard.place(x=0, y=0, width=1199, height=600)

        # Form left (display camera)
        Frame_left = Frame(Frame_dashboard, bg="white", bd=0, highlightthickness=1, highlightbackground="green")
        Frame_left.place(x=0, y=0, width=599, height=600)

        # Tạo đối tượng VideoCapture
        self.cap0 = cv2.VideoCapture(0)

        # Tạo một Label widget để hiển thị camera lên Frame_left
        self.label = Label(Frame_left)
        self.label.pack()
        self.update_image()   # Gọi hàm update_image() để cập nhật hình ảnh từ camera và hiển thị lên Label widget

        # Form right (car information)
        Frame_right = Frame(Frame_dashboard, bg="white", bd=0, highlightthickness=1, highlightbackground="green")
        Frame_right.place(x=600, y=0, width=599, height=600)
        Label(Frame_right, text="THÔNG TIN", font=("Goudy old style", 30, "bold"), fg="grey", bg="white").place(x=150,
                                                                                                                y=30)
        back = Button(Frame_right, text="Back", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white",
                        command=self.logout_function)
        back.place(x=480, y=30, width=100, height=40)

        Label(Frame_right, text="Id ", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30,
                                                                                                      y=130)
        self.id = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.id.place(x=150, y=130, width=320, height=35)

        Label(Frame_right, text="Time in", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30,
                                                                                                             y=230)
        self.timein = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.timein.place(x=150, y=230, width=320, height=35)

        Label(Frame_right, text="Biển số", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=30, y=330)

        self.bienso = Entry(Frame_right, font=("Goudy old style", 15), bg="#E7E6E6",state="normal")
        self.bienso.place(x=150, y=330, width=320, height=35)

        # Firebase
        self.firebase = fb()
        # Get data
        data = self.firebase.fb.get('/timein/3', None)
        print(data)

        # Display data in the Entry widgets
        self.id.delete(0, END)
        self.id.insert(0, str(data['id']))
        self.id.configure(state="readonly")

        self.timein.delete(0, END)
        self.timein.insert(0, str(data['timein']))
        self.timein.configure(state="readonly")

        self.bienso.delete(0, END)
        self.bienso.insert(0, str(data['license_plate']))
        self.bienso.configure(state="readonly")

    def update_image(self):
        # Đọc khung hình mới nhất từ camera và chuyển đổi sang định dạng RGB để có thể hiển thị lên label widget
        ret0, frame0 = self.cap0.read()
        frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame0)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(10, self.update_image) # Sau mỗi 10ms cập nhật hình ảnh mới từ camera

    def logout_function(self):
        self.root.destroy()