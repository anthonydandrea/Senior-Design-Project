import db_utilities
import json_utilities
Import rules
From collections import defaultdict
#*** metadata file: tables and their schemas


class Extractor:
    def __init__(self, m_path, r_path):
            self.metadata_path = m_path
            self.output_path = r_path
            self.metadata = json_utilities.json_read(m_path)
            self.relationships = []
    def extract_relationships(self):
            #iterate through metadata json array
            for each db in self.metadata:
                for each key :
                    columns = self._get_columns(db, table/collection)
                    for col in columns:
                attributes_meeting_threshold = self._get_deterministic_attrs(db,table,col)
        # attributes_meeting_threshold
        if attributes_meeting_threshold.length == 0:
            # append/create a json file with  [..., {db, table, col, samples}]
            self.write_to_file()
        else:
            # cool
            pass

        

    def _get_deterministic_attrs(self, db, table, col):
        #samples =  take X samples using db_utilities.sample_db_table_col(db, table/collection, colum/key)
        samples = db_utilities.sample_db_table_col(db, table, col)
        attribute_counts = self.find_attribute_counts(samples)
        attributes_meeting_threshold =self._find_threshold_attrs(attribute_counts,samples.length)

        return attributes_meeting_threshold

    def _find_attribute_counts(self,samples):
        found_attrs = defaultdict(lambda: 0)
        for s in samples:
            # sample_rules = rules.get_possible_keys(s)
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
