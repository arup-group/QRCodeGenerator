from PIL import Image, ImageFont, ImageDraw
import qrcode
from pyzbar.pyzbar import decode
import unittest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SCOPES = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]


GUID = 'd3501378-dd50-47c5-ae26-806726e1b749'
QRCODE = Image.open("./test_qrcode/AHU-1.png")
CAPTION = 'AHU-1'
SPREADSHEET_ID = '1O0-xqhXqkBIxdCF81NNyP5_yEINe75wXKkW12d54ApI'
WORKSHEET = 'Sheet1'
CREDENTIAL_FILE_PATH = '../config/creds.json'
URL_BDNS = 'https://raw.githubusercontent.com/theodi/BDNS/master/BDNS_Abbreviations_Register.csv'


class TestQRCodeGenerator(unittest.TestCase):

    def setUp(self):

        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE_PATH, SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = sheet.worksheet(WORKSHEET)
        except gspread.exceptions.WorksheetNotFound as e:
            pass

        bdns_csv = pd.read_csv(URL_BDNS)
        bdns_abb = bdns_csv[['abbreviation', 'ifc_class']]


    def test_qrcodegen(self):
        qr = qrcode.make(GUID, box_size=15)
        width, height = qr.size
        bi = Image.new('RGBA', (width + 10, height + (height // 5)), 'white')
        bi.paste(qr, (5, 5, (width + 5), (height + 5)))
        Imfont = ImageFont.load_default()
        w, h = Imfont.getsize(CAPTION)
        draw = ImageDraw.Draw(bi)
        draw.text(((width - w) / 2, (height + ((height / 5) - h) / 2)), CAPTION, font=Imfont, fill='black')

        self.assertEqual(decode(bi)[0], decode(QRCODE)[0])



if __name__ == '__main__':
    unittest.main()
