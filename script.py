import cv2
import numpy as np

# def nothing(x):
#     pass

def detect_and_count_balls(frame, pixels_per_cm, min_size_pixels,warna):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if warna == 1 :
        lower = np.array([0, 100, 100]) #L_RED
        upper = np.array([10, 255, 255])#U_RED
    if warna == 2 :
        lower = np.array([61, 100, 100])#L_BLUE
        upper = np.array([112, 255, 255])#U_BLUE
    if warna == 3 :
        lower = np.array([114, 100, 100])#L_PURPLE
        upper = np.array([130, 255, 255])#U_PURPLE

    masking = cv2.inRange(hsv, lower, upper)
    cv2.imshow("Result Frame (Red)", masking)
    result_frame = cv2.bitwise_and(frame, frame, mask=masking)
    contours, _ = cv2.findContours(masking, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("result_frame Frame", result_frame)
    # cv2.imshow("mask_red Frame", masking)
    
    ball_count = 0
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_size_pixels:  # Minimum size requirement
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                object_size_cm = 2 * np.sqrt(area / np.pi) / pixels_per_cm  # Diameter
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle
                cv2.putText(frame, f"{object_size_cm:.2f} cm", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(frame, f"({cx}, {cy})", (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(frame, f"BALL_RED {ball_count + 1} ", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                if cx < 213:
                    cv2.putText(frame, f"left", (cx - 5, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),2)
                if cx > 213 and cx < 427:
                    cv2.putText(frame, f"center", (cx - 5, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2)                    
                if cx > 427:
                    cv2.putText(frame, f"right", (cx - 5, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2)
                ball_count += 1
    if ball_count > 0:
        cv2.putText(frame, f"Total BOLA_MERAH: {ball_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2)
    print((ball_count))
    return frame, result_frame
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    
    result_frame, _  = detect_and_count_balls(frame, pixels_per_cm=20, min_size_pixels=1000, warna = 2)
    
    cv2.imshow("Result Frame", red_result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
