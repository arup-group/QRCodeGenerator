#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import config.config_def as config
import os
from pyfiglet import Figlet


__author__ = "Francesco Anselmo, Anushan Kirupakaran, Annalisa Romano"
__copyright__ = "Copyright 2019, Francesco Anselmo"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo, , Anushan Kirupakaran, Annalisa Romano"
__email__ = "francesco.anselmo@arup.com, anushan.kirupakaran@arup.com, annalisa.romano@arup.com"
__status__ = "Dev"



SPREADSHEET_ID = config.SPREADSHEET_ID
WORKSHEET = config.WORKSHEET
CREDENTIAL_FILE_PATH = config.CREDENTIAL_FILE_PATH
OUTFOLDER_GS = config.OUTFOLDER_GS

if not os.path.exists(OUTFOLDER_GS):
    os.mkdir(OUTFOLDER_GS)


DICTFONT = { "small":5,
             "medium":10,
             "large":15
            }

SCOPES = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]



def create_qrcode(row,dict_font):
    font = row['size']
    caption = row['asset_name']
    try:
        boxsize = dict_font[font]
    except:
        boxsize = 10

    print("Creating the qr code for %s"%caption)
    qr = qrcode.make(row['asset_guid'], box_size=boxsize)
    width, height = qr.size
    bi = Image.new('RGBA', (width + 10, height + (height // 5)), 'white')
    bi.paste(qr, (5, 5, (width + 5), (height + 5)))

    Imfont = ImageFont.load_default()
    w, h = Imfont.getsize(caption)
    draw = ImageDraw.Draw(bi)
    draw.text(((width - w) / 2, (height + ((height / 5) - h) / 2)), caption, font=Imfont, fill='black')
    bi.save(OUTFOLDER_GS + "/%s.png" % caption)


def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText('GSheet2QRcode'))


def main():

    show_title()

    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE_PATH, SCOPES)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SPREADSHEET_ID)
    wks = sh.worksheet(WORKSHEET)

    data = wks.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)

    df.apply(create_qrcode, dict_font=DICTFONT, axis=1)

    print()


if __name__ == "__main__":
    main()

