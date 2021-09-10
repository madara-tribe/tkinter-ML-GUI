import tkinter as tk
import glob
from PIL import Image, ImageTk, ImageOps, ImageDraw
import shutil
import os

#範囲を指定して切り取った画像の保存場所："ocr_images"
#古い画像を削除するため、毎回フォルダ毎削除し、再度フォルダを作成

OCR_FOLDER='ocr_images'
if os.path.exists(OCR_FOLDER):
    shutil.rmtree(OCR_FOLDER)
os.makedirs(OCR_FOLDER)

SIZE=600

#コールバック関数：タッチパッドを押した時
def Push(event):
    global x_start,y_start
    x_start = event.x
    y_start = event.y
    canvas.create_rectangle(x_start,y_start,x_start+1,y_start+1,outline="red",tag="rect")

#コールバック関数：タッチパッドから指を離したとき
def Release(event):
    global x_end,y_end,cnt
    x_end = event.x
    y_end = event.y
    canvas.create_rectangle(x_start,y_start,x_end,y_end,outline="red")
    img = Image.open(pngs)
    img = img.resize((SIZE, SIZE))
    img.crop((x_start,y_start,x_end,y_end)).save(f"ocr_images/{cnt}.png")
    cnt = cnt + 1

#コールバック関数：タッチパッド上で指を動かしている時
def Motion(event):
    x_end = event.x
    y_end = event.y
    canvas.coords("rect",x_start,y_start,x_end,y_end)


#tkinterで画像の表示を行う
root = tk.Tk()
root.geometry('840x840')
root.title("image select")

#OCRを行いたい、未処理の画像の保存場所："images"
pngs = 'images/dog2.png'
img1 = Image.open(pngs)
img1 = img1.resize((SIZE, SIZE))

#指定範囲した画像に名前をつける番号：cnt
cnt = 1

canvas = tk.Canvas(width=SIZE,height=SIZE,bg="black")
gazou = ImageTk.PhotoImage(img1)
canvas.create_image(0, 0, image=gazou, anchor=tk.NW)
canvas.pack()

#コールバック関数の設定
root.bind("<ButtonPress-1>",Push)
root.bind("<ButtonRelease-1>",Release)
root.bind("<Button1-Motion>",Motion)
root.mainloop()
