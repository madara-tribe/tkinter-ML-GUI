import tkinter as tk
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.master.title("add button")
        self.master.geometry('500x500')
        self.all_entries = []
        
        self.addboxButton = tk.Button(self.master, text='<Add raw>', fg="Red", command=self.addBox)
        self.addboxButton.pack()
        self.color_button = tk.Button(text='change bg color', command=self.change_bg_color)
        self.color_button.place(x=5, y=10)
    
    def addBox(self):
        if len(self.all_entries)>7:
            messagebox.showinfo(title='over space', message='you can not add row anymore')
        self.ent = tk.Entry(self.master, width=5)
        self.ent.place(x=30+((len(self.all_entries)+1)*50), y=60)
        self.all_entries.append(self.ent)
  
    def change_bg_color(self):
        for i, _ in enumerate(self.all_entries):
            if i % 2==0:
                self.all_entries[i]["bg"] = "red"
            else:
                self.all_entries[i]["bg"] =="green"  
  
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()

