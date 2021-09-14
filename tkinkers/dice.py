import tkinter as tk
import random

# ボタンが押された時の処理
def dice(event):
    # ランダムな整数を生成して、labelの内容を書き換える
    value["text"] = random.randint(1,6)


root = tk.Tk()
root.title("Dice.app")
root.geometry('200x150')

value = tk.Label(text="0",font=("",80))
value.pack(fill = 'x', padx=20, side = 'top')

Btn = tk.Button(text='サイコロをふる',width=10)
Btn.bind("<Button-1>", dice)
Btn.pack(fill = 'x', padx=20, side = 'top')


root.mainloop()
