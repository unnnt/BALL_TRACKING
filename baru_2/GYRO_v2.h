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

const int numReadings = 20;
float readings[numReadings];
float average = 0;
float thd = 0.0000000000001;

void setup_mpu() {
    Wire.begin();
    Serial.begin(115200);

    mpu.initialize();
    mpu.testConnection();

    devStatus = mpu.dmpInitialize();

    if (devStatus == 0) {
        mpu.setDMPEnabled(true);
        dmpReady = true;
        mpuIntStatus = mpu.getIntStatus();
        packetSize = mpu.dmpGetFIFOPacketSize();

        for (int thisReading = 0; thisReading < numReadings; thisReading++) {
            readings[thisReading] = 0;
        }
    }
}

float getYaw(float yawThreshold) {
    if (!dmpReady) return 0;

    fifoCount = mpu.getFIFOCount();

    if (fifoCount == 1024) {
        mpu.resetFIFO();
    } else if (fifoCount >= 42) {
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

        for (int i = 0; i < numReadings - 1; i++) {
            readings[i] = readings[i+1];
        }
        readings[numReadings - 1] = yawInDegrees;

        float total = 0;
        for (int i = 0; i < numReadings; i++) {
            total += readings[i];
        }
        average = total / numReadings;

        if (abs(yawInDegrees - average) < yawThreshold) {
            return average;
        } else {
            return yawInDegrees;
        }
    }
    return average;
}
