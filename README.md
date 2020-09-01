# QR Code  Generator
A python program to generate QR codes from Google Sheets document, IFC and CSV files.

# Installation

### Pre-requisites

```
pip install -r requirements.txt
```
    
In order to be able to use IFC as input file you will need to install the python package **IfcOpenShell**. 
You can find the appropriate version of this module [here](http://ifcopenshell.org/python). 
Download the module and place the extracted archive in the site-packages folder of your Python distribution.

The QR code generato uses the `arial.ttf` font. You can download it [here](https://github.com/JotJunior/PHP-Boleto-ZF2/blob/master/public/assets/fonts/arial.ttf).

## Steps for generating the QR code from Google Sheets document, IFC and CSV files

1. Create the input file following the istruction below:
    
    * Google Sheets document and CSV file MUST contain at least these three columuns: **asset_name**, **asset_guid** and **size**, where `size` refers to the size in pixel of the QR code.
    By default a size of 10 is considered, however the following options have been also implemented `small:5, medium:10, large:15`. 
    An example of input file can be found [here](https://docs.google.com/spreadsheets/d/1O0-xqhXqkBIxdCF81NNyP5_yEINe75wXKkW12d54ApI/edit?usp=sharing).
    In order to run the script using the google sheet option, please be aware that you must have the crediatial json file and the right to edit the document;
    * In the IFC file, the asset name can be specified in the **Data** property definition. 
    If it's not provided, the name will be generated by following the BDNS naming convention (if possible) using the Revit Tag number. 

2.To launch the application move into the src folder 

   * To run the Django-based web app use the following command 


    python manage.py runserver
   
    
   * If you want to run the application locally use instead
    
    python run_qrcgeneration.py [args]


## Command line options

```
  ___  ____   ____          _       ____            
 / _ \|  _ \ / ___|___   __| | ___ / ___| ___ _ __  
| | | | |_) | |   / _ \ / _` |/ _ \ |  _ / _ \ '_ \ 
| |_| |  _ <| |__| (_) | (_| |  __/ |_| |  __/ | | |
 \__\_\_| \_\\____\___/ \__,_|\___|\____|\___|_| |_|
                                                    

usage: run_qrcgeneration.py [-h] [-v] [-t INPUTTYPE] [-s GSHEETID] [-w WORKSHEET] [-j CREDSFILE] [-f FILENAME] [-o OUTPUT] [-b BDNSFLAG]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase the verbosity level
  -t INPUTTYPE, --inputtype INPUTTYPE
                        input type which can be gsheet, ifc or csv
  -s GSHEETID, --gsheetid GSHEETID
                        google spreadsheet ID
  -w WORKSHEET, --worksheet WORKSHEET
                        google spreadsheet worksheet
  -j CREDSFILE, --credsfile CREDSFILE
                        credential json file
  -f FILENAME, --filename FILENAME
                        input IFC or CSV file name
  -o OUTPUT, --output OUTPUT
                        output folder for the generated QR code
  -b BDNSFLAG, --bdnsflag BDNSFLAG
                        data validation against the BDNS initiative

```      

## Validation against the BDNS initiative

By default `BDNSFLAG =True` and this allow to:

1. Check the device instance globally unique identifier (GUID) format and its uniqueness 
2. Check that the device name rule is fulfilled 
3. Check if the abbreviation used is compliant with the [BDSN Abbreviations Register](https://github.com/theodi/BDNS/blob/master/BDNS_Abbreviations_Register.csv)

These tests are in place for warning purpose.  If the device is not complaint the QR code label will appear in red.



## Reference

[BDNS initiative](https://github.com/theodi/BDNS)

    
 
