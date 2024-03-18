import cv2
import numpy as np

def calculate_focal_length(known_distance, known_object_size, object_size_pixels):
    return (object_size_pixels * known_distance) / known_object_size

def detect_focal_length():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame from camera.")
        return

    # Mengatur ukuran objek hijau dan jarak yang diketahui
    known_object_size = 7   # Ukuran objek sebenarnya dalam cm (sesuaikan dengan nilai yang benar)
    known_distance = 30  # Jarak objek dari kamera dalam cm

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mendefinisikan rentang warna hijau dalam ruang warna HSV (sesuaikan jika diperlukan)
    lower_green = np.array([0, 100, 100])  # L_RED
    upper_green = np.array([10, 255, 255])  # U_RED

    # Membuat masking untuk warna hijau
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Menghilangkan noise dengan operasi morfologi
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

    # Mencari contour objek hijau
    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Mengabaikan contour kecil
            (x, y), radius = cv2.minEnclosingCircle(contour)
            object_size_pixels = 2 * radius

            focal_length = calculate_focal_length(known_distance, known_object_size, object_size_pixels)
            print(f"Focal Length: {focal_length:.2f}")

            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.putText(frame, f"{known_distance} cm", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_focal_length()