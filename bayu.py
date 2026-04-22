import cv2
import datetime

# 1. Inisialisasi Kamera (Coba 0, 1, atau 2)
cap = cv2.VideoCapture(2)

# 2. Atur Settingan Video
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

# Nama file pake timestamp biar gak ketumpuk tiap kali running
filename = datetime.datetime.now().strftime("BayuRecord_%Y-%m-%d_%H-%M-%S.avi")

# 3. Setup Writer (Codec XVID biasanya paling stabil di Ubuntu)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename, fourcc, 20.0, size)

print(f"Lagi merekam... File bakal disimpen jadi: {filename}")
print("Tekan 'q' buat stop dan simpen video.")

while True:
    ret, frame = cap.read()
    if ret:
        # Tulis frame ke file
        out.write(frame)

        # Tampil di layar
        cv2.imshow('Recording Bayucaraka...', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# 4. Beresin semua
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Selesai! Cek folder kamu, filenya ada di situ.")