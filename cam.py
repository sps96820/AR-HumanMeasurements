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
    if not im.is_alive:
        cv2.destroyAllWindows()
        return
    update_frame(imagearr)

# Function for main
def main():
    global cap
    sys.setrecursionlimit(9999)
    imagearr = []
    cap = cv2.VideoCapture(0)
    global im 
    im = threading.Thread(target = imaging, args=(imagearr,))
    im.start()
    update_frame(imagearr)

def imaging(imagearr):
    time.sleep(2)
    # Undistort images
    calib = cal()
    calib.getMatrix(imagearr)
    corrected = []
    for img in imagearr:
        corrected.append(calib.undistortImage(img))
    print("before scale")
    ratio = scale(corrected)
    print("ratio")
    print(ratio)
    # Get scale and measurements
    if ratio == 0:
        # Panic
        return
    
    mediapipeImgs = []
    
    print("Put papers down")
    time.sleep(3)
    for i in range(30):
        _, temp = cap.read() 
        mediapipeImgs.append(calib.undistortImage(temp))
        #mediapipeImgs[i] = calib.undistortImage(mediapipeImgs[i])
    
    measurelist = [[] for i in range(3)]
    #for image in corrected:
    for image in mediapipeImgs:
        temp = mpm.media(image)
        print(temp)
        measurelist[0].append(temp[0])
        measurelist[1].append(temp[1])
        measurelist[2].append(temp[2])
    avglist = measureavg(measurelist, ratio)
    # Print final values
    print("Height: ", avglist[0], "\nShoulder: ", avglist[1], "\nArms: ", avglist[2])
    
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
    counter = 0
    for list in measurelist:
        for num in list:
            if counter == 0:
                height += num
            elif counter == 1:
                shoulder += num
            elif counter == 2:
                arms += num
        counter += 1
        #height = list[0]
        #shoulder = list[1]
        #arms = list[2]
    print(height)
    print(shoulder)
    print(arms)
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