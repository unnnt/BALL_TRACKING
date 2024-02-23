#define INTEGRAL 1
#define NORMAL 2

class PID {
    /*
      sv = set value
      pv = preset value
      e  = error
      Kp = Gain Proportional
      Ki = Gain Integral
      Kd = Gain  Derivative
      Tc = Time Sampling (ms)
      mode = dU intergal / normal
    */
    float sv = 0, pv = 0, error, integralE, derivativeE, Kp = 0, Ki = 0, Kd = 0, dU = 0;
    int syntaxError = 0;
    unsigned long previousMillis = 0;
    float outP, outI, outD;
    float maxOut = 0;
    float minOut = 0;
    long lastTimeTC;
    float outPID, Tc;
    int mode;
    int first = 1;
  public:
    void param(float  Kp, float  Ki, float  Kd, int mode);
    void setPoint(float sv);
    void constraint(float minOut, float maxOut);
    void readSensor(float pv);
    void timeSampling(int Tc);
    int showPID() {
      return outPID;
    }
    void showParam() {
      DEBUG_PRINT(" Kp:"); DEBUG_PRINT(Kp);
      DEBUG_PRINT(" Ki:"); DEBUG_PRINT(Ki);
      DEBUG_PRINT(" Kd:"); DEBUG_PRINT(Kd);
      DEBUG_PRINT(" Tc:"); DEBUG_PRINT(Tc);
      //      DEBUG_PRINT("ms mode:");
      //      if (mode == 1) {
      //        DEBUG_PRINT("INTEGRAL");
      //      } else {
      //        DEBUG_PRINT("NORMAL");
      //      }
    }
    void showUnitPID() {
      DEBUG_PRINT(outP); DEBUG_PRINT("\t");
      DEBUG_PRINT(outI); DEBUG_PRINT("\t");
      DEBUG_PRINT(outD); DEBUG_PRINT("\t");
    }
    //pid calculation
    int calc() {
      //catch error
      if (syntaxError == 1)while (1);

      //error calculation
      error = sv - pv;

      //Derivative protection spike value
      if (first == 1) {
        first = 0;
        derivativeE = error;
      }
      //time sampling detection
      unsigned long Time = micros();
      if (Time - lastTimeTC >= (Tc * 1000)) {
        float tc =  (Time - lastTimeTC) / 1000000.0;
        lastTimeTC = Time;

        //Proportional calculation
        outP = Kp * error;

        //Integral calculation
        integralE += error;
        outI = Ki * integralE * tc;

        //Derivative calculation
        derivativeE = error - derivativeE;
        outD = (Kd * derivativeE) / tc;
        derivativeE = error;

        //delta U output
        dU = outP + outI + outD;
        //    DEBUG_PRINT("MOVEVAL = "); DEBUG_PRINTLN(dU);
        //case mode
        if (mode == 1) {
          outPID += dU;
        } else {
          outPID = dU;
        }

        //limit output value
        if (maxOut != 0 || minOut != 0) {
          if (outPID >= maxOut) {
            outPID = maxOut;
            integralE -= error;
          } else if (outPID <= minOut) {
            outPID = minOut;
            integralE -= error;
          }
        }
        //DEBUG_PRINT(integralE);DEBUG_PRINT("\t");

        return outPID;
      }
    }
};

void PID::param(float  vKp, float  vKi, float  vKd, int vmode) {
  Kp = vKp;
  Ki = vKi;
  Kd = vKd;
  mode = vmode;
}

void PID::readSensor(float vPv) {
  pv = vPv;
}

void PID::setPoint(float sp) {
  sv = sp;
}
void PID::timeSampling( int ts) {
  Tc = ts;
}

void PID::constraint(float Min, float Max) {
  minOut = Min;
  maxOut = Max;
  if (minOut > maxOut) {
    DEBUG_PRINTLN("Error 1 \nThe value of min don't over velue of max \n.constraint(min,max)");
    syntaxError = 1;
  }
}

PID PID;
