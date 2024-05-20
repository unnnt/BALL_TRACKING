import cv2

import numpy as np
import serial
import time

# Komentar atau hapus kode terkait GPIO
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(25, GPIO.IN)  # Pin 25 sebagai input
# GPIO.setup(5, GPIO.OUT)  # Pin 5 untuk LED merah
# GPIO.setup(6, GPIO.OUT)  # Pin 6 untuk LED biru

serial_port = serial.Serial('COM4', 115200)  # Ganti 'COMx' dengan port USB yang digunakan

def kirim_nilai_analog(nilai):
    serial_port.write(f"S{nilai}E\n".encode('utf-8'))
    time.sleep(0.1)

def is_circle(contour):
    hull = cv2.convexHull(contour)
    area = cv2.contourArea(hull)
    (x, y), radius = cv2.minEnclosingCircle(hull)
    circle_area = np.pi * radius ** 2
    area_ratio = area / circle_area
    return 0.5 <= area_ratio <= 1.2

def detect_and_count_balls(frame, pixels_per_cm, min_size_pixels, warna, focal_length):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if warna == 1:
        saturation_lower = 100
        value_lower = 100
        saturation_upper = 255
        value_upper = 255

        lower_red1 = np.array([0, saturation_lower, value_lower])
        upper_red1 = np.array([10, saturation_upper, value_upper])

        lower_red2 = np.array([160, saturation_lower, value_lower])
        upper_red2 = np.array([179, saturation_upper, value_upper])

        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

        masking = cv2.bitwise_or(mask_red1, mask_red2)
    elif warna == 2:
        lower = np.array([90, 30, 100])  # L_BLUE
        upper = np.array([110, 255, 255])  # U_BLUE
        masking = cv2.inRange(hsv, lower, upper)
    elif warna == 3:
        lower = np.array([114, 100, 100])  # L_PURPLE
        upper = np.array([130, 255, 255])  # U_PURPLE
        masking = cv2.inRange(hsv, lower, upper)
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(masking, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result_frame = cv2.bitwise_and(frame, frame, mask=masking)
    cv2.imshow("abu Frame", gray)
    cv2.imshow("rgb Frame", result_frame)
    
    ball_count = 0
    closest_distance = float('inf')
    closest_ball = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_size_pixels:
            hull = cv2.convexHull(contour)
            (x, y), radius = cv2.minEnclosingCircle(hull)
            object_size_pixels = 2 * radius
            object_size_cm = object_size_pixels / pixels_per_cm

            nilai_sensor_x = x
            nilai_sensor_y = y

            real_object_size_cm = 7
            distance = (real_object_size_cm * focal_length) / object_size_pixels

            left_half = frame[:, :int(x)]
            right_half = frame[:, int(x):]
            
            visibility_percent = area / (np.pi * (object_size_pixels / 2) ** 2) * 100

            hsv_left = cv2.bitwise_and(left_half, left_half, mask=masking[:, :int(x)])
            hsv_right = cv2.bitwise_and(right_half, right_half, mask=masking[:, int(x):])
            hsv_area_left = cv2.countNonZero(cv2.cvtColor(hsv_left, cv2.COLOR_BGR2GRAY))
            hsv_area_right = cv2.countNonZero(cv2.cvtColor(hsv_right, cv2.COLOR_BGR2GRAY))
            
            if visibility_percent < 75:
                sisi = -1 if hsv_area_left > hsv_area_right else 1
            else:
                sisi = 0

            if distance < closest_distance:
                closest_distance = distance
                closest_ball = (x, y)

            ball_count += 1
            
            kirim_nilai_analog(f"{nilai_sensor_x} {nilai_sensor_y} {sisi} {visibility_percent} {distance}") 

            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.putText(frame, f"{distance:.2f} cm ({sisi})", (int(x) - int(radius), int(y) - int(radius) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"{visibility_percent:.2f} %)", (int(x) - int(radius), int(y) - int(radius) - 36), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)

    if ball_count > 0:
        cv2.putText(frame, f"TOTAL BOLA: {ball_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if closest_ball is not None:
        x, y = closest_ball
        cv2.putText(frame, "Terdekat", (int(x) - 20, int(y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame, result_frame

cap = cv2.VideoCapture(0)  # Menggunakan kamera default laptop

# Menggunakan focal length yang dihitung dari program terpisah
focal_length = 707  # Ganti dengan nilai focal length yang dihitung

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    # Mengatur warna yang akan dideteksi
    # Pada laptop, kita bisa secara manual mengatur warna yang ingin dideteksi
    warna = 1  # Ubah nilai ini menjadi 1 untuk merah, 2 untuk biru, 3 untuk ungu

    result_frame, _ = detect_and_count_balls(frame, pixels_per_cm=25, min_size_pixels=1000, warna=warna, focal_length=focal_length)
    cv2.imshow("Result Frame", result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        serial_port.close()
        cap.release()
        cv2.destroyAllWindows()
        break

serial_port.close()
cap.release()
cv2.destroyAllWindows()
