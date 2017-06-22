#!/usr/bin/env python

import argparse
import json
import jsonschema
import os
import subprocess
import sys

def configure_parser():
	usage = "usage: validators/generic.py [options] file.json"
	description = 'Validate json report'
	parser = argparse.ArgumentParser(usage=usage, description=description)
	parser.add_argument("-s", "--schema",
						help="JSON schema file to be used as validator",
						required=True)
	parser.add_argument("file",
						help="JSON file to validate")
	return parser

def verify_args(args):
	if not os.path.isfile(args.file):
		print("File {} does not exists".format(args.file))
		sys.exit(1)
	else:
		if not args.file.endswith('json'):
			print("{} is not a valid target file. Only JSON files allowed".format(args.file))
			sys.exit(1)

	if not os.path.isfile(args.schema):
		print("Schema file {} does not exists".format(args.schema))
		sys.exit(1)
	else:
		if not args.schema.endswith('json'):
			print("{} is not a valid schema file. Only JSON files allowed".format(args.schema))
			sys.exit(1)

def get_parsed_arguments():
	parser = configure_parser()
	args = parser.parse_args()
	verify_args(args)
	return args

def load_json_schema(schema_file):
	return json.load(open(schema_file, 'r'))

def load_json_data(json_file):
	filename = os.path.abspath(json_file)
	return open(filename, 'r').read()

def validate(json_data, json_schema):
	jsonschema.validate(str(json_data), json_schema)


if __name__ == "__main__":
	args = get_parsed_arguments()
	json_schema = load_json_schema(args.schema)
	print("Using validator: {} - {}".format(args.schema, json_schema['title']))
	print("Verifing {}".format(args.file))
	json_data = load_json_data(args.file)
	validate(json_data, json_schema)
	print("JSON validation passed!")
