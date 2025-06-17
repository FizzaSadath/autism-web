import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk


def play_video(video_path):
    # Function to play video from the given path
    cap = cv2.VideoCapture(video_path)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
            lbl_video.config(image=frame_image)
            lbl_video.image = frame_image
            lbl_video.after(10, update_frame)
        else:
            cap.release()

    update_frame()


def browse_file():
    # Function to browse and select a video file
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov")]
    )
    if file_path:
        play_video(file_path)


# Create main Tkinter window
root = tk.Tk()
root.title("Video Player")

# Create UI components
btn_browse = tk.Button(root, text="Browse Video", command=browse_file)
btn_browse.pack()

lbl_video = tk.Label(root)
lbl_video.pack()

# Run the Tkinter main loop
root.mainloop()
