#include <IRremote.h>
IRsend irsend;
void setup() {
  Serial.begin(9600);  // start serial communication at 9600 baud
}

void loop() {
   // Read and execute commands from serial port
   if (Serial.available()) {  // check for incoming serial data
      String command = Serial.readString();  // read command from serial port
      if (command == "KEY_Power") {  // signal power button
         irsend.sendRC5(0xFCE1D0DA , 20);
      } else if (command == "KEY_FanUp") {  // signal fan speed up
         irsend.sendRC5(0x2FEDEE79 , 20);
      } else if (command == "KEY_FanDown") {  // signal fan speed down
         irsend.sendRC5(0xC1D0851 , 20);
      } else if (command == "KEY_TempUp") {  // signal temperature setting higher
         irsend.sendRC5(0xBA604E74 , 20);
      } else if (command == "KEY_TempDown") {  // signal temperature setting lower
         irsend.sendRC5(0xEEF84FE7 , 20);
      } else if (command == "KEY_Cool_Mode") {  // signal set dyson into cooler mode ( produces cold air no set temperature )
         irsend.sendRC5(0xFEE02B6D , 20);
      } else if (command == "KEY_Night_Mode") {  // signal set dyson into night mode ( runs quiter comapared to normal )
         irsend.sendRC5(0x4AB7527C, 20);
      }
   }
}
