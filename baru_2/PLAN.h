void ke_bola() {
  switch (index) {
    case 0:
      while (1) {
        yaw = getYaw();
        detect();
        if (int(yaw) < -5 || int(yaw) > 5 ) {
          output3 = calculatePID(yaw, setpoint3, Kp3, Ki3, Kd3, lastError3, integral3, output3);
          gerak(PUTAR, output3);
        }
        if (int(x) < -50 || int(x) > 50) {
        output2 = calculatePID(yaw, setpoint2, Kp2, Ki2, Kd2, lastError2, integral2, output2);
          gerak(FOLLOW_BOLA, output2);
        }
      }
  }
}
