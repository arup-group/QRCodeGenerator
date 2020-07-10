import re

class BDNSValidator():

    def __init__(self, df):
        self.df = df

    def validate_GUID(self):
        pat_guid_ifc = re.compile("[A-Za-z0-9_$]{22}$")
        pat_guid_hex = re.compile("([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$")
        fail_list = []
        for row in self.df.iterrows():
            if not ((pat_guid_hex.match(row[1]['asset_guid'])) or (pat_guid_ifc.match(row[1]['asset_guid']))):
                fail_list.append((row[1]['asset_name'], row[1]['asset_guid']))
        return fail_list


    def validate_DeviceName(self):
        pat_abb = re.compile("[A-Z]{2,6}-[0-9]{1,6}$")
        pat_prefix = re.compile("[A-Z]*-[A-Z]*-[A-Z0-9]*_[A-Z]{2,6}-[0-9]{1,6}$")
        fail_list = []
        for row in self.df.iterrows():
            if not ((pat_abb.match(row[1]['asset_name'])) or (pat_prefix.match(row[1]['asset_name']))):
                fail_list.append((row[1]['asset_name'], row[1]['asset_guid']))
        return fail_list


    def check_duplicates(self):
        dup_list=[]
        duplicateRowsDF = self.df[self.df.duplicated(['asset_guid'])]
        try:
            dup_list.append((duplicateRowsDF.values[0][1], duplicateRowsDF.values[0][0]))
        except:
            pass
        return dup_list


    def validate_abb(self):
        abb_list = []
        for row in self.df.iterrows():
            if not row[1]['asset_name'].split('-')[0] == row[1]['abbreviation']:
                abb_list.append(row[1]['asset_name'])
        return abb_list