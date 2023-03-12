import sys
from pip import main
import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
import threading
import mpmeasure as mpm
from calibrationClass import calibration as cal
from arucoClass import scaleAq as aru

# Define a function to update the webcam output
def update_frame(imagearr):
    global label
    _, frame = cap.read()
    if len(imagearr) != 30:
        imagearr.append(frame)
    cv2.imshow("image", cv2.flip(frame,1))
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        return
    if finished:
        cv2.destroyAllWindows()
        return
    update_frame(imagearr)

# Function for main
def main():
    global cap, finished
    sys.setrecursionlimit(9999)
    finished = False
    imagearr = []
    cap = cv2.VideoCapture(0)
    vid = threading.Thread(target = update_frame, args=(imagearr,))
    vid.start()
    time.sleep(2)
    # Undistort images
    calib = cal()
    calib.getMatrix(imagearr)
    corrected = []
    for img in imagearr:
        corrected.append(calib.undistortImage(img))
    print("before scale")
    ratio = scale(corrected)
    print(ratio)
    # Get scale and measurements
    if ratio == 0:
        # Panic
        return
    measurelist = []
    for image in corrected:
        measurelist.append(mpm.media(image))
    avglist = measureavg(measurelist, ratio)
    # Print final values
    print("Height: " + avglist[0] + "\nShoulder: " + avglist[1] + "\nArms: " + avglist[2])
    finished = True
    
def scale(corrected):
    sca = aru()
    ratio = []
    # Get the scales for each image
    for img in corrected:
        print("in for")
        if sca.scale(img):
            ratio.append(sca.ratio)
    print("after for in scale")
    # Check for issues
    if len(ratio) < 15:
        print("no aruco images found")
        return 0
    # Calculating the average scale
    temp = 0
    for num in ratio:
        temp = temp + num
    temp = temp / len(ratio)
    return temp

def measureavg(measurelist, ratio):
    height = 0
    shoulder = 0
    arms = 0
    # Add together all of the measurements in the lists
    for num in measurelist[0]:
        height+=num
        #height = list[0]
        #shoulder = list[1]
        #arms = list[2]
    print(height)
    # Average the measurements
    height = height / len(measurelist)
    shoulder = shoulder / len(measurelist)
    arms = arms / len(measurelist)
    # Scale and return
    height = height / ratio
    shoulder = shoulder / ratio
    arms = arms / ratio
    return height, shoulder, arms

if __name__ == "__main__":
    main()