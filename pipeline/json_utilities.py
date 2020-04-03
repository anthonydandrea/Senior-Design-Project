import json

def json_read(json_file_path):
	data = None
	with open(json_file_path) as json_file:
    		data = json.load(json_file)
	return data

def json_write(json_file_path, data):
	with open(json_file_path, 'w') as outfile:
    		json.dump(data, outfile)
