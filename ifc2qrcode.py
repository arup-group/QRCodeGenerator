from pprint import pprint
import qrcode
from PIL import Image, ImageDraw, ImageFont
import tkinter
from tkinter import filedialog
import os
b=[]
c=[]

F=open("IFC Test asset_name.ifc")
lines = F.readlines()
for line in lines:
    if "#41" in line:
        x=line.split(",")
        y=line.split("(")
        z=y[1]
        a=z.split(",")

        b.append(a[0].strip("'"))


b = list(filter(None, b))
b.remove(b[0])
for line in lines:
    for i in range (0,len(b)):
        if b[i] in line:
            d=line.split(",")
            c.append(d[2])


for j in range (0, len(b)):
    qr=qrcode.make(b[j])
    width, height = qr.size
    bi=Image.new('RGBA', (width+10, height+(height//5)), 'white')
    bi.paste(qr, (5, 5, (width+5), (height+5)))
    caption=c[j]
    font= ImageFont.truetype("arial.ttf", 25)
    w,h = font.getsize(caption)
    draw=ImageDraw.Draw(bi)
    draw.text(((width-w)/2, (height+((height/5)-h)/2)), caption, font=font, fill='black')
    bi.save(b[j] + ".png")
    j+=1
    



