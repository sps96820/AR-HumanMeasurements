import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
close = 0

# Create the GUI window
root = tk.Tk()
root.title("Webcam Controller")

# Define a function to turn on/off the webcam
def webcam_toggle():
    global cap, label
    if cap.isOpened():
        cap.release()
        label.config(image="")
        global close
        close = 1
    else:
        close = 0
        cap = cv2.VideoCapture(0)
        x = threading.Thread(target=media, args=())
        x.start()

def media():
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
                #reyebrow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]
                #rheel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL]
                # lshoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                # rshoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                # rwrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                # rhip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                # lhip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                # rankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
                '''
                if close == 1:
                    height = reyebrow.y - rheel.y 
                    print(height)
                    break
                '''
                if cv2.waitKey(5) & 0xFF == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

# Create a button to control the webcam
button = tk.Button(root, text="Turn On/Off Webcam", command=webcam_toggle)
button.pack()

# Create a label to display the webcam output
label = tk.Label(root)
label.pack()

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.release()

tk.mainloop()