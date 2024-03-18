//#define SOFTWARE_SERIAL
#define SERIAL_MONITOR

#define KONDISI_SERVO false

#if defined(SERIAL_MONITOR)
#define DEBUG_BEGIN(x) Serial.begin(x)
#define DEBUG_PRINT(x) Serial.print(x)
#define DEBUG_PRINTLN(x) Serial.println(x)
#elif defined(SOFTWARE_SERIAL)
#include <SoftwareSerial.h>
SoftwareSerial mySerial(11, 10); // RX, TX
#define DEBUG_BEGIN(x) mySerial.begin(x)
#define DEBUG_PRINT(x) mySerial.print(x)
#define DEBUG_PRINTLN(x) mySerial.println(x)
#else
#define DEBUG_BEGIN(x)
#define DEBUG_PRINT(x)
#define DEBUG_PRINTLN(x)
#endif

#if KONDISI_SERVO
#include <Servo.h>
Servo myServo;
#define SERVO_PIN(x) myServo.attach(x)
#define SERVO_WRITE(x) myServo.write(x);
#else
#define SERVO_PIN(x)
#define SERVO_WRITE(x)
#endif

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET     4
Adafruit_SSD1306 display(128, 32, &Wire, OLED_RESET);
//============================================================================================================VARIABEL=================================
int x, y;
