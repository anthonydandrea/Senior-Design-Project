import sys
import os

# path = os.getcwd()
# print(path)
# print(sys.path)
# path = os.path.split(path)[0]
# sys.path.append(os.path.join(path, 'Rules_data'))
# print(sys.path)

from hard_rules import *
import db_utilities
import json_utilities
from collections import defaultdict

import random as rd

# *** metadata file: tables and their schemas
SOME_MAGIC_THRESHOLD = .8


class Extractor:
    def __init__(self, m_path, r_path):
        self.metadata_path = m_path
        self.output_path = r_path
        self.metadata = json_utilities.json_read(m_path)
        self.relationships = []

    def write_to_file(self):
        json_utilities.json_write(self.output_path, self.relationships)

    def add_to_relationships(self, att, db, table, col):
        self.relationships.append({
            "id": rd.random(),
            "field_name": col,
            "db": db,
            "table": table,
            "cluster": att[0],
            "likelihood": att[1]
        })

    def extract_relationships(self):
        # iterate through metadata json array
        for db in self.metadata:
            keyword = "tables" if db["type"] == "mysql" else "collections"
            for table in db[keyword]:
                columns = self._get_columns(db, table)
                for col in columns:
                    attributes_meeting_threshold = self._get_deterministic_attrs(
                        db, table, col)

                    print("attributes_meeting_threshold:",
                          attributes_meeting_threshold)

                    # if len(attributes_meeting_threshold) == 1:
                    #     # append/create a json file with  [..., {db, table, col, samples}]
                    #     self.add_to_relationships(
                    #         attributes_meeting_threshold[0], db, table, col)
                    # elif len(attributes_meeting_threshold) == 0:
                    #     # none attributes found
                    #     print('cool')
                    #     pass
                    # else:
                    #     # more than one found, unsure
                    #     pass

                    for attr in attributes_meeting_threshold:
                        self.add_to_relationships(attr, db, table, col)

    def _get_deterministic_attrs(self, db, table, col):
        # samples =  take X samples using db_utilities.sample_db_table_col(db, table/collection, colum/key)
        samples = db_utilities.sample_db_table_col(db, table, col)
        samples = list(map(lambda x: str(x[0]) if type(
            x) == type((1, 1)) else str(x), samples))
        print("Samples:", samples)
        # return []
        # samples = ["Georgia", 'Kansas', 'New York', 'California']
        attribute_counts = self._find_attribute_counts(samples)
        attributes_meeting_threshold = self._find_threshold_attrs(
            attribute_counts, len(samples))
        return attributes_meeting_threshold

    def _find_attribute_counts(self, samples):
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
            likelihood = val / num_samples
            if likelihood >= SOME_MAGIC_THRESHOLD:
                met_threshold_attrs.append((key, likelihood))

        return met_threshold_attrs

    def _get_columns(self, db, table):
        # if type === mysql, return tables array

        if db['type'] == 'mysql':
            return db['tables'][table]
            # if type === mongo, return db_utilites.get_mongo_keys(db, table)
        elif db['type'] == 'mongo':
            # return db['collections']
            keys = db_utilities.get_mongo_keys(db, table)
            # print("keys:", keys)
            return keys

    def _attribute_type(self, samples):
        naive_type_counts = {'numerical': 0, 'categorical': 0}
        for x in samples:
            try:
                float(x)
                naive_type_counts['numerical'] += 1
            except:
                naive_type_counts['categorical'] += 1

        return 'numerical' if (naive_type_counts['numerical'] > naive_type_counts['categorical']) else 'categorical'


# pathr = os.path.join(path, 'files/tset.json')
# pathm = os.path.join(path, 'files/db_metadata.json')
# x = Extractor(pathm, pathr)
# x.extract_relationships()
