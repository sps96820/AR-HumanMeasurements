import tkinter as tk
import cv2
from PIL import Image, ImageTk

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
        update_frame()

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
