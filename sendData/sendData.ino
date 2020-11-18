#include <SoftwareSerial.h>

SoftwareSerial bt(10,11);  

void setup() {
  bt.begin(9600); //#HC-05 says this should be 38400, but 9600 works better, i dont know why
}
 
void loop() {
    sendToRaspberry("Paul");
    delay (2000); //prepare for data (2s)
}



void sendToRaspberry(String dataToBeSent)
{
  bt.print(dataToBeSent);
  bt.print("\n");
}

