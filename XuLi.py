import DetectPlate.function.helper as helper
import DetectPlate.function.utils_rotate as utils_rotate
import cv2
import torch
import serial
import serial.tools.list_ports
import pandas as pd
from ultralytics import YOLO

def detect_com_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'USB' in port.description:  # Customize this condition based on your device
            return port.device
    return None

com = detect_com_port()
arData = serial.Serial(com, 9600)

# yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='./DetectPlate/model/LP_detector.pt', force_reload=True, source='local')
# yolo_license_plate = torch.hub.load('yolov5', 'custom', path='./DetectPlate/model/best.pt', force_reload=True, source='local')
yolo_LP_detect = YOLO("./DetectPLate/model/bienso.pt")
yolo_license_plate = YOLO("./DetectPLate/model/kitu.pt")
# def detect(img):
#     plates = yolo_LP_detect(img, size=640)
#     list_plates = plates.pandas().xyxy[0].values.tolist()
    
#     return list_plates

# def plate(img):
#     yolo_license_plate.conf = 0.60
#     list_plates = detect(img)
#     list_read_plates = set()
#     if(len(list_plates) == 0):
#         return list_read_plates
#     else:
#         for plate in list_plates:
#             # bounding box
#             cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)

#             # read plate number
#             flag = 0
#             x = int(plate[0]) # xmin
#             y = int(plate[1]) # ymin
#             w = int(plate[2] - plate[0]) # xmax - xmin
#             h = int(plate[3] - plate[1]) # ymax - ymin  
#             crop_img = img[y:y+h, x:x+w]
#             lp = ""
#             for cc in range(0,2):
#                 for ct in range(0,2):
#                     lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
#                     cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
#                     if lp != "unknown":
#                         list_read_plates.add(lp)
#                         flag = 1
#                         break
#                 if flag == 1:
#                     break
#     return list_read_plates

def convert(result):
    boxes = result[0].boxes

    xyxy = pd.DataFrame(boxes.xyxy.cpu().numpy(), columns=['xmin', 'ymin', 'xmax', 'ymax'])
    conf = pd.DataFrame(boxes.conf.cpu().numpy(), columns=['confidence'])
    cls = pd.DataFrame(boxes.cls.cpu().numpy(), columns=['class'])

    result = pd.concat([xyxy, conf, cls], axis=1)

    names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
            'U', 'V', 'W', 'X', 'Y', 'Z']
    label_map = {i: name for i, name in enumerate(names)}
    result['name'] = result['class'].map(label_map)

    return result.values.tolist()

def detect(img):
    plates = yolo_LP_detect(img, device = 0)
    list_plates = convert(plates)
    print(len(list_plates))
    return list_plates

def plate(img):
    yolo_license_plate.conf = 0.60
    
    list_plates = detect(img)
    list_read_plates = set()
    if(len(list_plates) == 0):
        return list_read_plates
    else:
        for plate in list_plates:
            # bounding box
            cv2.rectangle(img, (int(plate[0]),int(plate[1])), (int(plate[2]),int(plate[3])), color = (0,0,225), thickness = 2)

            # read plate number
            flag = 0
            x = int(plate[0]) # xmin
            y = int(plate[1]) # ymin
            w = int(plate[2] - plate[0]) # xmax - xmin
            h = int(plate[3] - plate[1]) # ymax - ymin  
            crop_img = img[y:y+h, x:x+w]
            lp = ""
            for cc in range(0,2):
                for ct in range(0,2):
                    lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                    cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_TRIPLEX, 2.5, (0, 255, 0), 2)
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        flag = 1
                        break
                if flag == 1:
                    break
    return list_read_plates

def SendData(data):
    arData.write(data.encode('utf-8'))