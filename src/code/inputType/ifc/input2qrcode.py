#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import ifcopenshell
from code.shared.BDNS_validation import BDNSValidator
from code.shared.qrcode_gen import make_qrc
import numpy as np
from string import Template
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



URL_BDNS = 'https://raw.githubusercontent.com/theodi/BDNS/master/BDNS_Abbreviations_Register.csv'


def get_qrcodegen(ifc_input, ouputfolder, bdns_flag):
    return IFCt2QRCODE(ifc_input, ouputfolder, bdns_flag)

class IFCt2QRCODE:

    def __init__(self,
                 ifc_input,
                 ouputfolder,
                 bdns_flag
                 ):

        self.ifc_input = ifc_input
        self.ouputfolder = ouputfolder
        self.BDNS_validation = bdns_flag



    def create_qrcode(self, row, boxsize):
        color_text = row['color_text']
        try:
            caption = row['asset_name']
        except:
            caption = row['abbreviation']+"-"+row['RevitTag']
        boxsize = boxsize

        print("Creating the qr code for %s"%caption)

        data = Template("""{
        "asset": {
            "guid": "ifc://$asset_guid",
            "name": "$asset_name"
            }
        }""")

        img = make_qrc(data.substitute(asset_guid=row['asset_guid'], asset_name=row['asset_name']), caption, boxsize,color_text)
        img.save(self.ouputfolder + "/%s.png" % caption)



    def start(self):

        # Read  in the BDNS naming abbreviation
        bdns_csv = pd.read_csv(URL_BDNS)
        bdns_abb = bdns_csv[['abbreviation', 'ifc_class']]

        # Read  in the ifc file
        f = ifcopenshell.open(self.ifc_input)
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


        if self.BDNS_validation :

            BDNSVal = BDNSValidator(res)

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
            res['color_text'] = np.where(res['asset_name'].isin(str_list), 'red', 'black')


            checkdup = BDNSVal.check_duplicates()
            if not checkdup.empty:
                print("Duplicate GUID are:")
                print(checkdup)
                print("-------------------")


        # Generate QR code
        if res.empty:
            print('None of the ifc classes matches the BDNS ones .....')
        else:
            res.apply(self.create_qrcode, boxsize=10, axis=1)




