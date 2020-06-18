import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import qrcode
from PIL import Image, ImageDraw, ImageFont
import tkinter
from tkinter import filedialog
import os


scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds=ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client=gspread.authorize(creds)

sheet = client.open("Google sheet 1").sheet1

data=sheet.get_all_records()


for i in range (2, 5):
    boxsize=10
    row = sheet.row_values(i)
    if sheet.cell(i, 3).value=="small":
        boxsize=5
    if sheet.cell(i, 3).value=="medium":
        boxsize=10
    if sheet.cell(i, 3).value=="large":
        boxsize=15
    qr=qrcode.make(row, box_size=boxsize)
    width, height = qr.size
    bi=Image.new('RGBA', (width+10, height+(height//5)), 'white')
    bi.paste(qr, (5, 5, (width+5), (height+5)))
    caption=row[1]
    font= ImageFont.truetype("arial.ttf", 45)
    w,h = font.getsize(caption)
    draw=ImageDraw.Draw(bi)
    draw.text(((width-w)/2, (height+((height/5)-h)/2)), caption, font=font, fill='black')
    bi.save(row[1] + ".png")
    i+=1


