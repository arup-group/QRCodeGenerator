#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from code.shared.BDNS_validation import BDNSValidator
from code.shared.qrcode_gen import make_qrc
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



DICTFONT = { "small":5,
             "medium":10,
             "large":15
            }

SCOPES = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

URL_BDNS = 'https://raw.githubusercontent.com/theodi/BDNS/master/BDNS_Abbreviations_Register.csv'


def get_qrcodegen(spreadsheet_id, sheet, credentials_file_path, ouputfolder, bdns_flag):
    return GSheet2QRCODE(spreadsheet_id, sheet, credentials_file_path, ouputfolder, bdns_flag)


class GSheet2QRCODE:

    def __init__(self,
                 spreadsheet_id,
                 sheet,
                 credentials_file_path,
                 ouputfolder,
                 bdns_flag
                 ):

        self.spreadsheet_id = spreadsheet_id
        self.sheet = sheet
        self.creds = credentials_file_path
        self.ouputfolder = ouputfolder
        self.BDNS_validation = bdns_flag


    def create_qrcode(self, row,dict_font):
        color_text = row['color_text']
        caption = row['asset_name']
        try:
            font = row['boxsize']
            boxsize = dict_font[font]
        except:
            boxsize = 10
        print("Creating the qr code for %s"%caption)

        img = make_qrc(row['asset_guid'], caption, boxsize, color_text)
        img.save(self.ouputfolder + "/%s.png" % caption)


    def start(self):


        creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds, SCOPES)
        client = gspread.authorize(creds)
        sh = client.open_by_key(self.spreadsheet_id)
        wks = sh.worksheet(self.sheet)

        data = wks.get_all_values()
        headers = data.pop(0)
        df = pd.DataFrame(data, columns=headers)

        bdns_csv = pd.read_csv(URL_BDNS)
        bdns_abb = bdns_csv[['abbreviation', 'ifc_class']]


        if self.BDNS_validation:

            BDNSVal = BDNSValidator(df)

            print('The following devices fail the GUID validation tests:')
            failed_GUID = BDNSVal.validate_GUID()
            print("-------------------")

            print('The following devices fail the device role name validation tests:')
            failed_DeviceName = BDNSVal.validate_DeviceName()
            print("-------------------")

            print('The following devices fail to follow the BDNS abbreviation:')
            faild_abb = BDNSVal.validate_abb(bdns_csv)
            print("-------------------")

            str_list =  failed_GUID+failed_DeviceName+faild_abb
            df['color_text'] = np.where(df['asset_name'].isin(str_list), 'red', 'black')


            checkdup = BDNSVal.check_duplicates()
            if not checkdup.empty:
                print("Duplicate GUID are:")
                print(checkdup)
                print("-------------------")


        df.apply(self.create_qrcode, dict_font=DICTFONT, axis=1)



