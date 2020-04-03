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
	
	def write_to_file(self):
		json_utilities.json_write(self.output_path, self.relationships)

	def extract_relationships(self):
		#iterate through metadata json array
		for each db
	   	       for each collection/table:
	            columns = self._get_columns(db, table/collection)
	            for col in columns:
 			attributes_meeting_threshold = self._get_deterministic_attrs(db,table,col)
	# attributes_meeting_threshold
	if attributes_meeting_threshold.length == 0:
		# append/create a json file with  [..., {db, table, col, samples}]
	else:
		# cool

 	

	def _get_deterministic_attrs(self, db, table, col):
		 samples =  take X samples using db_utilities.sample_db_table_col(db, table/collection, colum/key)
 attribute_counts = self._find_attribute_counts(samples)
 attributes_meeting_threshold =self._find_threshold_attrs(attribute_counts,samples.length)
 return attributes_meeting_threshold
			
	def _get_remaining_attrs(self, db, table, col):
		#remaining columns → clustering algo.
for x in remaining_cols:
		

	def _find_attribute_counts(self,samples):
found_attrs = defaultdict(lambda: 0)
 for s in samples:
   			# sample_rules = rules.get_possible_keys(s)
	for k in sample_rules:
 	found_attrs[k] += 1
	## found_attrs = {
		Email: 20,
		Address: 9
	}
return found_attrs


	def _find_threshold_attrs(self, attr_counts, num_samples):
		met_threshold_attrs = []
		for key, val in attr_counts.items():
			If val/num_samples >= SOME_MAGIC_THRESHOLD:
				met_threshold_attrs.append(key)

		Return met_threshold_attrs
		

	def _get_columns(self, db, table):
		# if type === mysql, return tables array
		# if type === mongo, return db_utilites.get_mongo_keys(db, table)


	def _attribute_type(self, samples):
		naive_type_counts = {“numerical”: 0, “categorical”: 0} 
		for x in samples:
			try:
float(x)
naive_type_counts[“numerical”] += 1
except:
				naive_type_counts[“categorical”] += 1
return “numerical” if (naive_type_counts[“numerical”] > naive_type_counts[“categorical”]) else return “categorical”

	# run on remaining samples that weren’t assigned a defined category based on the rules
	def run_naive_clustering():
		pass #implement in separate modules, this will just use 

	def run_probabilistic_clustering():
		pass #will call sampling
