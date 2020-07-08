#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import config.config_def as config
import os
from pyfiglet import Figlet
import ifcopenshell

from bs4 import BeautifulSoup
import requests


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

if not os.path.exists(OUTFOLDER_IFC):
    os.mkdir(OUTFOLDER_IFC)


def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText('ifc2QRcode'))


# url="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
#
# # Make a GET request to fetch the raw HTML content
# html_content = requests.get(url).text
#
# # Parse the html content
# soup = BeautifulSoup(html_content, "lxml")
# print(soup.prettify()) # print the parsed data of html

f = ifcopenshell.open(IFC_FILE_PATH)

products = f.by_type('IfcProduct')
for product in products:
    print(product.is_a())


# wall = f.by_type('IfcFlowTerminal')[0]
# print(wall.GlobalId)
# print(wall.Name)



# def main():
#
#     show_title()
#
#
#
# if __name__ == "__main__":
#     main()
#
