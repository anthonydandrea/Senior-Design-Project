import db_utilities
Import utilities

class Fetcher:
	def __init__(self, c_path, m_path):
		self.DBConnector = DBConnector()
		self.config_path = c_path
		self.output_path = m_path

	def fetch(self):
schemas = []
		# read the config
		# iterate through dbs in config
		for db in config:
schemas.append(db_utilities.get_db_metadata(db))
		
		self.schemas = self._format_schemas(schemas)

	def _format_schemas(self, raw_schemas)
		# do some formatting
		# return new schema
	
def write_to_file(self):
		# save self.schemas to self.output_path
		utilities.json_write(self.output_path, self.schemas)
