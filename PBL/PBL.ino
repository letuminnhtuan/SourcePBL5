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
  servo_in.write(0);
  servo_out.attach(servoPinOut);
  servo_out.write(0);
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
            // digitalWrite(8, HIGH);
            // delay(1000);
            // digitalWrite(8, LOW);
            servo_in.write(90);
            delay(3000);
            servo_in.write(0);
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
          // Gửi tín hiệu chụp ảnh và nhận diện
          // Serial.print("2");
          // Nhận lại tín hiệu
          while(Serial.available() == 0){}
          char incomingByte = Serial.read();
          // kiểm tra tín hiệu
          if (incomingByte == '3'){
            // digitalWrite(9, HIGH);
            // delay(1000);
            // digitalWrite(9, LOW);
            servo_out.write(90);
            delay(3000);
            servo_out.write(0);
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
  Check();
}



// -----------------------------
/*
* MOSI: Pin 51 / ICSP-4
* MISO: Pin 50 / ICSP-1
* SCK: Pin 52 / ISCP-3
* SS: Pin 53
* RST: Pin 5
*/
 
// #include <Thread.h>
// #include <SPI.h>
// #include <RFID.h>
 
// #define SS_PIN1 53
// #define RST_PIN1 5
// #define SS_PIN2 48
// #define RST_PIN2 6
// RFID rfid1(SS_PIN1, RST_PIN1);
// unsigned char reading_card1[5]; // Mảng đọc mã card
// RFID rfid2(SS_PIN2, RST_PIN2);
// unsigned char reading_card2[5]; // Mảng đọc mã card

// void check1(){
//   if (rfid1.isCard()) {
//     if (rfid1.readCardSerial()) // Nếu có thẻ
//     {
//       digitalWrite(8, HIGH);
//       delay(1000);
//       digitalWrite(8, LOW);
//       // Serial.println("1");
//       // for (int i = 0; i < 5; i++) {
//       //     reading_card1[i] = rfid1.serNum[i]; //Lưu mã thẻ đọc được vào mảng reading_card
//       //     Serial.println(reading_card1[i], HEX);
//       // }
//       // Serial.println();
//     }
//     rfid1.halt();
//   }
//   delay(100);
// }

// void check2(){
//   if (rfid2.isCard()) {
//     if (rfid2.readCardSerial()) // Nếu có thẻ
//     {
//       digitalWrite(9, HIGH);
//       delay(1000);
//       digitalWrite(9, LOW);
//       // Serial.println("2");
//       // for (int i = 0; i < 5; i++) {
//       //     reading_card2[i] = rfid2.serNum[i]; //Lưu mã thẻ đọc được vào mảng reading_card
//       //     Serial.println(reading_card2[i], HEX);
//       // }
//       // Serial.println();
//     }
//     rfid2.halt();
//   }
//   delay(100);
// }

// void setup()
// {
//   Serial.begin(9600);
//   SPI.begin();
//   rfid1.init();
//   rfid2.init();
//   pinMode(8, OUTPUT);
//   pinMode(9, OUTPUT);

//   // thread1.onRun(check1);
//   // thread1.run();
//   // thread2.onRun(check2);
//   // thread2.run();
// }

// void loop()
// {
//   check1();
//   check2();
//   // thread1.onRun(check1);
//   // thread1.run();
//   // thread2.onRun(check2);
//   // thread2.run();
// }


// #include <Thread.h>
// #include <ThreadController.h>

// ThreadController controller;
// Thread thread1 = Thread();
// Thread thread2 = Thread();

// // Shared resources
// int shared_variable1 = 0;
// int shared_variable2 = 0;

// // Mutexes for synchronization
// Mutex mutex1;
// Mutex mutex2;

// void setup() {
//   Serial.begin(9600);

//   // Start the threads
//   thread1.onRun(runThread1);
//   controller.add(&thread1);

//   thread2.onRun(runThread2);
//   controller.add(&thread2);
// }

// void loop() {
//   // Run the thread controller
//   controller.run();
// }

// void runThread1() {
//   while(true) {
//     // Acquire mutex1 before accessing shared_variable1
//     mutex1.lock();
//     // Read shared_variable1
//     int data = shared_variable1;
//     // Release mutex1
//     mutex1.unlock();

//     // Do some processing with data
//     data++;

//     // Acquire mutex2 before accessing shared_variable2
//     mutex2.lock();
//     // Write data to shared_variable2
//     shared_variable2 = data;
//     // Release mutex2
//     mutex2.unlock();

//     // Wait for some time before running again
//     delay(1000);
//   }
// }

// void runThread2() {
//   while(true) {
//     // Acquire mutex2 before accessing shared_variable2
//     mutex2.lock();
//     // Read shared_variable2
//     int data = shared_variable2;
//     // Release mutex2
//     mutex2.unlock();

//     // Do some processing with data
//     data--;

//     // Acquire mutex1 before accessing shared_variable1
//     mutex1.lock();
//     // Write data to shared_variable1
//     shared_variable1 = data;
//     // Release mutex1
//     mutex1.unlock();

//     // Wait for some time before running again
//     delay(1000);
//   }
// }

// Kiểm tra lúc xe đi vào
// void Check_In(){
//   // Kiểm tra thẻ
//   if (rfid1.isCard()) {
//     if (rfid1.readCardSerial()){
//       // Kiểm tra thẻ xe
//       for (int i = 0; i < sizeof(listRFID)/sizeof(listRFID[0]); i++) {
//         // Tìm được thẻ
//         if (memcmp(listRFID[i], rfid1.serNum, 5) == 0) {
//           // Gửi tín hiệu chụp ảnh và nhận diện
//           String message = "";
//           for (int j = 0; j < sizeof(rfid1.serNum); j++) {
//             message += String(rfid1.serNum[j], HEX); // Convert byte to hex string and concatenate
//           }
//           Serial.println("IN");
//           delay(1000);
//           Serial.println(message);
//           // Serial.print("1");
//           // // Nhận lại tín hiệu
//           while(Serial.available() == 0){}
//           char incomingByte = Serial.read();
//           // kiểm tra tín hiệu
//           if (incomingByte == '1'){
//             digitalWrite(8, HIGH);
//             delay(1000);
//             digitalWrite(8, LOW);
//             // servo_in.write(83);
//             // delay(3000);
//             // servo_in.write(175);
//           }
//           break;
//         }
//       }
//     }
//   }
//   delay(1000);
// }

// Kiểm tra lúc xe đi ra
// void Check_Out(){
//   // Kiểm tra thẻ
//   if (rfid2.isCard()) {
//     if (rfid2.readCardSerial()){
//       // Kiểm tra thẻ xe
//       for (int i = 0; i < sizeof(listRFID)/sizeof(listRFID[0]); i++) {
//         // Tìm được thẻ
//         if (memcmp(listRFID[i], rfid2.serNum, 5) == 0) {
//           String message = "";
//           for (int j = 0; j < sizeof(rfid2.serNum); j++) {
//             message += String(rfid2.serNum[j], HEX); // Convert byte to hex string and concatenate
//           }
//           Serial.println("OUT");
//           delay(1000);
//           Serial.println(message);
//           // Gửi tín hiệu chụp ảnh và nhận diện
//           // Serial.print("2");
//           // Nhận lại tín hiệu
//           while(Serial.available() == 0){}
//           char incomingByte = Serial.read();
//           // kiểm tra tín hiệu
//           if (incomingByte == '3'){
//             digitalWrite(9, HIGH);
//             delay(1000);
//             digitalWrite(9, LOW);
//             // servo_in.write(83);
//             // delay(3000);
//             // servo_in.write(175);
//           }
//           break;
//         }
//       }
//     }
//   }
//   delay(1000);
// }