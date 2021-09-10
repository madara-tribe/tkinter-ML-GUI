import tkinter as tk
import os
from http_req import http_request
from PIL import Image, ImageTk, ImageOps, ImageDraw

URL = 'https://hooks.slack.com/services/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'

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        
        self.master.title("Tkinter test")
        self.master.geometry('840x840')
        
        btn = tk.Button(text='Enter', command=self.pushed)
        btn.pack()
        
        # Enter text box
        self.set_buttons()

    def set_buttons(self):
        self.clear_button = tk.Button(text='clear all', command=self.clear_all)
        self.clear_button.place(x=200, y=10)
        
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
       
        self.name_label = tk.Label(text='send name')
        self.name_label.place(x=5, y=570)
        
        self.name_txt = tk.Entry(width=20)
        self.name_txt.place(x=5, y=600)
        self.name_txt.config(fg='red')
        
        self.name_label = tk.Label(text='send label')
        self.name_label.place(x=5, y=630)
        
        self.label_txt = tk.Entry(width=20)
        self.label_txt.place(x=5, y=660)
        self.label_txt.config(fg='red')
        
        
    def send_message_to_url(self, name, label):
        text = 'name:'+str(name)+'\n'+'label:'+str(label)
        http_request(URL, text)
        self.name_txt.insert(tk.END, str(name))
        self.label_txt.insert(tk.END, str(label))
        
    def clear_all(self):
        self.name_txt.delete(0, tk.END)
        self.label_txt.delete(0, tk.END)
        
    def pushed(self):
        name_txt = self.textBox1.get()
        label_txt = self.textBox2.get()
        print("in the function =",name_txt, label_txt)
        self.textBox1.delete(0,tk.END)
        self.textBox2.delete(0,tk.END)
        print('name', name_txt)
        print('label', label_txt)
        ## HTTP request to URL
        self.send_message_to_url(name_txt, label_txt)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    root.mainloop()



    

