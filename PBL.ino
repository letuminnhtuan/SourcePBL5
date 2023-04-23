#include <Servo.h>

// Biến
int  n_slot = 4;
int ledPins[] = {2, 3, 4, 5};
int cbPins[] = {8, 9, 10, 11};
Servo servo_start;
int servoPin = 13;
int cbPin = 12;
int out = 1;

//  Thiết lập cảm biến và led cho vị trí đỗ xe
void SetUpSlot(){
  for(int i = 0; i < 4; i++){
    pinMode(ledPins[i], OUTPUT);
    pinMode(cbPins[i], INPUT);
  }
}

// Thiết lập cảm biến, Servo cho cổng vào
void SetUpGate(){
  servo_start.attach(servoPin);
  pinMode(cbPin, INPUT);
  servo_start.write(90);
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

// Kiểm tra xe đi vào và chụp ảnh nếu có
void Check_In(){
  /* 
  - Khi xe vào, cảm biến đọc
  - Gửi tín hiệu qua python và nhận dạng biển số
  - Trả dữ liệu biển số về arduino và mở cửa
  + Vấn đề: Lặp quá nhiều dẫn đến quá tải
  */
  int check = digitalRead(cbPin);
  // Gửi tín hiệu chụp ảnh
  Serial.print(check);
  if(check == 0){
    if(out == 1){
      // Nhận tín hiệu
      String serialData = "";
      if (Serial.available() > 0) {  
        serialData = Serial.readStringUntil('\r');
        Serial.print(serialData);
      }
      // Khi nhận được biển số -> mở cổng
      if(serialData.length() > 0){
        servo_start.write(180);
        delay(3000);
        servo_start.write(90);
      }
      out = 0;
    }
    // Thoát
    check = digitalRead(cbPin);
    if(check == 0){
      out = 1;
    }
  }
}

void setup() {
  SetUpGate();
  Serial.begin(9600);
}

void loop() {
  Check_In();
}
