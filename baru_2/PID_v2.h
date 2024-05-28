double Kp1 = 2;  // Konstanta Proporsional untuk input 1 (x)
double Ki1 = 0; // Konstanta Integral untuk input 1
double Kd1 = 0.1; // Konstanta Derivatif untuk input 1
double Kp2 = 1;  // Konstanta Proporsional untuk input 2 (y)
double Ki2 = 0.1; // Konstanta Integral untuk input 2
double Kd2 = 0.05; // Konstanta Derivatif untuk input 2
double Kp3 = 2; // Konstanta Proporsional untuk input 3 (yaw)
double Ki3 = 0; // Konstanta Integral untuk input 3
double Kd3 = 0.1; // Konstanta Derivatif untuk input 3

double error1 = 0;
double setpoint1 = 0; // Set point untuk koordinat x
double lastError1 = 0;
double integral1 = 0;
double derivative1 = 0;
double output1 = 0;

double error2 = 0;
double setpoint2 = 0; // Set point untuk koordinat y
double lastError2 = 0;
double integral2 = 0;
double derivative2 = 0;
double output2 = 0;

double error3 = 0;
double setpoint3 = 0; // Set point untuk sudut yaw
double lastError3 = 0;
double integral3 = 0;
double derivative3 = 0;
double output3 = 0;

double calculatePID(double input, double setpoint, double Kp, double Ki, double Kd, double &lastError, double &integral, double &output) {
  double error = setpoint - input;
  integral += error;

  double derivative = error - lastError;

  output = Kp * error + Ki * integral + Kd * derivative;

  lastError = error;
  return output;
}

void gerak(unsigned char mode, int nilai_pid) {
  if (mode == PUTAR) {
    minpwm = 100;
    maxpwm = 255;
    putar_pwm = constrain(nilai_pid, minpwm, maxpwm);
    Serial.print("pwm="); Serial.println(putar_pwm);
    if (int(yaw) > 5) {
      jalan(rot_kiri, putar_pwm);
    }
    else if (int(yaw) < -5) {
      jalan(rot_kanan, putar_pwm);
    }
    else {
      jalan(stopp, 70);
    }
  }
  else if (mode == FOLLOW_BOLA) {
    detect();
    if (jarak < 30 ) {
      minpwm = 120;
      maxpwm = 170;
    }
    else{
      minpwm = 120;
      maxpwm = 255;
    }
    putar_pwm = constrain(nilai_pid, minpwm, maxpwm);
    Serial.print("pwm="); Serial.println(putar_pwm);

    if (int(x) <= 50 && int(x) >= -50) {
      jalan(maju, putar_pwm);
    }
    else if (int(x) > 50) {
      jalan(go_kanan, putar_pwm);
    }
    else if (int(x) < -50) {
      jalan(go_kiri, putar_pwm);
    }
    else if (jarak <= 15) {
      jalan(stopp, 70);
    }
  }
}
