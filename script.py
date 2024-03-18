import cv2
import numpy as np
import serial
import time

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
    return 0.8 <= area_ratio <= 1.2

def detect_and_count_balls(frame, pixels_per_cm, min_size_pixels, warna, focal_length):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if warna == 1:
        lower = np.array([0, 100, 100])  # L_RED
        upper = np.array([10, 255, 255])  # U_RED
    elif warna == 2:
        lower = np.array([61, 100, 100])  # L_BLUE
        upper = np.array([112, 255, 255])  # U_BLUE
    elif warna == 3:
        lower = np.array([114, 100, 100])  # L_PURPLE
        upper = np.array([130, 255, 255])  # U_PURPLE

    masking = cv2.inRange(hsv, lower, upper)
    result_frame = cv2.bitwise_and(frame, frame, mask=masking)
    contours, _ = cv2.findContours(masking, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ball_count = 0
    closest_distance = float('inf')
    closest_ball = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_size_pixels and is_circle(contour):
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                object_size_pixels = 2 * np.sqrt(area / np.pi)
                object_size_cm = object_size_pixels / pixels_per_cm  # Diameter

                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Garis persegi hijau
                cv2.circle(frame, (cx, cy), int(object_size_pixels / 2), (255, 0, 0), 2)  # Lingkaran biru di sekeliling bola

                nilai_sensor_x = cx
                nilai_sensor_y = cy

                kirim_nilai_analog(f"{nilai_sensor_x} {nilai_sensor_y}")

                real_object_size_cm = 7  # Ganti dengan ukuran sebenarnya objek
                distance = (real_object_size_cm * focal_length) / object_size_pixels
                cv2.putText(frame, f"{distance:.2f} cm", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_ball = (x, y, w, h)

                ball_count += 1
                print(cx, cy, distance)

    if ball_count > 0:
        cv2.putText(frame, f"TOTAL BOLA: {ball_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if closest_ball is not None:
        x, y, w, h = closest_ball
        cv2.putText(frame, "Terdekat", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame, result_frame

cap = cv2.VideoCapture(0)

# Menggunakan focal length yang dihitung dari program terpisah
focal_length = 554.15  # Ganti dengan nilai focal length yang dihitung

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    result_frame, _ = detect_and_count_balls(frame, pixels_per_cm=25, min_size_pixels=1000, warna=1, focal_length=focal_length)
    cv2.imshow("Result Frame", result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

serial_port.close()
cap.release()