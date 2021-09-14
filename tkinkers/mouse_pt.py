import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import os
import math
import sys
import time
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1280x768")
        self.master.title('tkinter canvas trial')
        
        self.vcap = cv2.VideoCapture(0)
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH ) // 2
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT ) // 2
        self.pack()
        self.create_movie_frame()
        self.create_mouse_pt_widgets()
        self.delay = 15 #[mili seconds]
        self.update()
        
    def create_mouse_pt_widgets(self):
        self.start_x = tk.StringVar()
        self.start_y = tk.StringVar()
        self.current_x = tk.StringVar()
        self.current_y = tk.StringVar()
        self.stop_x = tk.StringVar()
        self.stop_y = tk.StringVar()

        self.label_description = tk.ttk.Label(self, text='Mouse position')
        self.label_description.grid(row=0, column=1)
        self.label_start_x = tk.ttk.Label(self, textvariable=self.start_x)
        self.label_start_x.grid(row=1, column=1)
        self.label_start_y = tk.ttk.Label(self, textvariable=self.start_y)
        self.label_start_y.grid(row=2, column=1)
        self.label_current_x = tk.ttk.Label(self, textvariable=self.current_x)
        self.label_current_x.grid(row=3, column=1)
        self.label_current_y = tk.ttk.Label(self, textvariable=self.current_y)
        self.label_current_y.grid(row=4, column=1)
        self.label_stop_x = tk.ttk.Label(self, textvariable=self.stop_x)
        self.label_stop_x.grid(row=5, column=1)
        self.label_stop_y = tk.ttk.Label(self, textvariable=self.stop_y)
        self.label_stop_y.grid(row=6, column=1)

        self.test_canvas = tk.Canvas(self, width=300, height=300, highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, rowspan=7)
        

    def create_movie_frame(self):

        #Frame_Camera
        self.frame_cam = tk.Frame(self.master)
        self.frame_cam.place(x = 10, y = 10)
        self.frame_cam.configure(width = self.width+30, height = self.height+50)
        self.frame_cam.grid_propagate(0)

        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=0,padx = 10, pady=10)
        self.canvas1.bind('<ButtonPress-1>', self.start_pickup)
        self.canvas1.bind('<B1-Motion>', self.pickup_position)
        self.canvas1.bind('<ButtonRelease-1>', self.stop_pickup)
        #self.canvas1.create_rectangle(self.start_x, self.start_y, self.current_x, self.current_y, fill="blue", tag="rectangle")
        
    def update(self):
        #Get a frame from the video source
        _, frame = self.vcap.read()

        frame = cv2.resize(frame, (int(self.width), int(self.height)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

        #self.photo -> Canvas
        self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)

        self.master.after(self.delay, self.update)

    def start_pickup(self, event):
        self.start_x.set('x1 : ' + str(event.x))
        self.start_y.set('y1 : ' + str(event.y))
        self.stop_x.set('')
        self.stop_y.set('')

    def pickup_position(self, event):
        self.current_x.set('x2 : ' + str(event.x))
        self.current_y.set('y2 : ' + str(event.y))

    def stop_pickup(self, event):
        self.stop_x.set('stop x : ' + str(event.x))
        self.stop_y.set('stop y : ' + str(event.y))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
