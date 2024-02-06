
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (mySerial.available() > 0) { // Jika ada data tersedia di port serial
    int receivedChar = mySerial.parseInt(); // Baca karakter yang diterima
    Serial.print("Received: ");
    Serial.println(receivedChar); // Tampilkan karakter yang diterima
  }
}
