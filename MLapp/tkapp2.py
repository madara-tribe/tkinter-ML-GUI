import tkinter as tk
import tkinter.ttk as ttk
import os
import requests
import json
from PIL import Image, ImageTk, ImageOps, ImageDraw
from paddleocr import main

# alia-app
#URL='https://hooks.slack.com/services/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'
# hagi
URL = 'https://hooks.slack.com/services/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'
SIZE=600
cnt = 1

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        
        self.master.title("Tkinter test")
        self.master.geometry('840x840')
        self.filepath = 'input1.jpg'
        self.output_filepath = 'output.png'
        
        # Enter text box
        self.set_buttons()
        self.create_widgets()
        self.master.bind("<ButtonPress-1>",self.Push)
        self.master.bind("<ButtonRelease-1>",self.Release)
        self.master.bind("<Button1-Motion>",self.Motion)

    def set_buttons(self):
        self.label1 = tk.Label(text='name')
        self.label1.place(x=5, y=140)
        self.textBox1 = tk.Entry(width=5)
        self.textBox1.place(x=5, y=170)

        self.label2 = tk.Label(text='label')
        self.label2.place(x=5, y=200)
        self.textBox2 = tk.Entry(width=5)
        self.textBox2.place(x=5, y=230)
        
        self.textBox1.focus_set()
        self.textBox2.focus_set()
        btn = tk.Button(text='Enter', command=self.pushed)
        btn.pack()
       
        self.txt = tk.Entry(width=30)
        self.txt.place(x=5, y=700)
        self.txt.config(fg='red')
        
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

    #コールバック関数：タッチパッドから指を離したとき
    def Release(self, event):
        global x_end,y_end,cnt
        x_end = event.x
        y_end = event.y
        self.canvas.create_rectangle(x_start,y_start,x_end,y_end,outline="red")
        img = Image.open(self.filepath)
        img = img.resize((SIZE, SIZE))
        img.crop((x_start,y_start,x_end,y_end)).save(f"ocr_images/{cnt}.png")
        cnt = cnt + 1

    #コールバック関数：タッチパッド上で指を動かしている時
    def Motion(self, event):
        x_end = event.x
        y_end = event.y
        self.canvas.coords("rect",x_start,y_start,x_end,y_end)
    
    def ocr_predict(self, name, label):
        os.system('python3 paddleocr.py --case server')
        in_text = main()
        payload = {'text': 'name:'+str(name)+'\n'+'label:'+str(label)+'\n'+str(in_text)}
        requests.post(URL, data=json.dumps(payload))
        self.txt.insert(tk.END, str(in_text))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img_, anchor=tk.NW)

    def change_radio(self):
        if self.vr.get() == 1:
            self.eraser_on = False
        else:
            self.eraser_on = True    
    
    def clear_canvas(self):
        self.canvas.create_image(0, 0, image=self.img_, anchor=tk.NW)
        self.txt.delete(0,tk.END)

    def pushed(self):
        name_txt = self.textBox1.get()
        label_txt = self.textBox2.get()
        print("in the function =",name_txt, label_txt)
        self.textBox1.delete(0,tk.END)
        self.textBox2.delete(0,tk.END)
        print('name', name_txt)
        print('label', label_txt)
        ## OCR detection
        self.ocr_predict(name_txt, label_txt)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    root.mainloop()



    
