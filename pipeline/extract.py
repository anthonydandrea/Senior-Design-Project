import db_utilities
import json_utilities
from collections import defaultdict
import sys
import os
path = "/mnt/c/Users/Michael/Desktop/School/SD_Project/Repo/Senior-Design-Project/"

sys.path.append(os.path.join(path, 'rules_data'))
from hard_rules import * 
#*** metadata file: tables and their schemas
SOME_MAGIC_THRESHOLD = 0.0

class Extractor:
    def __init__(self, m_path, r_path):
            self.metadata_path = m_path
            self.output_path = r_path
            self.metadata = json_utilities.json_read(m_path)
            self.relationships = []
           
    def write_to_file(self):
        print(self.relationships, 'test')
        json_utilities.json_write(self.output_path, self.relationships)

    def extract_relationships(self):
            #iterate through metadata json array
            for  db in self.metadata:
                if 'tables' in db:
                    for table in db['tables']:
                        columns = self._get_columns(db,table)
                        for col in columns:
                            attributes_meeting_threshold = self._get_deterministic_attrs(db,table,col)
                        # attributes_meeting_threshold
                        if len(attributes_meeting_threshold) == 0:
                            # append/create a json file with  [..., {db, table, col, samples}]
                            self.write_to_file()
                        else:
                        # cool
                            print('cool')
                            pass
                else:
                    for table in db['collections']:
                        columns = self._get_columns(db,table)
                        for col in columns:
                            attributes_meeting_threshold = self._get_deterministic_attrs(db,table,col)
                        # attributes_meeting_threshold
                        if len(attributes_meeting_threshold) == 0:
                            # append/create a json file with  [..., {db, table, col, samples}]
                            self.write_to_file()
                        else:
                        # cool
                            pass                   

        

    def _get_deterministic_attrs(self, db, table, col):
        #samples =  take X samples using db_utilities.sample_db_table_col(db, table/collection, colum/key)
        # samples = db_utilities.sample_db_table_col(db, table, col)
        samples = ["Georgia", 'Kansas', 'New York', 'California']
        attribute_counts = self._find_attribute_counts(samples)
        attributes_meeting_threshold = self._find_threshold_attrs(attribute_counts,len(samples))
        print('meeting threshold', attributes_meeting_threshold)
        return attributes_meeting_threshold

    def _find_attribute_counts(self,samples):
        found_attrs = defaultdict(lambda: 0)
        for s in samples:
            sample_rules = get_possible_keys(s)
            for k in sample_rules:
                found_attrs[k] += 1
            # ## found_attrs = {
            #     Email: 20,
            #     Address: 9
            # }
        return found_attrs


    def _find_threshold_attrs(self, attr_counts, num_samples):
        met_threshold_attrs = []
        for key, val in attr_counts.items():
            if val/num_samples >= SOME_MAGIC_THRESHOLD:
                met_threshold_attrs.append(key)

        return met_threshold_attrs

    def _get_columns(self, db, table):
		# if type === mysql, return tables array

        if db['type'] == 'mysql':
            return db['tables'][table]
		# if type === mongo, return db_utilites.get_mongo_keys(db, table)
        elif db['type'] == 'mongo':
            return  db['collections']
     
    def _attribute_type(self, samples):
        naive_type_counts = {'numerical': 0, 'categorical': 0} 
        for x in samples:
            try:
                float(x)
                naive_type_counts['numerical'] += 1
            except:
                naive_type_counts['categorical'] += 1

        return 'numerical' if (naive_type_counts['numerical'] > naive_type_counts['categorical']) else  'categorical'




pathr = os.path.join(path, 'files/tset.json')
pathm = os.path.join(path, 'files/db_metadata.json') 
x = Extractor(pathm, pathr)
x.extract_relationships()


