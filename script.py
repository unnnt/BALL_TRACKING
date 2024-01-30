import cv2
import numpy as np

def nothing(x):
    pass

def detect_and_count_balls(frame, pixels_per_cm, min_size_pixels,warna):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if warna == 1 :
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])

        mask_red = cv2.inRange(hsv, lower_red, upper_red)

        cv2.imshow("Result Frame (Red)", mask_red)
        result_frame_RED = cv2.bitwise_and(frame, frame, mask=mask_red)

        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

                    if cx < 71.1:
                        cv2.putText(frame, f"RED_left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                                    2)
                        # print("KIRI")
                    if cx > 71.2 and cx < 142.3:
                        cv2.putText(frame, f"RED_3/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 142.4 and cx < 213.5:
                        cv2.putText(frame, f"RED_2/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 213.6 and cx < 284.7:
                        cv2.putText(frame, f"RED_1/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("KIRI")
                    if cx > 284.8 and cx < 355.9:
                        cv2.putText(frame, f"RED_center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 356 and cx < 427.1:
                        cv2.putText(frame, f"RED_1/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 427.2 and cx < 498.3:
                        cv2.putText(frame, f"RED_2/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("KIRI")
                    if cx > 498.4 and cx < 569.5:
                        cv2.putText(frame, f"RED_3/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 569.6:
                        cv2.putText(frame, f"RED_right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)

                    ball_count += 1
                    if cx > 0:
                        cv2.putText(frame, f"Total BOLA_MERAH: {ball_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)

        return frame, result_frame_RED

    elif warna == 2 :
        lower_blue = np.array([61, 100, 100])
        upper_blue = np.array([112, 255, 255])

        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        cv2.imshow("Result Frame (Blue)", mask_blue)
        result_frame_BLUE = cv2.bitwise_and(frame, frame, mask=mask_blue)

        contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
                    cv2.putText(frame, f"{object_size_cm:.2f} cm", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)
                    cv2.putText(frame, f"({cx}, {cy})", (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                                2)
                    cv2.putText(frame, f"BALL_BLUE {ball_count + 1} ", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)
                    if cx < 71.1:
                        cv2.putText(frame, f"BLUE_left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                                    2)
                        # print("KIRI")
                    if cx > 71.2 and cx < 142.3:
                        cv2.putText(frame, f"BLUE_3/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 142.4 and cx < 213.5:
                        cv2.putText(frame, f"BLUE_2/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 213.6 and cx < 284.7:
                        cv2.putText(frame, f"BLUE_1/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("KIRI")
                    if cx > 284.8 and cx < 355.9:
                        cv2.putText(frame, f"BLUE_center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255), 2)
                            # print("CEN")
                    if cx > 356 and cx < 427.1:
                        cv2.putText(frame, f"BLUE_1/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255), 2)
                            # print("CEN")
                    if cx > 427.2 and cx < 498.3:
                        cv2.putText(frame, f"BLUE_2/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255), 2)
                        # print("KIRI")
                    if cx > 498.4 and cx < 569.5:
                            cv2.putText(frame, f"BLUE_3/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255), 2)
                            # print("CEN")
                    if cx > 569.6:
                            cv2.putText(frame, f"BLUE_right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255), 2)

                    ball_count += 1
                    if cx > 0:
                        cv2.putText(frame, f"Total BOLA_BIRU: {ball_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)

        return frame, result_frame_BLUE

    elif warna == 3 :
        lower_purple = np.array([114, 100, 100])
        upper_purple = np.array([130, 255, 255])

        mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

        cv2.imshow("Result Frame (PURPLE)", mask_purple)
        result_frame_UNGU = cv2.bitwise_and(frame, frame, mask=mask_purple)

        contours, _ = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ball_count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_size_pixels:  # Minimum size requirement
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    data = (cx, cy)
                    print(data)

                    contour_img = np.zeros_like(frame)

                    object_size_cm = 2 * np.sqrt(area / np.pi) / pixels_per_cm  # Diameter

                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle
                    cv2.putText(frame, f"{object_size_cm:.2f} cm", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(frame, f"({cx}, {cy})", (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2),
                    cv2.putText(frame, f"BALL_PURPLE {ball_count + 1} ", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    if cx < 71.1:
                        cv2.putText(frame, f"PURPLE_left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                                    2)
                        # print("KIRI")
                    if cx > 71.2 and cx < 142.3:
                        cv2.putText(frame, f"PURPLE_3/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 142.4 and cx < 213.5:
                        cv2.putText(frame, f"PURPLE_2/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 213.6 and cx < 284.7:
                        cv2.putText(frame, f"PURPLE_1/4 left", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("KIRI")
                    if cx > 284.8 and cx < 355.9:
                        cv2.putText(frame, f"PURPLE_center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 356 and cx < 427.1:
                        cv2.putText(frame, f"PURPLE_1/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 427.2 and cx < 498.3:
                        cv2.putText(frame, f"PURPLE_2/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("KIRI")
                    if cx > 498.4 and cx < 569.5:
                        cv2.putText(frame, f"PURPLE_3/4 right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        # print("CEN")
                    if cx > 569.6:
                        cv2.putText(frame, f"PURPLE_right", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)

                    ball_count += 1
                    if cx > 0:
                        cv2.putText(frame, f"Total BOLA_UNGU: {ball_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
        return frame, result_frame_UNGU

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    
    red_result_frame, _ = detect_and_count_balls(frame, pixels_per_cm=20, min_size_pixels=1000,warna = 1)
    blue_result_frame, _ = detect_and_count_balls(frame, pixels_per_cm=20, min_size_pixels=1000,warna = 2)
    purple_result_frame, _ = detect_and_count_balls(frame, pixels_per_cm=20, min_size_pixels=1000,warna = 3)

    cv2.imshow("Original Frame", frame)
    cv2.imshow("Result Frame", red_result_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
