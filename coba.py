import cv2
import numpy as np
import serial
import time

serial_port = serial.Serial('COM4', 115200)  # Ganti 'COMx' dengan port USB yang digunakan

def kirim_nilai_analog(x, y, sisi, visibility_percent, distance):
    data_string = f"{x} {y} {sisi} {visibility_percent:.2f} {distance:.2f}"
    serial_port.write(data_string.encode('utf-8') + b'\n')
    time.sleep(0.1)

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
        
    result_frame = cv2.bitwise_and(frame, frame, mask=masking)

    gray = cv2.cvtColor(result_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2, 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                               param1=100, param2=30, minRadius=15, maxRadius=160)

    ball_count = 0
    closest_distance = float('inf')
    closest_ball = None

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, radius) in circles:
            object_size_pixels = 2 * radius
            object_size_cm = object_size_pixels / pixels_per_cm
            real_object_size_cm = 7
            distance = (real_object_size_cm * focal_length) / object_size_pixels
            
            nilai_sensor_x = x
            nilai_sensor_y = y

            mask_circle = np.zeros_like(masking)
            cv2.circle(mask_circle, (x, y), radius, 255, -1)
            intersection = cv2.bitwise_and(masking, mask_circle)
            left_half = intersection[:, :x]
            right_half = intersection[:, x:]
            left_area = cv2.countNonZero(left_half)
            right_area = cv2.countNonZero(right_half)
            visibility_percent = cv2.countNonZero(intersection) / (np.pi * (radius ** 2)) * 100

            if visibility_percent < 65:
                if left_area > right_area:
                    sisi = -1
                elif right_area > left_area:
                    sisi = 1
            else:
                sisi = 0

            if distance < closest_distance:
                closest_distance = distance
                closest_ball = (x, y)

            ball_count += 1

            kirim_nilai_analog(int(x), int(y), sisi, visibility_percent, distance)
            print(x,y)
            

            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.putText(frame, f"{distance:.2f} cm ({sisi})", (x - radius, y - radius - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"{visibility_percent:.2f} %", (x - radius, y - radius - 36), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)

        if ball_count > 0:
            cv2.putText(frame, f"TOTAL BOLA: {ball_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if closest_ball is not None:
            x, y = closest_ball
            cv2.putText(frame, "Terdekat", (x - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Result Frame", frame)
    cv2.imshow("Masked Frame", result_frame)

    return frame, result_frame

cap = cv2.VideoCapture(0)  # Menggunakan kamera default laptop

focal_length = 707  # Ganti dengan nilai focal length yang dihitung

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    warna = 2  # Ubah nilai ini menjadi 1 untuk merah, 2 untuk biru, 3 untuk ungu

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
