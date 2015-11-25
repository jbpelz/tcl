import numpy as np
import sys
import cv2

from multiprocessing import Process
from multiprocessing import Queue


# from multiprocessing.Queue import Empty

from queue import Empty

from PIL import Image, ImageTk
import time
import tkinter as tk
from tkinter import ttk

#tkinter GUI functions----------------------------------------------------------
def quit_all(root, process):
     print("Quit button pressed ... terminating processes and destroying window")
     process.terminate()
     print("Process should have been terminated")
     root.destroy()
     print("Root destroyed")

def pause_video():
     print("Pause button pressed ... pausing a couple of seconds ...")
     cv2.waitKey(2000)

def update_image(image_label, queue):
    frame = queue.get()
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    a = Image.fromarray(im)
    b = ImageTk.PhotoImage(image=a)
    image_label.configure(image=b)
    image_label._image_cache = b  # avoid garbage collection
    root.update()


def update_all(root, image_label, queue, msecDelay):
    update_image(image_label, queue)
    root.after(0, func=lambda: update_all(root, image_label, queue, msecDelay))


#multiprocessing image processing functions-------------------------------------
def frame_read(queue):
    # vidFile = cv2.VideoCapture(0)
    vidFile = cv2.VideoCapture('short_eye.mov')
    while True:
        try:
            flag, frame=vidFile.read()
            if flag==0:
                break
            queue.put(frame)
            cv2.waitKey(msecDelay)
        except:
            continue

if __name__ == '__main__':
    msecDelay = 20  # delay during image display

    queue = Queue()
    print('queue initialized...')
    root = tk.Tk()
    print('GUI initialized...')
    image_label = tk.Label(master=root)# label for the video frame
    image_label.pack()
    print('GUI image label initialized...')
    p = Process(target=frame_read, args=(queue,))
    p.start()
    print('frame reading process has started...')

    # quit button
    quitButton = tk.Button(master=root, text='Quit', command=lambda: quit_all(root, p))
    quitButton.pack()
    print('quit button initialized...')

    # pause button
    pauseButton = tk.Button(master=root, text='Pause', command=lambda: pause_video())
    pauseButton.pack()
    print('quit button initialized...')

    # Speed slider ('scale')
    msecDelay = tk.DoubleVar()
    speedScale = ttk.Scale(master=root, orient=tk.HORIZONTAL, length=400, variable=msecDelay, from_= 2.0, to = 500.0)
    speedScale.config(variable=1.0)  # Initialized to normal speed
    speedScale.pack()
    print('Speed slider initialized...')

    speedFeedbackbar = ttk.Progressbar(master=root, orient=tk.HORIZONTAL, length = 200)
    speedFeedbackbar.pack()

    speedFeedbackbar.config(mode='determinate', maximum = 500.0, value = 20.0)
    speedFeedbackbar.config(variable=msecDelay)


    # setup the update callback
    root.after(0, func=lambda: update_all(root, image_label, queue, msecDelay))
    print('root.after was called...')
    root.mainloop()
    print('mainloop exit')
    p.join()
    print('image capture process exit')