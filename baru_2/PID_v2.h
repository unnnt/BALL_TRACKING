double Kp1 = 2;  // Konstanta Proporsional untuk input 1
double Ki1 = 0; // Konstanta Integral untuk input 1
double Kd1 = 0.1; // Konstanta Derivatif untuk input 1
double Kp2 = 1;  // Konstanta Proporsional untuk input 2
double Ki2 = 0.1; // Konstanta Integral untuk input 2
double Kd2 = 0.05; // Konstanta Derivatif untuk input 2

double error1 = 0;
double setpoint1 = 0;
double lastError1 = 0;
double integral1 = 0;
double derivative1 = 0;
double output1 = 0;

double error2 = 0;
double lastError2 = 0;
double integral2 = 0;
double derivative2 = 0;
double output2 = 0;

double calculatePID(double input, double setpoint, double Kp, double Ki, double Kd, double &lastError, double &integral, double &output) {
  double error = setpoint - input;
  integral += error;
  
  double derivative = error - lastError;
  
  output = Kp * error + Ki * integral + Kd * derivative;
  
  lastError = error;  
  return output;
}
