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
import numpy as np
import mediapipe as mp


# Define a function to update the webcam output
def update_frame():
    global label
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    _, frame = cap.read()
    #if len(imagearr) != 30:
        #imagearr.append(frame)
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            
        results = pose.process(frame)
        mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        sca.scale(frame)
        if sca.bboxs:
            sca.scale(frame)
            int_corners = np.int0(sca.bboxs)
            cv2.polylines(frame, int_corners, True, (0, 255, 0), 2)

        calibFrameUpdate.singleImage(frame)
        if calibFrameUpdate.threedpoints:
            frame = cv2.drawChessboardCorners(frame, calibFrameUpdate.CHECKERBOARD, calibFrameUpdate.corners2, calibFrameUpdate.ret)
        
        cv2.imshow("image", cv2.flip(frame,1))
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            return
        if not im.is_alive:
            cv2.destroyAllWindows()
            return
        #update_frame(imagearr)

# Function for main
def main():
    time.sleep(4)
    global cap
    global sca
    sca = aru()
    global calib
    calib = cal()
    
    global calibFrameUpdate
    calibFrameUpdate = cal()
    
    sys.setrecursionlimit(9999)
    imagearr = []
    cap = cv2.VideoCapture(0)
    global im 
    im = threading.Thread(target = imaging, args=())
    im.start()
    while True:
        update_frame()

def imaging():
    time.sleep(2)
    # Undistort images
    #calib = cal()
    imagearr = []
    for i in range(30):
        _, tempCap = cap.read() 
        imagearr.append(tempCap)
    temp = calib.getMatrix(imagearr)
    while temp == False:
        print("Checkerboard not found. Hold it up", flush=True)
        for i in range(30):
            _, tempImage = cap.read() 
            imagearr[i] = tempImage
        time.sleep(2)
        temp = calib.getMatrix(imagearr)
        
    
    
    print("Put checkerboard down and hold aruco marker", flush=True)
    time.sleep(2)
    corrected = []
    for i in range(30):
        _, tempCap = cap.read() 
        corrected.append(tempCap)
        #corrected.append(calib.undistortImage(tempCap))
    ##for img in imagearr:
        #corrected.append(calib.undistortImage(img))

    print("before scale", flush=True)
    ratio = scale(corrected)
    print("ratio",flush=True)
    print(ratio,flush=True)
    # Get scale and measurements
    while ratio < 4:
        arucoArray = []
        print("Make sure aruco marker is visible", flush=True)
        time.sleep(2)
        for i in range(30):
            _, tempCap = cap.read() 
            arucoArray.append(tempCap)
            #arucoArray.append(calib.undistortImage(tempCap))
            
        ratio = scale(arucoArray)
        print("length", len(arucoArray), flush=True)
        print("ratio",flush=True)
        print(ratio,flush=True)
    
    CAM_CONTROL = True
    
    mediapipeImgs = []
    
    print("Put papers down", flush=True)
    time.sleep(3)
    for i in range(30):
        _, tempCap = cap.read() 
        mediapipeImgs.append(tempCap)
        #mediapipeImgs.append(calib.undistortImage(tempCap))
        #mediapipeImgs[i] = calib.undistortImage(mediapipeImgs[i])
    
    measurelist = [[] for i in range(3)]
    #for image in corrected:
    for image in mediapipeImgs:
        temparray = mpm.media(image)
        print(tempCap, flush=True)
        measurelist[0].append(temparray[0])
        measurelist[1].append(temparray[1])
        measurelist[2].append(temparray[2])
    avglist = measureavg(measurelist, ratio)
    # Print final values
    print("Height: ", avglist[0], "\nShoulder: ", avglist[1], "\nArms: ", avglist[2], flush=True)
    
    
    
def scale(corrected):
    #sca = aru()
    ratio = []
    # Get the scales for each image
    for img in corrected:
        print("in for", flush = True)
        if sca.scale(img):
            #print(sca.scale(img), flush=True)
            ratio.append(sca.ratio)
    print("after for in scale", flush=True)
    # Check for issues
    if len(ratio) < 15:
        print("no aruco images found", flush=True)
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
    heightL = 0
    shoulderL = 0
    armsL = 0
    for list in measurelist:
        if counter == 0:
            heightL = len(list)
        elif counter == 1:
            shoulderL = len(list)
        elif counter == 2:
            armsL = len(list)
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
    height = height / heightL
    shoulder = shoulder / shoulderL
    arms = arms / armsL
    # Scale and return
    height = height / ratio
    shoulder = shoulder / ratio
    arms = arms / ratio
    return height, shoulder, arms

if __name__ == "__main__":
    main()