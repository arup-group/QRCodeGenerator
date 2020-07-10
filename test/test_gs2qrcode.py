import sys
import os
parentdir = os.path.dirname(os.getcwd())
sys.path.append(parentdir)

from PIL import Image, ImageFont, ImageDraw
from pyzbar.pyzbar import decode
import unittest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import qrcode_gen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


SCOPES = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]



expected_QR = Image.open("./test_qrcode/AHU-1.png")


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

        img = qrcode_gen.make_qrc('d3501378-dd50-47c5-ae26-806726e1b749', 'AHU-1', 15)
        self.assertEqual(decode(img)[0], decode(expected_QR)[0])


    # def test_validate_GUID(self):




if __name__ == '__main__':
    unittest.main()
