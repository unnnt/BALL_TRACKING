#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"

MPU6050 mpu;

bool dmpReady = false;
uint8_t mpuIntStatus;
uint8_t devStatus;
uint16_t packetSize;
uint16_t fifoCount;
uint8_t fifoBuffer[64];

Quaternion q;
VectorFloat gravity;
float ypr[3];

float kalmanYaw = 0.0;
float kalmanGain = 0.0;
float estimationError = 0.0001;
float measurementError = 0.00001; // Adjust as needed
float processNoise = 0.000001;   // Adjust as needed

void setup_mpu() {
    Wire.begin();
    Serial.begin(115200);

    mpu.initialize();
    if (!mpu.testConnection()) {
        Serial.println("MPU6050 connection failed");
        while (1);
    }

    // Set offset (adjust these values based on your calibration)
    mpu.setXAccelOffset(13108);
    mpu.setYAccelOffset(-14400);
    mpu.setZAccelOffset(5906);
    mpu.setXGyroOffset(72);
    mpu.setYGyroOffset(591);
    mpu.setZGyroOffset(-2);

    devStatus = mpu.dmpInitialize();

    if (devStatus == 0) {
        mpu.setDMPEnabled(true);
        dmpReady = true;
        mpuIntStatus = mpu.getIntStatus();
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        Serial.print("DMP Initialization failed (code ");
        Serial.print(devStatus);
        Serial.println(")");
    }
}


float getYaw() {
    if (!dmpReady) return 0.0;

    fifoCount = mpu.getFIFOCount();

    if (fifoCount == 1024) {
        mpu.resetFIFO();
    } else if (fifoCount >= packetSize) {
        mpu.getFIFOBytes(fifoBuffer, packetSize);
        mpuIntStatus = mpu.getIntStatus();

        mpu.dmpGetQuaternion(&q, fifoBuffer);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

        float yawInDegrees = ypr[0] * 180.0 / M_PI;

        if (yawInDegrees > 180) {
            yawInDegrees -= 360;
        } else if (yawInDegrees < -180) {
            yawInDegrees += 360;
        }

        // Kalman filter update
        kalmanGain = estimationError / (estimationError + measurementError);
        kalmanYaw = kalmanYaw + kalmanGain * (yawInDegrees - kalmanYaw);
        estimationError = (1.0 - kalmanGain) * estimationError + fabs(kalmanYaw) * processNoise;

        return kalmanYaw;
    }
    return kalmanYaw;
}
