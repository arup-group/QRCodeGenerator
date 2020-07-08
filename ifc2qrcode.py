#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import config.config_def as config
import os
from pyfiglet import Figlet
import ifcopenshell
import ssl

ssl._create_default_https_context = ssl._create_unverified_context



__author__ = "Francesco Anselmo, Anushan Kirupakaran, Annalisa Romano"
__copyright__ = "Copyright 2019, Francesco Anselmo"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo, , Anushan Kirupakaran, Annalisa Romano"
__email__ = "francesco.anselmo@arup.com, anushan.kirupakaran@arup.com, annalisa.romano@arup.com"
__status__ = "Dev"



IFC_FILE_PATH = config.IFC_FILE_PATH
OUTFOLDER_IFC = config.OUTFOLDER_IFC
URL_BDNS = config.URL_BDNS
DEBUG = False


if not os.path.exists(OUTFOLDER_IFC):
    os.mkdir(OUTFOLDER_IFC)


def create_qrcode(row,boxsize):

    caption = row['abbreviation']+'-'+row['id']
    boxsize = boxsize

    print("Creating the qr code for %s"%caption)
    qr = qrcode.make(row['asset_guid'], box_size=boxsize)
    width, height = qr.size
    bi = Image.new('RGBA', (width + 10, height + (height // 5)), 'white')
    bi.paste(qr, (5, 5, (width + 5), (height + 5)))

    Imfont = ImageFont.load_default()
    w, h = Imfont.getsize(caption)
    draw = ImageDraw.Draw(bi)
    draw.text(((width - w) / 2, (height + ((height / 5) - h) / 2)), caption, font=Imfont, fill='black')
    bi.save(OUTFOLDER_IFC + "/%s.png" % caption)


def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText('ifc2QRcode'))



def main():

    show_title()

    # Read  in the BDNS naming abbreviation
    bdns_csv = pd.read_csv(URL_BDNS)
    bdns_abb = bdns_csv[['abbreviation', 'ifc_class']]

    # Read  in the ifc file
    f = ifcopenshell.open(IFC_FILE_PATH)
    products = f.by_type('IfcProduct')

    # Create a df with all ifc classes
    d = []
    for product in products:
        d.append({
            'ifc_class': product.is_a(),
            'asset_guid': product.GlobalId,
            'name': product.Name
        })
    df = pd.DataFrame(d)


    res = pd.merge(df, bdns_abb, how='left', on=['ifc_class']).dropna(subset=['abbreviation'])
    res['id'] =  res['name'].astype(str).apply(lambda x: x.split(':')[-1])

    if DEBUG: print(res.head())

    if res.empty:
        print('None of the ifc classes matches the BDNS ones .....')
    else:
        res.apply(create_qrcode, boxsize=10, axis=1)


if __name__ == "__main__":
    main()

