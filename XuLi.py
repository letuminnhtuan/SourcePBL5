import DetectPlate.function.helper as helper
import DetectPlate.function.utils_rotate as utils_rotate
import cv2
import torch
import serial
import time

def detect(img):
    yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='E:\PBL5\License-Plate-Recognition\model\LP_detector.pt', force_reload=True, source='local')

    plates = yolo_LP_detect(img, size=640)
    list_plates = plates.pandas().xyxy[0].values.tolist()

    return list_plates

def plate(img):
    yolo_license_plate = torch.hub.load('yolov5', 'custom', path='E:\PBL5\License-Plate-Recognition\model\LP_ocr.pt', force_reload=True, source='local')
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
                    cv2.putText(img, lp, (int(plate[0]), int(plate[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        flag = 1
                        break
                if flag == 1:
                    break
    return list_read_plates

def SendData(data):
    arData.write(data.encode('utf-8'))
    

if __name__ == '__main__':
    arData = serial.Serial('COM4', 9600)

    cap = cv2.VideoCapture(0)

    while True:
        _, image = cap.read()
        cv2.imshow('show', image)
        
        if arData.in_waiting == 0 or arData.read() == '0xff':
            continue
        data = str(arData.read(), 'utf')
        if(data == '0'):
            l = plate(image)
            print(l)
            if len(l) > 0:
                num_plate = list(l)
                SendData(num_plate[0])
            time.sleep(.1)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break