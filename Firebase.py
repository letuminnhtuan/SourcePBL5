from firebase import firebase
from datetime import datetime
import string
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
        data = list(filter(None, data))
        data1 = self.fb.get('Customer',None)
        data1 = list(filter(None, data1))
        car_manager_info = []
        if data is not None and data1 is not None:
            for item in data:
                if item is not None:
                    # Lấy các giá trị cần thiết từ mục hiện tại
                    id = item.get('ID', '')
                    id_owner = item.get('ID_owner', '')
                    time_regis = item.get('Time-register')
                    period_time = item.get('Period-time')
                    total_money = item.get('Total-money')

                    # Tìm thông tin khách hàng từ cột "Customer" với ID_owner tương ứng
                    customer_data = next((customer for customer in data1 if customer.get('ID_owner') == id_owner), {})
                    name = customer_data.get('Name', '')
                    phone = customer_data.get('Phone', '')
                    cccd = customer_data.get('CCCD', '')

                    # Thêm thông tin vào danh sách car_manager_info
                    car_manager_info.append((id, id_owner, name, phone, cccd, time_regis, period_time, total_money))
        return car_manager_info

    def get_car_manager_info1(self):
        data = self.fb.get('Car-management', None)
        car_manager_info = []
        lp_car_data = self.fb.get('LP_Car', None)  # Lấy dữ liệu từ cột LP_Car
        if data is not None and lp_car_data is not None:
            for item in data:
                if item is not None:
                    id = item.get('Id', '')
                    id_owner = item.get('ID_owner', '')
                    name = item.get('Owner-name', '')
                    email = item.get('Phone', '')
                    phone = item.get('CCCD', '')
                    time_regis = item.get('Time-register')
                    period_time = item.get('Period-time').replace('h','')
                    total_money = item.get('Total-money').replace('VND', '')
                    lp_plate = ''  # Khởi tạo giá trị ban đầu cho lp_plate
                    for lp_item in lp_car_data:
                        if lp_item is not None and lp_item.get('ID_owner') == id_owner:
                            lp_plate = lp_item.get('L_Plate', '')  # Lấy giá trị "L_Plate" từ lp_item
                            break
                    car_manager_info.append((id, id_owner, name, email, phone, time_regis, period_time, total_money,
                                             lp_plate))  # Thêm lp_plate vào tuple

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
        return self.fb.get('/L_Plate', '')
    def get_price_list(self):
        return self.fb.get('/Price_List','')
    def get_account(self):
        return self.fb.get('/Login','')
    def get_account_name(self):
        return self.fb.get('/Login/')
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
        lp_data = self.fb.get('/L_Plate', '')
        lp_data = list(filter(None, lp_data))
        car_data = self.fb.get('/Customer', '')
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
            self.fb.patch('/card_car/' + str(id_card), {'L_Plate': license_plate})
            print('Thêm license plate thành công!')
        else:
            print('Không tìm thấy card trong cơ sở dữ liệu!')

    def check_card_license_plate(self, card, license_plate):
        # Kiểm tra xem giá trị của card và license_plate có trùng với giá trị của khóa ID_card và L_Plate trong cột card_car hay không
        card_car = self.fb.get('/card_car', '')
        card_car = list(filter(None, card_car))
        time_out = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in card_car:
            if item['ID_card'] == card and item['L_Plate'] == license_plate:
                time_in = self.get_car_info1(license_plate)[0]
                period = self.get_car_info1(license_plate)[1]
                print(period)
                period = float(period.replace('h',''))
                time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
                time_out = datetime.strptime(time_out, "%Y-%m-%d %H:%M:%S")
                time = time_out - time_in
                # print("Vào lúc : ",time_in)
                # print("Thời gian thuê từ trước : ", period , "h")
                hour = time.total_seconds() / 3600
                check = hour - period
                fee = check * 3000
                if check == 0 : # Lấy sớm
                    return str('Mời bạn ra'), check
                elif check < 0:
                    check = -check;
                    return str(f'Mời bạn ra và bạn còn {check}h'), -check
                else : # Lấy muộn
                    return str('Mời bạn ra!\n Bạn bị quá giờ nên đóng thêm ' + str(fee) + " VND tiền phí"), check
        return str('Không hợp lệ!!'), None

    def get_car_info1(self, L_Plate):
        lp_car = self.fb.get('/L_Plate', '')
        lp_car = list(filter(None, lp_car))
        for lp in lp_car:
            if  lp['L_Plate'] == L_Plate:
                id_owner = lp['ID_owner']
                # Nếu tìm thấy khớp trong bảng LP_Car thì lấy giá trị time_register và period_time trong bảng Car-management tương ứng với ID_owner đó
                car_mgmt = self.fb.get('/Car-management', '')
                car_mgmt = list(filter(None, car_mgmt))
                for car in reversed(car_mgmt):
                    if car['ID_owner'] == id_owner:
                        return car['Time-register'], car['Period-time']
    def save_account(self,acc_number,tk,mk,role):
        login = 'Login'
        self.fb.put(login, f"acc-{acc_number}", {'username': tk, 'password': mk, 'role': role})

    def set_Plate(self,car_card):
            data = self.fb.get('/card_car','')
            data = list(filter(None, data))
            id = None
            for item in data:
                if item['ID_card'] == car_card:
                    id = item['Id']
                    break
            if id is not None:
                self.fb.put('/card_car', id, {'ID_card': car_card, 'Id': id, 'L_Plate': ""})

    def get_Plate(self,car_card):
        data = self.fb.get('/card_car','')
        data = list(filter(None, data))
        lp = ""
        for item in data:
            if item['ID_card'] == car_card:
                lp = item['L_Plate']
                break
        return lp