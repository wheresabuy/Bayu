import cv2
import datetime
import signal
import sys
import os

running = True

def handle_stop(sig, frame):
    global running
    # Gunakan flush=True supaya log langsung muncul di journalctl tanpa nunggu
    print("\n[INFO] Menutup rekaman...", flush=True)
    running = False

signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGINT, handle_stop)

save_path = "/home/pi/Bayu"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Pake MP4 + MP4V (Ini paling stabil di Ubuntu/LOQ lu)
extension = ".mp4"
base_name = "BayuRecord_Session"
filename = os.path.join(save_path, f"{base_name}{extension}")

counter = 1
while os.path.exists(filename):
    filename = os.path.join(save_path, f"{base_name}_{counter}{extension}")
    counter += 1

cap = cv2.VideoCapture(2)
# Set FPS manual biar sinkron
fps = 20.0
cap.set(cv2.CAP_PROP_FPS, fps)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename, fourcc, fps, size)

if not out.isOpened():
    print(f"[ERROR] Gagal buka: {filename}", flush=True)
    sys.exit(1)

print(f"[SUCCESS] Start recording: {filename}", flush=True)

frame_count = 0
while running:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Kamera ilang/diskonek!", flush=True)
        break
    
    out.write(frame)
    frame_count += 1
    
    # Log setiap 100 frame biar lu tau dia ga stuck
    if frame_count % 100 == 0:
        print(f"[PROGRESS] Sudah merekam {frame_count} frame...", flush=True)

cap.release()
out.release()
print(f"[FINISHED] Total frame: {frame_count}. File aman.", flush=True)
sys.exit(0)