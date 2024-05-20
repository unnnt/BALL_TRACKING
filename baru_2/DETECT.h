void detect() {
  if (Serial.available() > 0) {
    String dataReceived = Serial.readStringUntil('\n');
    dataReceived.trim(); 
    int spaceIndex = 0;
    int prevSpaceIndex = 0;

    x = dataReceived.substring(prevSpaceIndex, spaceIndex = dataReceived.indexOf(' ', prevSpaceIndex)).toInt();
    prevSpaceIndex = spaceIndex + 1;

    y = dataReceived.substring(prevSpaceIndex, spaceIndex = dataReceived.indexOf(' ', prevSpaceIndex)).toInt();
    prevSpaceIndex = spaceIndex + 1;

    sisi = dataReceived.substring(prevSpaceIndex, spaceIndex = dataReceived.indexOf(' ', prevSpaceIndex)).toInt();
    prevSpaceIndex = spaceIndex + 1;

    persentase = dataReceived.substring(prevSpaceIndex, spaceIndex = dataReceived.indexOf(' ', prevSpaceIndex)).toFloat();
    prevSpaceIndex = spaceIndex + 1;

    jarak = dataReceived.substring(prevSpaceIndex).toFloat();
  }
}
