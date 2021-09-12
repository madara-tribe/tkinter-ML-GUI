import tkinter as tk
from tkinter import messagebox

bcnt=1
class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.master.title("add button")
        self.master.geometry('500x500')
        self.all_entries = []
        
        self.addboxButton = tk.Button(self.master, text='<Add raw>', fg="Red", command=self.addBox)
        self.addboxButton.pack()
        
    def addBox(self):
        global bcnt
        if bcnt>7:
            messagebox.showinfo(title='over space', message='you can not add row anymore')
        self.ent = tk.Entry(self.master, width=5)
        self.ent.place(x=30+(bcnt*50), y=30)
        self.all_entries.append(self.ent)
        bcnt += 1
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()

