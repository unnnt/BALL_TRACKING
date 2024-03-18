void detect() {
  if (Serial.available() > 0) {
    String dataReceived = Serial.readStringUntil('\n');
    dataReceived.remove(0, 1);  
    dataReceived.remove(dataReceived.length() - 1, 1);
    // Pecah data menjadi nilai_sensor_x dan nilai_sensor_y
    x = dataReceived.substring(0, dataReceived.indexOf(' ')).toInt();
    y = dataReceived.substring(dataReceived.indexOf(' ') + 1).toInt();

    Serial.print("Data Pertama: ");
    Serial.println(x);
    Serial.print("Data Kedua: ");
    Serial.println(y);
  }
}
