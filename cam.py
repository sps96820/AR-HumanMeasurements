from pip import main
import time
import cv2
from PIL import Image, ImageTk
import threading
import mpmeasure as mpm
import calibration as cal
import aruco as aru


# Define a function to update the webcam output
def update_frame():
    global cap, label
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    img = ImageTk.PhotoImage(frame)
    label.config(image=img)
    label.image = img
    root.after(30, update_frame)

# Function for main
def main():
    global cap, startframe, correctframe
    cap = cv2.VideoCapture(0)
    vid = threading.Thread(target = update_frame, args=())
    vid.start()
    time.sleep(5)
    calib = threading.Thread(target=cal.method, args=(startframe))
    calib.start()
    scale = threading.Thread(target=aru.method, args=(correctframe))
    scale.start()
    media = threading.Thread(target=mpm.media, args=(correctframe))
    media.start()
    

if __name__ == "__main__":
    main()