#from keras.models import load_model
from tkinter import *
import tkinter as tk
import appscript
from PIL import ImageGrab, Image
import numpy as np
import pyocr
import pyocr.builders
import cv2


def call_ocr_tool():
    tools = pyocr.get_available_tools()
    # if there is no OCR tools, end up.
    if len(tools) == 0:
       print("OCRソフトが見つかりません。")
       sys.exit(1)
    # choose the first tool among the found ocr tools list.
    tool = tools[0]
    return tool
    
def predict_digit(img):
    # crop the image by specifing coordinates
    tool = call_ocr_tool()
    txt=tool.image_to_string(img,
                             lang="eng",
                             builder=pyocr.builders.DigitBuilder(tesseract_layout=6))
    print(txt, img.size)
    return img

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0
        
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Draw..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting)   
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
       
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        #HWND = self.canvas.winfo_id()  # get the handle of the canvas
        #rect=self.canvas.coords(HWND)
        #rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        #a,b,c,d = rect
        #a,b,c,d=self.canvas.winfo_rootx(), self.canvas.winfo_rooty(), self.canvas.winfo_width(),self.canvas.winfo_height() 
        x, y = (self.canvas.winfo_rootx(), self.canvas.winfo_rooty())
        width, height = (self.canvas.winfo_width(), self.canvas.winfo_height())
        a, b, c, d = (x, y, x+width, y+height)
        rect=(a+4,b+4,c-4,d-4)
        im = ImageGrab.grab(rect)

        _ = predict_digit(im)
        #self.label.configure(text=str(txt))

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        HWND=self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
       
app = App()
mainloop()
