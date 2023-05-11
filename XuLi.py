import DetectPlate.function.helper as helper
import DetectPlate.function.utils_rotate as utils_rotate
import cv2
import torch
import serial
import time
import threading

arData = serial.Serial('COM4', 9600)

def detect(img):
    yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='E:\\PBL5\\SourceCodePBl5\\DetectPlate\\model\\LP_detector.pt', force_reload=True, source='local')
    plates = yolo_LP_detect(img, size=640)
    list_plates = plates.pandas().xyxy[0].values.tolist()
    
    return list_plates

def plate(img):
    yolo_license_plate = torch.hub.load('yolov5', 'custom', path='E:\\PBL5\\SourceCodePBl5\\DetectPlate\\model\\best.pt', force_reload=True, source='local')
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

# Define a function to receive and send data
# def data_handler(arData, cap):
#     while True:
#         if arData.in_waiting == 0:
#             continue
#         else:
#             data = str(arData.read(), 'utf')
#             if data == '1':
#                 _, img = cap.read()
#                 print(plate(img))
#                 SendData('1')

#             time.sleep(1)

# Define a function to display camera images
# def display_camera(cap):
#     while True:
#         _, image = cap.read()
#         cv2.imshow('show', image)
#         if cv2.waitKey(1) == ord('q'):
#             cv2.destroyAllWindows()
#             break

# Create a VideoCapture object to capture video from the default camera
# cap = cv2.VideoCapture(0)

# # Start the data handling thread
# data_thread = threading.Thread(target=data_handler, args=(arData, cap,))
# data_thread.start()

# # Start the camera display thread
# camera_thread = threading.Thread(target=display_camera, args=(cap,))
# camera_thread.start()

# # Wait for the threads to finish
# data_thread.join()
# camera_thread.join()

# # Release the VideoCapture object and close all windows
# cap.release()
# cv2.destroyAllWindows()