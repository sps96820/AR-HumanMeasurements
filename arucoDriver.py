from arucoClass import scaleAq
import cv2
from calibrationClass import calibration

cap = cv2.VideoCapture(0)
temp = scaleAq()
calib = calibration()


images = []
i = 0
while i < 30:
    _, image = cap.read()
    images.append(image)
    #temp.scale(image)
    #print(temp.ratio)
    i+=1

calib.getMatrix(images)

while True:
    _, image = cap.read()
    image = calib.undistortImage(image)
    cv2.imshow("image", image)
    temp.scale(image)
    print(temp.ratio)
    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()