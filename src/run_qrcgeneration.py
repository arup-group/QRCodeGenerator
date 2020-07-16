import importlib
from pyfiglet import Figlet
import argparse
from sys import argv, exit
import os

__author__ = "Francesco Anselmo, Anushan Kirupakaran, Annalisa Romano"
__copyright__ = "Copyright 2019, Francesco Anselmo"
__credits__ = ["Francesco Anselmo"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo, , Anushan Kirupakaran, Annalisa Romano"
__email__ = "francesco.anselmo@arup.com, anushan.kirupakaran@arup.com, annalisa.romano@arup.com"
__status__ = "Dev"



def show_title():
    """Show the program title
    """
    f1 = Figlet(font='standard')
    print(f1.renderText('QRCodeGen'))

def main():

    """Generate QR code from gsheet, ifc and csv files.
        Arguments:
            INPUT_TYPE {[string]} -- input type which can be gsheet, ifc or csv
            SPREADSHEET_ID {[string]} -- google spreadsheet ID
            SHEET_NAME {[string]} -- google spreadsheet worksheet
            GSHEET_CREDS {[string]} -- credential json file
            IFC_FILENAME {[string]} -- input IFC file name
            CSV_FILENAME {[string]} -- input CSV file name
            OUTPUT_FILENAME {[string]} -- output folder for the generated QR code
            BDNS_VAL_FLAG {[boolean]} -- data validation against the BDNS initiative
            VERBOSE {[boolean]} -- increase the verbosity level
        """

    # show_title()

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", default=True, help="increase the verbosity level")
    parser.add_argument("-t", "--inputtype", default=False, help="input type which can be gsheet, ifc or csv")
    parser.add_argument("-s", "--gsheetid", default=False, help="google spreadsheet ID")
    parser.add_argument("-w", "--worksheet", default="Sheet1", help="google spreadsheet worksheet")
    parser.add_argument("-j", "--credsfile", default=False, help="credential json file")
    parser.add_argument("-f", "--filename", default=False, help="input IFC or CSV file name")
    parser.add_argument("-o", "--output", default="output", help="output folder for the generated QR code")
    parser.add_argument("-b", "--bdnsflag", default=True, help="data validation against the BDNS initiative")

    args = parser.parse_args()

    INPUT_TYPE = args.inputtype
    INPUT_FILENAME = args.filename
    SPREADSHEET_ID = args.gsheetid
    WORKSHEET = args.worksheet
    CREDENTIAL_FILE_PATH = args.credsfile
    OUTFOLDER = args.output
    BDNS_VALIDATION = args.bdnsflag


    if args.verbose:
        print("Program arguments:")
        print(args)
        print()

    if not ((INPUT_TYPE=='gsheet') or (INPUT_TYPE=='ifc') or (INPUT_TYPE=='csv')):
        print('Please choose an input type between gsheet, ifc and csv')
        print('Invoke %s -h for further information.\n' % argv[0])
        exit(1)

    if not OUTFOLDER:
        OUTFOLDER = 'output'
        pwd = os.getcwd()
        print('Results have been saved here: %s' % (pwd+'/'+OUTFOLDER))

    if not os.path.exists(OUTFOLDER):
        os.mkdir(OUTFOLDER)



    input_module = importlib.import_module("code.inputType.%s.input2qrcode" %INPUT_TYPE)

    if INPUT_TYPE=='gsheet':
        inputfile = input_module.get_qrcodegen(SPREADSHEET_ID, WORKSHEET, CREDENTIAL_FILE_PATH, OUTFOLDER, BDNS_VALIDATION)
    elif INPUT_TYPE=='ifc':
        inputfile = input_module.get_qrcodegen(INPUT_FILENAME, OUTFOLDER, BDNS_VALIDATION)
    elif INPUT_TYPE=='csv':
        inputfile = input_module.get_qrcodegen(INPUT_FILENAME, OUTFOLDER, BDNS_VALIDATION)


    inputfile.start()


if __name__ == "__main__":
    main()