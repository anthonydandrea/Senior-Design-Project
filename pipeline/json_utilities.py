import json

def json_read(json_file_path):
	data = None
	with open(json_file_path) as json_file:
    		data = json.load(json_file)
	return data

def json_write(write_file_path, read_file_path):
	data = json_read(read_file_path)
	open(write_file_path, 'w').close()
	with open(write_file_path, 'a') as outfile:
		_format_json(outfile, data)
		#json.dump(data, outfile)

def _format_json(f, data):
	formatted_var = ["var nodes = [\n\t"]
	formatted_edges = ["var edges = [\n\t"]
	for entry in data:
		nextnode = "{id: %d, label: %s, group: %s},\n\t" %(entry["id"], entry["field_name"], entry["cluster"])
		formatted_var.append(nextnode)
		nextedge = "{from: %d, to: %d, label: %s},\n\t" %(entry["id"], entry["cluster"], str(entry["likelihood"]*100)+"%")
		formatted_edges.append(nextedge)
	formatted_var.append("];\n\n")
	formatted_edges.append("];\n\n")
	for x in formatted_var:
		f.write(x)
	for y in formatted_edges:
		f.write(y)
	return

#json_write("./jsonpractice.js", "./sample.json")