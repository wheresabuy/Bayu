import cv2
from pathlib import Path
import signal
import sys
import os
import glob
import subprocess

running = True

def handle_stop(sig, frame):
    global running
    # Gunakan flush=True supaya log langsung muncul di journalctl tanpa nunggu
    print("\n[INFO] Menutup rekaman...", flush=True)
    running = False

signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGINT, handle_stop)

script_dir = Path(__file__).parent
save_path = script_dir / "video"
save_path.mkdir(exist_ok=True)

print(f"Folder created at: {save_path}")

# Pake MP4 + MP4V (Ini paling stabil di Ubuntu/LOQ lu)
extension = ".mp4"
base_name = "BayuRecord_Session"
filename = os.path.join(save_path, f"{base_name}{extension}")

counter = 1
while os.path.exists(filename):
    filename = os.path.join(save_path, f"{base_name}_{counter}{extension}")
    counter += 1

def find_camera_port() -> int:
    try:
        for dev in sorted(glob.glob("/dev/video*")):
            result = subprocess.run(["v4l2-ctl", "--device", dev, "--info"], capture_output=True, text=True)
            if "Capture" in result.stdout:
                # Remove '/dev/video' and convert the rest to an integer
                return int(dev.replace("/dev/video", ""))
    except Exception:
        pass

    devices = sorted(glob.glob("/dev/video*"))
    if devices:
        return int(devices[0].replace("/dev/video", ""))
    
    # Fallback directly to 0 instead of "/dev/video0"
    return 0

cap = cv2.VideoCapture(find_camera_port())
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