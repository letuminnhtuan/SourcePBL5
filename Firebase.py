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

    def get_cars(self):
        return self.fb.get('/LP_Car', '')

    def check_license_plate(self, license_plate):
        data = self.get_cars()
        if data is not None:
            for car in data:
                if car is not None and car['L_Plate'] == license_plate:
                    return True
        return False
    # Trả về thông tin với biển số tương ứng: tên người, cccd,
        # Lấy thông tin cột LP_Car và thông tin cột Car-management
        # Ktra xem ID_owner tương ứng với L_Plate trong cột LP_Car và lấy thông tin car trong cột Car-management với ID_owner tương ứng đó
    def get_car_info(self, license_plate):
        lp_data = self.fb.get('/LP_Car', '')
        lp_data = list(filter(None, lp_data))
        car_data = self.fb.get('/Car-management', '')
        car_data = list(filter(None, car_data))
        car_info = {}

        if lp_data is not None and car_data is not None:
            for lp_dict in lp_data:
                if lp_dict['L_Plate'] == license_plate:
                    if 'ID_owner' not in lp_dict:
                        print("Không có khóa ID_owner")
                    else:
                        id_owner = lp_dict['ID_owner']
                        for car_dict in car_data:
                            if str(car_dict.get('ID_owner')) == id_owner:
                                car_info = car_dict
                                car_info['L_Plate'] = license_plate
                                break
        return car_info
    def get(self):
        lp_data = self.fb.get('/LP_Car', '')
        return lp_data

    def add_license_plate(self, card, license_plate):
        # Kiểm tra xem giá trị của card có trùng với giá trị của khóa ID_card trong cột card_car hay không
        card_car = self.fb.get('/card_car', '')
        card_car = list(filter(None, card_car))
        id_card = None
        for item in card_car:
            if item['ID_card'] == card:
                id_card = item['Id']
                break

        if id_card is not None:
            # Cập nhật khóa L_Plate của bản ghi tương ứng với khóa ID_card trong cột card_car
            self.fb.patch('/card_car/' + id_card, {'L_Plate': license_plate})
            print('Thêm license plate thành công!')
        else:
            print('Không tìm thấy card trong cơ sở dữ liệu!')
    # def get1(self):
    #     a=self.fb.get('/card_car','')
    #     print(a)
    def check_card_license_plate(self, card, license_plate):
        # Kiểm tra xem giá trị của card và license_plate có trùng với giá trị của khóa ID_card và L_Plate trong cột card_car hay không
        card_car = self.fb.get('/card_car', '')
        card_car = list(filter(None, card_car))
        for item in card_car:
            if item['ID_card'] == card and item['L_Plate'] == license_plate:
                print('Mời bạn ra')
                return
        print('Mời bạn cút vào trong')