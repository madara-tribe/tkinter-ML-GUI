import tkinter as tk
import glob
from PIL import Image, ImageTk, ImageOps, ImageDraw
import shutil
import os

SIZE=600
cnt = 1

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.master.title("image select")
        self.master.geometry('840x840')
        
        self.pngs = 'images/dog2.png'
        self.create_canvas(self.master)
    
    def create_canvas(self, root):
        img1 = Image.open(self.pngs)
        img1 = img1.resize((SIZE, SIZE))
        gazou = ImageTk.PhotoImage(img1)
        
        self.canvas = tk.Canvas(width=SIZE, height=SIZE, bg="black")
        self.canvas.place(x=100, y=100)
        self.canvas.create_image(0, 0, image=gazou, anchor=tk.NW)
        root.bind("<ButtonPress-1>",self.Push)
        root.bind("<ButtonRelease-1>",self.Release)
        root.bind("<Button1-Motion>",self.Motion)
        root.mainloop()
        
    def Push(self, event):
        global x_start,y_start
        x_start = event.x
        y_start = event.y
        self.canvas.create_rectangle(x_start,y_start,x_start+1,y_start+1,outline="red",tag="rect")

    #コールバック関数：タッチパッドから指を離したとき
    def Release(self, event):
        global x_end,y_end,cnt
        x_end = event.x
        y_end = event.y
        self.canvas.create_rectangle(x_start,y_start,x_end,y_end,outline="red")
        img = Image.open(self.pngs)
        img = img.resize((SIZE, SIZE))
        img.crop((x_start,y_start,x_end,y_end)).save(f"ocr_images/{cnt}.png")
        cnt = cnt + 1

    #コールバック関数：タッチパッド上で指を動かしている時
    def Motion(self, event):
        x_end = event.x
        y_end = event.y
        self.canvas.coords("rect",x_start,y_start,x_end,y_end)


if __name__ == "__main__":
    OCR_FOLDER='ocr_images'
    if os.path.exists(OCR_FOLDER):
        shutil.rmtree(OCR_FOLDER)
    os.makedirs(OCR_FOLDER)
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()

