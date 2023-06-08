#include <Servo.h>
#include <RFID.h>
#include <Thread.h>

#define SS_PIN1 53
#define RST_PIN1 5
#define SS_PIN2 48
#define RST_PIN2 6

unsigned char reading_card1[5]; // Mảng đọc mã card
unsigned char reading_card2[5]; // Mảng đọc mã card
// Biến
int  n_slot = 4;
int ledPins[] = {2, 3, 4, 5};
int cbPins[] = {9, 10, 11, 12};
int servoPinIn = 7;
int servoPinOut = 8;
int close = 80;
int open = 170;

// Phần cứng
RFID rfid1(SS_PIN1, RST_PIN1);
RFID rfid2(SS_PIN2, RST_PIN2);
Servo servo_in;
Servo servo_out;

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
  servo_in.attach(servoPinIn);
  servo_in.write(close);
  servo_out.attach(servoPinOut);
  servo_out.write(close);
  SPI.begin();
  rfid1.init();
  rfid2.init();
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

void Check(){
  // Kiểm tra thẻ
  if (rfid1.isCard()) {
    if (rfid1.readCardSerial()){
      // Kiểm tra thẻ xe
      for (int i = 0; i < sizeof(listRFID)/sizeof(listRFID[0]); i++) {
        // Tìm được thẻ
        if (memcmp(listRFID[i], rfid1.serNum, 5) == 0) {
          // Gửi tín hiệu chụp ảnh và nhận diện
          String message = "";
          for (int j = 0; j < sizeof(rfid1.serNum); j++) {
            message += String(rfid1.serNum[j], HEX); // Convert byte to hex string and concatenate
          }
          Serial.println("IN");
          delay(1000);
          Serial.println(message);
          // Serial.print("1");
          // // Nhận lại tín hiệu
          while(Serial.available() == 0){}
          char incomingByte = Serial.read();
          // kiểm tra tín hiệu
          if (incomingByte == '1'){
            servo_in.write(open);
            delay(3000);
            servo_in.write(close);
          }
          break;
        }
      }
    }
  }
  else if (rfid2.isCard()) {
    if (rfid2.readCardSerial()){
      // Kiểm tra thẻ xe
      for (int i = 0; i < sizeof(listRFID)/sizeof(listRFID[0]); i++) {
        // Tìm được thẻ
        if (memcmp(listRFID[i], rfid2.serNum, 5) == 0) {
          String message = "";
          for (int j = 0; j < sizeof(rfid2.serNum); j++) {
            message += String(rfid2.serNum[j], HEX); // Convert byte to hex string and concatenate
          }
          Serial.println("OUT");
          delay(1000);
          Serial.println(message);
          while(Serial.available() == 0){}
          char incomingByte = Serial.read();
          // kiểm tra tín hiệu
          if (incomingByte == '3'){
            servo_out.write(open);
            delay(3000);
            servo_out.write(close);
          }
          break;
        }
      }
    }
  }
  delay(1000);
}

void Open_Close(){
  if(Serial.available() != 0){
    char incomingByte = Serial.read();
    if (incomingByte == '5'){
      servo_out.write(open);
      delay(3000);
      servo_out.write(close);
    }
    if (incomingByte == '6'){
      servo_in.write(open);
      delay(3000);
      servo_in.write(close);
    }
  }
}

void setup() {
  SetUpGate();
  Serial.begin(9600);
}

void loop() {
  Check();
  Open_Close();
}
