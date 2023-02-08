import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
import mediapipe as mp
mp_dr = mp.solutions.drawing_utils
mp_drst = mp.solutions.drawing_styles
mp_h = mp.solutions.holistic

# Create the GUI window
root = tk.Tk()
root.title("Webcam Controller")

# Define a function to turn on/off the webcam
def webcam_toggle():
    global cap, label
    if cap.isOpened():
        cap.release()
        label.config(image="")
    else:
        cap = cv2.VideoCapture(0)
        # x = threading.Thread(target=media, args=())
        # x.start()
        media()

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

def media():
    cap = cv2.VideoCapture(0)
    with mp_h.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
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
            results = holistic.process(image)

            # Draw landmark annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_dr.draw_landmarks(
                image,
                results.face_landmarks,
                mp_h.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drst
                .get_default_face_mesh_contours_style())
            mp_dr.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_h.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drst
                .get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()

# Create a button to control the webcam
button = tk.Button(root, text="Turn On/Off Webcam", command=webcam_toggle)
button.pack()

# Create a label to display the webcam output
label = tk.Label(root)
label.pack()

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.release()

# Start the GUI event loop
root.mainloop()
