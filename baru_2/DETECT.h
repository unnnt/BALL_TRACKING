void detect() {
  if (Serial.available() > 0) {
    String dataReceived = Serial.readStringUntil('\n');
    dataReceived.trim();  // Menghapus spasi yang tidak perlu di awal dan akhir string

    // Memisahkan data menjadi bagian-bagian yang sesuai
    x = dataReceived.substring(0, dataReceived.indexOf(' ')).toInt();
    y = dataReceived.substring(dataReceived.indexOf(' ') + 1, dataReceived.indexOf(' ', dataReceived.indexOf(' ') + 1)).toInt();    
    sisi = dataReceived.substring(dataReceived.indexOf(' ', dataReceived.indexOf(' ') + 1) + 1, dataReceived.lastIndexOf(' ')).toInt();  
    persentase = dataReceived.substring(dataReceived.lastIndexOf(' ', dataReceived.lastIndexOf(' ') - 1) + 1, dataReceived.lastIndexOf(' ')).toInt();
    jarak = dataReceived.substring(dataReceived.lastIndexOf(' ') + 1).toInt();
  }
}
