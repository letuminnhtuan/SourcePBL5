#include <Servo.h>
#include <RFID.h>

#define SS_PIN 53
#define RST_PIN 5
// Biến
int  n_slot = 4;
int ledPins[] = {2, 3, 4, 5};
int cbPins[] = {8, 9, 10, 11};
int servoPin = 7;

// Phần cứng
RFID rfid(SS_PIN, RST_PIN);
Servo servo_in;

byte listRFID[][5] = {
  {0xF7, 0xF5, 0xDD, 0xD7, 0x8},
  {0x45, 0x8E, 0xEB, 0x2A, 0xA}
};

//  Thiết lập cảm biến và led cho vị trí đỗ xe
void SetUpSlot(){
  for(int i = 0; i < 4; i++){
    pinMode(ledPins[i], OUTPUT);
    pinMode(cbPins[i], INPUT);
  }
}

// Thiết lập RFID, Servo cho cổng vào
void SetUpGate(){
  servo_in.attach(servoPin);
  servo_in.write(175);
  SPI.begin();
  rfid.init();
}

// Kiểm tra các vị trí trong bãi đỗ xe
void Check_Slot(){
  for(int i = 0; i < n_slot; i++){
    int giatri = digitalRead(cbPins[i]);
    if(giatri == 0){
      digitalWrite(ledPins[i], HIGH);
    }
    else{
      digitalWrite(ledPins[i], LOW);  
    }
  }
}

// Kiểm tra lúc xe đi vào
void Check_In(){
  // Kiểm tra thẻ
  if (rfid.isCard()) {
    if (rfid.readCardSerial()){
      // Kiểm tra thẻ xe
      for (int i = 0; i < sizeof(listRFID)/sizeof(listRFID[0]); i++) {
        // Tìm được thẻ
        if (memcmp(listRFID[i], rfid.serNum, 5) == 0) {
          // Gửi tín hiệu chụp ảnh và nhận diện
          Serial.print("1");
          // Nhận lại tín hiệu
          while(Serial.available() == 0){}
          char incomingByte = Serial.read();
          // kiểm tra tín hiệu
          if (incomingByte == '1'){
            servo_in.write(83);
            delay(3000);
            servo_in.write(175);
          }
          break;
        }
      }
    }
  }
  delay(1000);
}

void setup() {
  SetUpGate();
  Serial.begin(9600);
}

void loop() {
  Check_In();
}