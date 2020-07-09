#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import config.config_def as config
import os
from pyfiglet import Figlet
import ifcopenshell
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



__author__ = "Francesco Anselmo, Anushan Kirupakaran, Annalisa Romano"
__copyright__ = "Copyright 2019, Francesco Anselmo"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo, Anushan Kirupakaran, Annalisa Romano"
__email__ = "francesco.anselmo@arup.com, anushan.kirupakaran@arup.com, annalisa.romano@arup.com"
__status__ = "Dev"



IFC_FILE_PATH = config.IFC_FILE_PATH
OUTFOLDER = config.OUTFOLDER
URL_BDNS = config.URL_BDNS
DEBUG = config.DEBUG
BDNS_VALIDATION =  config.BDNS_VALIDATION


if not os.path.exists(OUTFOLDER):
    os.mkdir(OUTFOLDER)


def create_qrcode(row,boxsize):
    try:
        caption = row['asset_name']
    except:
        caption = row['abbreviation']+"-"+row['RevitTag']
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
    bi.save(OUTFOLDER + "/%s.png" % caption)


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
        asset_name = ''
        definitions = product.IsDefinedBy
        for definition in definitions:
            if 'IfcRelDefinesByProperties' == definition.is_a():
                property_definition = definition.RelatingPropertyDefinition
                if 'Data' == property_definition.Name:
                    for par in property_definition.HasProperties:
                        if par.Name == 'asset_name':
                            asset_name = par.NominalValue[0]
        d.append({
            'ifc_class': product.is_a(),
            'asset_guid': product.GlobalId,
            'RevitName': product.Name,
            'asset_name': asset_name,

        })

    df = pd.DataFrame(d)
    res = pd.merge(df, bdns_abb, how='left', on=['ifc_class']).dropna(subset=['asset_name', 'abbreviation'])
    res['RevitTag'] = res['RevitName'].astype(str).apply(lambda x: x.split(':')[-1])

    if BDNS_VALIDATION:

        pat_guid_ifc = re.compile("[A-Za-z0-9_$]{22}$")
        pat_guid_hex = re.compile(
            "([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$")
        print('The following devices fail the GUID validation tests:')
        for row in res.iterrows():
            if not ((pat_guid_hex.match(row[1]['asset_guid'])) or (pat_guid_ifc.match(row[1]['asset_guid']))):
                print(row[1]['asset_name'], row[1]['asset_guid'])
        print("_________________")

        # Select all duplicate rows based on one column
        duplicateRowsDF = res[res.duplicated(['asset_guid'])]
        print("Duplicate GUID are:", duplicateRowsDF.values, sep='\n')
        print("_________________")

        pat_abb = re.compile("[A-Z]{2,6}-[0-9]{1,6}$")
        pat_prefix = re.compile("[A-Z]*-[A-Z]*-[A-Z0-9]*_[A-Z]{2,6}-[0-9]{1,6}$")
        print('The following devices fail the device role name validation tests:')
        for row in res.iterrows():
            if not ((pat_abb.match(row[1]['asset_name'])) or (pat_prefix.match(row[1]['asset_name']))):
                print(row[1]['asset_name'], row[1]['asset_guid'])
        print("----------------")

        print('The following devices fail to follow the BDNS abbreviation:')
        for row in res.iterrows():
            if not row[1]['asset_name'].split('-')[0] == row[1]['abbreviation']:
                print((row[1]['asset_name']))

    if res.empty:
        print('None of the ifc classes matches the BDNS ones .....')
    else:
        res.apply(create_qrcode, boxsize=10, axis=1)


if __name__ == "__main__":
    main()

