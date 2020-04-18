#!/usr/bin/python3
import json_utilities as json

def js_write(write_file_path, read_file_path):
	data = json.json_read(read_file_path)
	open(write_file_path, 'w').close()
	with open(write_file_path, 'a') as outfile:
		_format_javascript(outfile, data)

def _format_javascript(f, data):
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

#js_write("./jsonpractice.js", "./sample.json")