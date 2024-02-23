import cv2
import numpy as np

def calculate_focal_length(real_object_size_cm, object_size_cm, distance_cm):
    # Rumus untuk menghitung panjang fokus
    focal_length = (real_object_size_cm * distance_cm) / object_size_cm
    return focal_length

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Diameter bola di dunia nyata (contoh: 10 cm)
real_object_size_cm = 1.3

while True:
    ret, frame = cap.read()

    # Konversi ke warna abu-abu
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi bola menggunakan metode deteksi sederhana (contoh: deteksi tepi)
    edges = cv2.Canny(gray, 50, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=50)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Gambar lingkaran dan tampilkan diameter
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            diameter_pixels = i[2] * 2
            distance_cm = 20.0  # Jarak antara kamera dan objek (contoh: 50 cm)
            focal_length = calculate_focal_length(real_object_size_cm, diameter_pixels, distance_cm)
            cv2.putText(frame, f"Diameter: {diameter_pixels:.2f} cm, Focal Length: {focal_length:.2f} pixels", (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Tampilkan hasil di layar
    cv2.imshow('Object Measurement', frame)

    # Tombol 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Hentikan kamera dan tutup jendela
cap.release()
cv2.destroyAllWindows()
