from arucoClass import scaleAq
import cv2
from calibrationClass import calibration

cap = cv2.VideoCapture(0)
temp = scaleAq()
calib = calibration()



i = 0
while i < 300:
    _, image = cap.read()
    temp.scale(image)
    print(temp.ratio)
    i+=1



cap.release()
cv2.destroyAllWindows()