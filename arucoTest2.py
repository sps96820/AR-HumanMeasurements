import cv2
import numpy as np



class scaleAq:
    def __init__(self):
        self.image = None
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_250)
        self.arucoParam = cv2.aruco.DetectorParameters()

        self.cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        #cap.set(cv2.CAP_PROP_FPS, 120)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.ratio = 0

        self.ratioArray = []
        self.averageRatio = 0

    '''
    def getRatio(self):
        return self.ratio

    def getAverageRatio(self):
        return self.averageRatio
    '''
    def scale(self):

        i = 0
        while i < 30:

            _, image = self.cap.read()
            bboxs, ids, rejected = cv2.aruco.detectMarkers(image, self.arucoDict, parameters = self.arucoParam)
            int_corners = np.int0(bboxs)

            if bboxs:
            
                aruco_perimeter = cv2.arcLength(bboxs[0], True)
                #print(aruco_perimeter)

                self.ratio = aruco_perimeter / 32
                self.ratioArray.append(self.ratio)
                #print(self.ratio)
                i+=1

                
                cv2.polylines(image, int_corners, True, (0, 255, 0), 2)
            cv2.imshow("image", image)
            key = cv2.waitKey(1)
            if key == 27:
                self.cap.release()
                cv2.destroyAllWindows()
                break
        sum = 0
        for temp in self.ratioArray:
            sum+= temp
        self.averageRatio = sum / 30

#cap.release()
#cv2.destroyAllWindows()