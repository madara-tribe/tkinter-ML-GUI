import tkinter as tk
import tkinter.ttk as ttk
import os, glob
import shutil
import requests
import json
from PIL import Image, ImageTk, ImageOps, ImageDraw
from main import predict

URL = 'https://hooks.slack.com/services/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'

SIZE=600
cnt = 1
CROP_FOLDER='crop_images'

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        
        self.master.title("color prediction")
        self.master.geometry('840x840')
        self.filepath = 'images/1.jpeg'
        self.btn = tk.Button(text='Color estimation', command=self.pushed)
        self.btn.pack()
        self.all_entries = []
        # Enter text box
        self.setup()
        self.create_widgets()
        self.master.bind("<ButtonPress-1>",self.Push)
        self.master.bind("<ButtonRelease-1>",self.Release)
        self.master.bind("<Button1-Motion>",self.Motion)
        
    def setup(self):
        if os.path.exists(CROP_FOLDER):
            shutil.rmtree(CROP_FOLDER)
        os.makedirs(CROP_FOLDER)
        self.all_entries = []
        for _ in range(3):
            self.ent = tk.Entry(width=5)
            self.ent.place(x=30+(70*(len(self.all_entries)+1)), y=700)
            self.all_entries.append(self.ent)
        
    def create_widgets(self):
        img = Image.open(self.filepath)
        img = img.resize((SIZE, SIZE))
        self.img_ = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.master, width=SIZE,height=SIZE,bg="black")
        self.canvas.create_image(0, 0, image=self.img_, anchor=tk.NW)
        self.canvas.pack()
        self.clear_button = tk.Button(text='clear all', command=self.clear_canvas)
        self.clear_button.place(x=5, y=10)
        
    def Push(self, event):
        global x_start,y_start
        x_start = event.x
        y_start = event.y
        self.canvas.create_rectangle(x_start,y_start,x_start+1,y_start+1,outline="red",tag="rect")
        self.canvas.create_text(x_start, y_start-10, text=str(cnt), fill='red', font=("courier", 18))

    #コールバック関数：タッチパッドから指を離したとき
    def Release(self, event):
        global x_end,y_end,cnt
        x_end = event.x
        y_end = event.y
        self.canvas.create_rectangle(x_start,y_start,x_end,y_end,outline="red")
        
        img = Image.open(self.filepath)
        img = img.resize((SIZE, SIZE))
        crop_img = img.crop((x_start,y_start,x_end,y_end))
        queryname = os.path.join(CROP_FOLDER, "{}.png".format(cnt))
        crop_img.save(queryname, quality=95)
        cnt = cnt + 1

    #コールバック関数：タッチパッド上で指を動かしている時
    def Motion(self, event):
        x_end = event.x
        y_end = event.y
        self.canvas.coords("rect",x_start,y_start,x_end,y_end)
        
    def change_bg_color(self, colors):
        for i, color_name in enumerate(colors):
            print(color_name[0][1])
            self.all_entries[i]["bg"] = str(color_name[0][1])
   
    def clear_canvas(self):
        global cnt
        cnt=1
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img_, anchor=tk.NW)
        for i in range(0, len(self.all_entries)):
            self.all_entries[i].delete(0,tk.END)
        self.setup()
        
    def pushed(self):
        images = glob.glob('crop_images/*.png')
        images.sort()
        os.system('python3 main.py')
        top1, top2, top3 = predict(str(images[0]))
        payload = {'text': 'top1:'+str(top1[0][1])+'\n'+'top2:'+str(top2[0][1])+'\n'+'top3:'+ str(top3[0][1])}
        requests.post(URL, data=json.dumps(payload))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img_, anchor=tk.NW)
        self.change_bg_color([top1, top2, top3])


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    root.mainloop()



    
