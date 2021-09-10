import tkinter as tk
import tkinter.ttk as ttk
import os
import requests
import json
from PIL import Image, ImageTk, ImageOps, ImageDraw
#from ocr import ocr_prediction

URL = 'https://hooks.slack.com/services/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'

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        
        self.master.title("Tkinter test")
        self.master.geometry('840x840')
        self.filepath = 'input.jpg'
        self.output_filepath = 'output.png'
        
        # Enter text box
        self.set_buttons()
        self.set_ptbox()
        self.create_widgets()
        self.create_canvas(self.master, self.filepath)

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
        self.txt.place(x=5, y=600)
        self.txt.config(fg='red')
        
    def set_ptbox(self):
        self.start_x = tk.StringVar()
        self.start_y = tk.StringVar()
        self.current_x = tk.StringVar()
        self.current_y = tk.StringVar()
        self.stop_x = tk.StringVar()
        self.stop_y = tk.StringVar()
        
        self.label_description = tk.Label(text='Mouse position')
        self.label_description.place(x=5, y=260)
        self.label_start_x = tk.Label(textvariable=self.start_x)
        self.label_start_x.place(x=5, y=280)
        self.label_start_y = tk.Label(textvariable=self.start_y)
        self.label_start_y.place(x=5, y=320)
        self.label_current_x = tk.Label(textvariable=self.current_x)
        self.label_current_x.place(x=5, y=360)
        self.label_current_y = tk.Label(textvariable=self.current_y)
        self.label_current_y.place(x=5, y=400)
        self.label_stop_x = tk.Label(textvariable=self.stop_x)
        self.label_stop_x.place(x=5, y=440)
        self.label_stop_y = tk.Label(textvariable=self.stop_y)
        self.label_stop_y.place(x=5, y=480)
        
    def create_widgets(self):
        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.eraser_on = False
        self.im = Image.new('RGB', (600, 600))
        self.draw = ImageDraw.Draw(self.im)
        
        self.vr = tk.IntVar()
        self.vr.set(1)
        self.write_radio = tk.Radiobutton(text='write', variable=self.vr, value=1, command=self.change_radio)
        self.write_radio.place(x=100, y=10)

        self.clear_button = tk.Button(text='clear all', command=self.clear_canvas)
        self.clear_button.place(x=200, y=10)

        self.save_button = tk.Button(text='save', command=self.save_canvas)
        self.save_button.place(x=290, y=10)
        
    def create_canvas(self, root, filepath):
        img = Image.open(filepath)
        img = img.resize((500, 500))
        img = ImageTk.PhotoImage(img)
        
        self.canvas = tk.Canvas(width=600, height=600)
        self.canvas.place(x=300, y=100)
        self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
        self.canvas.bind('<ButtonPress-1>', self.start_pickup)
        self.canvas.bind('<B1-Motion>', self.pickup_position)
        self.canvas.bind('<ButtonRelease-1>', self.stop_pickup)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        root.mainloop()
        
    def ocr_predict(self, name, label):
        os.system('python3 ocr.py')
        in_text = ocr_prediction()
        payload = {'text': 'name:'+str(name)+'\n'+'label:'+str(label)+'\n'+str(in_text)}
        requests.post(URL, data=json.dumps(payload))
        self.txt.insert(tk.END, str(in_text))
        self.canvas.delete("all")
        self.create_canvas(self.master, self.output_filepath)
        
    def clear_canvas(self):
        self.create_canvas(self.master, self.filepath)

    def save_canvas(self):
        self.canvas.postscript(file='out.ps', colormode='color')

    def change_radio(self):
        if self.vr.get() == 1:
            self.eraser_on = False
        else:
            self.eraser_on = True
   
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

    def start_pickup(self, event):
        self.start_x.set('x : ' + str(event.x))
        self.start_y.set('y : ' + str(event.y))
        self.stop_x.set('')
        self.stop_y.set('')
        print(event.x, event.y)
    
    def pickup_position(self, event):
        self.current_x.set('x : ' + str(event.x))
        self.current_y.set('y : ' + str(event.y))
        print(event.x, event.y)

    def stop_pickup(self, event):
        self.stop_x.set('x : ' + str(event.x))
        self.stop_y.set('y : ' + str(event.y))
        print(event.x, event.y)
    
    def reset(self, event):
        self.old_x, self.old_y = None, None

    def paint(self, event):
        if self.eraser_on:
            paint_color = 'white'
        else:
            paint_color = 'black'
        if self.old_x and self.old_y:
            self.canvas.create_rectangle(self.old_x, self.old_y, event.x, event.y, width=5.0, fill=paint_color)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=paint_color, width=5)
        
        self.old_x = event.x
        self.old_y = event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    root.mainloop()



    
