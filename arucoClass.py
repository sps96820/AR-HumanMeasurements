import cv2
import numpy as np



class scaleAq:
    def __init__(self):
        self.image = None
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_250)
        self.arucoParam = cv2.aruco.DetectorParameters()
        self.arucoPresent = False

        # class variables for ratio array and average Ratio
        #self.ratioArray = []
        #self.averageRatio = 0

   
    def scale(self, image):
        #while i < 30:
        self.arucoPresent = False
        #_, image = self.cap.read()
        bboxs, ids, rejected = cv2.aruco.detectMarkers(image, self.arucoDict, parameters = self.arucoParam)
        int_corners = np.int0(bboxs)

        if bboxs:
            
            aruco_perimeter = cv2.arcLength(bboxs[0], True)


            self.ratio = aruco_perimeter / 32
            self.arucoPresent = True
                
            cv2.polylines(image, int_corners, True, (0, 255, 0), 2)
        return self.arucoPresent
