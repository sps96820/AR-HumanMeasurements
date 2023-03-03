import cv2
import numpy as np



#image=cv2.imread("aruco_objects/aruco_object.jpg")


arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_250)
arucoParam = cv2.aruco.DetectorParameters()

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
#cap.set(cv2.CAP_PROP_FPS, 120)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:

    _, image = cap.read()
    bboxs, ids, rejected = cv2.aruco.detectMarkers(image, arucoDict, parameters = arucoParam)
    int_corners = np.int0(bboxs)

    if bboxs:
    
        aruco_perimeter = cv2.arcLength(bboxs[0], True)
        print(aruco_perimeter)

        ratio = aruco_perimeter / 8

        print(ratio)

        cv2.polylines(image, int_corners, True, (0, 255, 0), 2)
    cv2.imshow("image", image)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()