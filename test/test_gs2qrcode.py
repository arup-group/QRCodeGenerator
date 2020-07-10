import sys
import os
parentdir = os.path.dirname(os.getcwd())
sys.path.append(parentdir)

from PIL import Image, ImageFont, ImageDraw
from pyzbar.pyzbar import decode
import unittest
import qrcode_gen
from BDNS_validation import BDNSValidator
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context




expected_QR = Image.open("./test_qrcode/AHU-1.png")
df = pd.DataFrame({'asset_name': ['AHU-1'], 'asset_guid': ['d3501378-dd50-47c5-ae26-806726e1b749-897']})



class TestQRCodeGenerator(unittest.TestCase):

    def setUp(self):

        self.BDNSValidator = BDNSValidator(df)


    def test_qrcodegen(self):
        img = qrcode_gen.make_qrc('d3501378-dd50-47c5-ae26-806726e1b749', 'AHU-1', 15)
        self.assertEqual(decode(img)[0], decode(expected_QR)[0])


    def test_validate_GUID(self):
        fail_list = self.BDNSValidator.validate_GUID()
        self.assertTrue(len(fail_list)>0)


    def test_validate_DeviceName(self):
        fail_list = self.BDNSValidator.validate_DeviceName()
        self.assertTrue(len(fail_list)==0)


if __name__ == '__main__':
    unittest.main()
