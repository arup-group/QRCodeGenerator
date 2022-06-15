#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from code.shared.BDNS_validation import BDNSValidator
from code.shared.qrcode_gen import make_qrc
import numpy as np
from string import Template
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


DICTFONT = { "small":5,
             "medium":10,
             "large":15
            }


URL_BDNS = 'https://raw.githubusercontent.com/theodi/BDNS/master/BDNS_Abbreviations_Register.csv'


def get_qrcodegen(csv_file, ouputfolder, bdns_flag, minifiedflag):
    return CSV2QRCODE(csv_file, ouputfolder, bdns_flag, minifiedflag)


class CSV2QRCODE:

    def __init__(self,
                 csv_file,
                 ouputfolder,
                 bdns_flag,
                 minifiedflag
                 ):

        self.csv_file = csv_file
        self.ouputfolder = ouputfolder
        self.BDNS_validation = bdns_flag
        self.minified_flag = minifiedflag


    def create_qrcode(self, row,dict_font):
    
        color_text = row['color_text']
        caption = row['asset_name']
        
        try:
            font = row['size']
            boxsize = font #dict_font[font]
        except:
            boxsize = 3
        print("Creating the " + ("minified " if self.minified_flag == True else "") + "qr code for %s"%caption)

        template_path = path.join(path.dirname(path.realpath(__file__)), '..', '..', '..', 'qrtemplates', ('csv_qr.' + ('min.' if self.minified_flag == True else '')) + 'template')
        #print('template_path: %s, %s, %s'  %(template_path, self.minified_flag, ('min.' if self.minified_flag == True else '')))
        with open(template_path) as f:
            data = Template(f.read())

        caption2 = row['bms_label'] 
        if caption2 == None or pd.isnull(caption2) :
            caption2 = '' 
        
        print('bms_label: %s' %(caption2))
        
        img = make_qrc(data.substitute(asset_guid=row['asset_guid'], asset_name=row['asset_name'], asset_site=row['asset_site']), caption, caption2, boxsize, color_text)
        img.save(self.ouputfolder + "/%s.png" % caption)


    def start(self):


        df = pd.read_csv(self.csv_file)

        bdns_csv = pd.read_csv(URL_BDNS)
        bdns_abb = bdns_csv[['asset_abbreviation', 'ifc_class']]


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



