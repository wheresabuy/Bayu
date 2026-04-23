import cv2
import datetime
import signal
import sys
import os

running = True

def handle_stop(sig, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGINT, handle_stop)

save_path = "/home/muhammad/recordings"
if not os.path.exists(save_path):
    os.makedirs(save_path)

base_name = "BayuRecord_Session.avi"
filename = os.path.join(save_path, base_name)

counter = 1
while os.path.exists(filename):
    filename = os.path.join(save_path, f"BayuRecord_Session_{counter}.mp4")
    counter += 1

cap = cv2.VideoCapture(2)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename, fourcc, 20.0, size)

while running:
    ret, frame = cap.read()
    if not ret:
        break
    
    out.write(frame)

cap.release()
out.release()
sys.exit(0)