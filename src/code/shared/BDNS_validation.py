import re

class BDNSValidator():

    def __init__(self, df):
        self.df = df

    def validate_GUID(self):
        d = self.df
        pat_guid_ifc = re.compile("[A-Za-z0-9_$]{22}$")
        pat_guid_hex = re.compile("([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$")
        fail_list = []
        for row in d.iterrows():
            if not ((pat_guid_hex.match(row[1]['asset_guid'])) or (pat_guid_ifc.match(row[1]['asset_guid']))):
                print(row[1]['asset_name'], row[1]['asset_guid'])
                fail_list.append(row[1]['asset_name'])
        return fail_list


    def validate_DeviceName(self):
        pat_abb = re.compile("[A-Z]{2,6}-[0-9]{1,6}$")
        pat_prefix = re.compile("[A-Z]*-[A-Z]*-[A-Z0-9]*_[A-Z]{2,6}-[0-9]{1,6}$")
        fail_list = []
        for row in self.df.iterrows():
            if not ((pat_abb.match(row[1]['asset_name'])) or (pat_prefix.match(row[1]['asset_name']))):
                print(row[1]['asset_name'], row[1]['asset_guid'])
                fail_list.append(row[1]['asset_name'])
        return fail_list


    def check_duplicates(self):
        duplicateGUID = self.df[self.df.duplicated(['asset_guid'], keep=False)]
        wrong_GUID = duplicateGUID[~duplicateGUID.duplicated(['asset_name'])]
        return wrong_GUID[['asset_guid', 'asset_name']]


    def validate_abb(self, bdns_csv):
        abb_list = []
        for row in self.df.iterrows():
            if '_' in row[1]['asset_name']:
                asset_name = row[1]['asset_name'].split('_')[-1]
            else:
                asset_name = row[1]['asset_name']

            if not bdns_csv['abbreviation'].str.contains(asset_name.split('-')[0]).any():
                print(row[1]['asset_name'], row[1]['asset_guid'])
                abb_list.append(row[1]['asset_name'])

        return abb_list