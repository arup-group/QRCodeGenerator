import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import config.config_def as config
import os
from pyfiglet import Figlet
import re
import ifcopenshell
import ssl
import argparse
ssl._create_default_https_context = ssl._create_unverified_context


__copyright__ = "Copyright 2019, Francesco Anselmo"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo, , Anushan Kirupakaran, Annalisa Romano"
__email__ = "francesco.anselmo@arup.com, anushan.kirupakaran@arup.com, annalisa.romano@arup.com"
__status__ = "Dev"



IFC_FILE_PATH = config.IFC_FILE_PATH
SPREADSHEET_ID = config.SPREADSHEET_ID
WORKSHEET = config.WORKSHEET
CREDENTIAL_FILE_PATH = config.CREDENTIAL_FILE_PATH
OUTFOLDER = config.OUTFOLDER
URL_BDNS = config.URL_BDNS
BDNS_VALIDATION = config.BDNS_VALIDATION


if not os.path.exists(OUTFOLDER):
    os.mkdir(OUTFOLDER)


DICTFONT = { "small":5,
             "medium":10,
             "large":15
            }

SCOPES = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]



def createDFfromGS(spreadsheetID, worksheet, cred_file_path, scopes):

    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file_path, scopes)
    client = gspread.authorize(creds)
    sh = client.open_by_key(spreadsheetID)
    wks = sh.worksheet(worksheet)

    data = wks.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    return df


def createDFfromIFC(ifcfile, url):

    bdns_csv = pd.read_csv(url)
    bdns_abb = bdns_csv[['abbreviation', 'ifc_class']]

    # Read  in the ifc file
    f = ifcopenshell.open(ifcfile)
    products = f.by_type('IfcProduct')

    # Create a df with all ifc classes
    d_list = []
    for product in products:
        d_list.append({
            'ifc_class': product.is_a(),
            'asset_guid': product.GlobalId,
            'name': product.Name
        })
    d = pd.DataFrame(d_list)

    df = pd.merge(d, bdns_abb, how='left', on=['ifc_class']).dropna(subset=['abbreviation'])
    df['id'] = df['name'].astype(str).apply(lambda x: x.split(':')[-1])
    df['asset_name'] = df['abbreviation'] + '-' + df['id']
    return df


def create_qrcode(row,dict_font):
    caption = row['asset_name']
    try:
        font = row['size']
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
    bi.save(OUTFOLDER + "/%s.png" % caption)



def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText("QRCodeGen"))


def main():

    show_title()

    # df = createDFfromGS(SPREADSHEET_ID, WORKSHEET, CREDENTIAL_FILE_PATH, SCOPES)

    df = createDFfromIFC(IFC_FILE_PATH, URL_BDNS)


    if BDNS_VALIDATION:

        pat_guid_ifc = re.compile("[A-Za-z0-9_$]{22}$")
        pat_guid_hex = re.compile("([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$")
        print('The following devices fail the ID validation tests:')
        for row in df.iterrows():
            if not((pat_guid_hex.match(row[1]['asset_guid'])) or (pat_guid_ifc.match(row[1]['asset_guid']))):
                print(row[1]['asset_name'], row[1]['asset_guid'])
        print("_________________")

        pat_abb = re.compile("[A-Z]{2,6}-[0-9]{1,6}$")
        pat_prefix = re.compile("[A-Z]*-[A-Z]*-[A-Z0-9]*_[A-Z]{2,6}-[0-9]{1,6}$")
        print('The following devices fail the device role name validation tests:')
        for row in df.iterrows():
            if not ((pat_abb.match(row[1]['asset_name'])) or (pat_prefix.match(row[1]['asset_name']))):
                print(row[1]['asset_name'], row[1]['asset_guid'])
        print("_________________")


    if df.empty:
        print('Check your input file, the dataframe is empty ...')
    else:
        df.apply(create_qrcode, dict_font=DICTFONT, axis=1)



if __name__ == "__main__":
    main()