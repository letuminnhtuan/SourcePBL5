from tkinter import *
from Firebase import database
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import defaultdict
import customtkinter
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import ImageTk

class dt:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1299x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Quản lí doanh thu")
        # self.show()
        # font definition
        main_font = customtkinter.CTkFont(family="Helvetica", size=14)
        # Tạo frame chứa các thành phần trên màn hình trái
        self.left_frame = Frame(self.root, width=540, height=600, bg="white", bd=0, highlightthickness=5,
                                highlightbackground="orange")
        self.left_frame.place(x=40, y=0, width=400, height=600)
        self.Thongtin = customtkinter.CTkLabel(self.left_frame, text="Doanh Thu", font=("Helvetica", 30), height=40,
                                               width=320, text_color="#6699FF").place(x=45, y=10)
        btn_doanhthu = customtkinter.CTkButton(
            master=self.left_frame,
            command=self.show,
            text="Doanh thu từng năm",
            font=main_font,
            text_color="black",
            hover=True,
            hover_color="#ffb557",
            height=40,
            width=220,
            border_width=2,
            corner_radius=20,
            border_color="#bc863f",
            bg_color="white",
            fg_color="#eda850").place(x=100, y=100)
        btn_6month = customtkinter.CTkButton(
            master=self.left_frame,
            command=self.show_last_6_months,
            text="Doanh thu 6 tháng gần nhất",
            font=main_font,
            text_color="black",
            hover=True,
            hover_color="#FF99FF",
            height=40,
            width=160,
            border_width=2,
            corner_radius=20,
            border_color="#9e4a43",
            bg_color="white",
            fg_color="#FF66FF").place(x=100, y=200)
        btn_dudoan = customtkinter.CTkButton(
            master=self.left_frame,
            command=self.predict_revenue,
            text="Dự đoán doanh thu",
            font=main_font,
            text_color="black",
            hover=True,
            hover_color="#e06a61",
            height=40,
            width=220,
            border_width=2,
            corner_radius=20,
            border_color="#9e4a43",
            bg_color="white",
            fg_color="#c75d55").place(x=100, y=300)
        btn_user = customtkinter.CTkButton(
            master=self.left_frame,
            command=self.top_5,
            text="Bảng XH khách hàng",
            font=main_font,
            text_color="black",
            hover=True,
            hover_color="#CCFF66",
            height=40,
            width=220,
            border_width=2,
            corner_radius=20,
            border_color="#9e4a43",
            bg_color="white",
            fg_color="#99FF00").place(x=100, y=400)
        # Tạo frame chứa các thành phần trên màn hình phải
        self.right_frame = Frame(self.root, width=540,height=600, bg="gray", bd=0, highlightthickness=5,
                                 highlightbackground="orange")
        self.right_frame.place(x=480, y=0, width=800, height=600)
        self.bg = ImageTk.PhotoImage(file="Picture/logo.webp")
        self.bg_image = Label(self.right_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas = None  # Canvas for "show" button
        self.canvas1 = None  # Canvas for "show_last_6_months" button

    def show(self):
        # Clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        # Ket noi db
        db = database()
        car_manager_info = db.get_car_manager_info()
        total_money_by_month = self.get_total_money_by_month(car_manager_info)
        # plot
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        years = []
        data = []
        for year, monthly_data in total_money_by_month.items():
            years.append(year)
            monthly_total_money = [0] * 12
            for month, total_money in monthly_data.items():
                monthly_total_money[month - 1] = total_money
            data.append(monthly_total_money)
        for i in range(len(years)):
            ax.plot(range(1, 13), data[i], label=str(years[i]))
        ax.set_xlabel('Tháng', fontsize=10)
        ax.set_ylabel('Tổng tiền (VND)', fontsize=10)
        ax.set_title('Biểu đồ doanh thu theo tháng trong từng năm', fontsize=12)
        ax.legend()
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_last_6_months(self):
        # Clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        # Ket noi db
        db = database()
        car_manager_info = db.get_car_manager_info()

        # Get revenue data for the last 6 months
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        last_6_months = []
        for i in range(6):
            month_start = (today - timedelta(days=30 * i)).replace(day=1)
            last_6_months.append(month_start)

        total_money_by_month = defaultdict(int)
        for info in car_manager_info:
            time_regis = datetime.strptime(info[5], "%Y-%m-%d %H:%M:%S")
            if time_regis >= last_6_months[-1]:
                month = time_regis.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                if month in last_6_months:
                    total_money = float(info[7].split()[0])
                    total_money_by_month[month] += total_money

        # plot
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        months = []
        data = []
        for month in last_6_months:
            months.append(month.strftime("%m/%Y"))
            data.append(total_money_by_month[month])

        ax.pie(data, labels=months, autopct='%1.1f%%')
        ax.set_title('Biểu đồ doanh thu 6 tháng gần nhất', fontsize=12)

        canvas1 = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

    def predict_revenue(self):
        # Clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Prepare data
        db = database()
        car_manager_info = db.get_car_manager_info()
        total_money_by_month = self.get_total_money_by_month(car_manager_info)

        # Sort total_money_by_month by year and month
        sorted_data = sorted(total_money_by_month.items(), key=lambda x: (x[0], x[1]))

        # Prepare time series data
        time_series = np.array([total_money for year_data in sorted_data for total_money in year_data[1].values()])

        # Prepare training data
        window_size = 10
        data = []
        labels = []
        for i in range(len(time_series) - window_size):
            data.append(time_series[i:i + window_size])
            labels.append(time_series[i + window_size])
        data = np.array(data)
        labels = np.array(labels)

        # Build and train the model
        model = tf.keras.Sequential([
            tf.keras.layers.SimpleRNN(32, activation='relu', input_shape=(window_size, 1)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mae')
        history = model.fit(data, labels, epochs=20, batch_size=1)

        # Predict next month's revenue
        predicted_revenue = model.predict(np.array([time_series[-window_size:]]))

        # Plot the prediction
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(time_series, 'ro-', label='Doanh thu các tháng trước')
        ax.scatter(len(time_series), predicted_revenue, label='Doanh thu dự đoán tháng tiếp theo')
        ax.set_title('Đồ thị dự đoán doanh thu tháng tiếp theo', fontsize=12)
        ax.set_xlabel('Time')
        ax.set_ylabel('Doanh thu (nghìn đồng)')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    def top_5(self):
        # Clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Get data from Firebase
        db = database()
        car_manager_info = db.get_car_manager_info()

        # Calculate total money for each user
        user_money = defaultdict(int)
        for info in car_manager_info:
            user_id = info[2]
            total_money = float(info[7].split()[0])
            user_money[user_id] += total_money

        # Sort users by total money
        sorted_users = sorted(user_money.items(), key=lambda x: x[1], reverse=True)
        top_5_users = sorted_users[:5]

        # Create DataFrame for the top 5 users
        user_ids = [user[0] for user in top_5_users]
        total_moneys = [user[1] for user in top_5_users]
        data = {'Name': user_ids, 'Total Money': total_moneys}
        df = pd.DataFrame(data)

        # Plot bar chart
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.bar(df['Name'], df['Total Money'])
        ax.set_xlabel('Name')
        ax.set_ylabel('Total Money (VND)')
        ax.set_title('Top 5 khách hàng có tổng tiền nhiều nhất', fontsize=12)
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def get_total_money_by_month(self, car_manager_info):
        total_money_by_month = defaultdict(lambda: defaultdict(int))
        for info in car_manager_info:
            time_regis = datetime.strptime(info[5], "%Y-%m-%d %H:%M:%S")
            year = time_regis.year
            month = time_regis.month
            total_money = float(info[7].split()[0])
            total_money_by_month[year][month] += total_money
        return total_money_by_month