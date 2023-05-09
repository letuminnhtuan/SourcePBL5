from firebase import firebase
class database:
    def __init__(self):
        # Firebase
            self.fb = firebase.FirebaseApplication('https://pbl5-7a693-default-rtdb.firebaseio.com', None)
    # Hàm check login
    def check_login(self, username, password):
        result = self.fb.get('Login', None)
        found = False
        user_role = None
        for key in result.keys():
            if result[key]['username'] == username and result[key]['password'] == password:
                found = True
                user_role = result[key]['role']
                break
        return found, user_role
    # Hàm lấy thông tin xe đăng kí
    def get_car_manager_info(self):
        data = self.fb.get('Car-management', None)
        car_manager_info = []
        if data is not None:
            for item in data:
                if item is not None:
                    id = item.get('Id', '')
                    name = item.get('Owner-name', '')
                    email = item.get('Phone', '')
                    phone = item.get('CCCD', '')
                    time_regis = item.get('Time-register')
                    period_time = item.get('Period-time')
                    total_money = item.get('Total-money')
                    car_manager_info.append((id, name, email, phone, time_regis, period_time, total_money))
        return car_manager_info
    # Hàm lấy thông tin xe đăng kí
    # def get_car_manager_info(self):
    #     data = self.fb.get('/Car-management', '')
    #     car_manager_info = []
    #     if data is not None:
    #         for item in data:
    #             if item is not None:
    #                 id = item.get('Id', '')
    #                 name = item.get('Owner-name', '')
    #                 email = item.get('Phone', '')
    #                 phone = item.get('CCCD', '')
    #                 time_regis = item.get('Time-register')
    #                 period_time = item.get('Period-time')
    #                 total_money = item.get('Total-money')
    #                 car_manager_info.append((id, name, email, phone, time_regis, period_time, total_money))
    #     return car_manager_info

    # Hàm lắng nghe sự kiện thay đổi trên Firebase Realtime Database
    # def get_car_manager_info_realtime(self, callback):
    #     def on_change(event):
    #         callback(event)
    #     self.fb.stream('/Car-management', callback=on_change)
    def add_car_data(self, id, owner_name, phone, cccd, time_register, period_time, total_money):
        car_data = {
            "Id": id,
            "Owner-name": owner_name,
            "Phone": phone,
            "CCCD": cccd,
            "Time-register": time_register,
            "Period-time": period_time,
            "Total-money": total_money
        }
        self.fb.post('/Car-management', car_data)
    




