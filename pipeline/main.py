
import os
import sys
from pathlib import Path
# filename = 
# print(filename)
path = os.getcwd()
sys.path.insert(0,str(Path('../Rules_data').resolve()))
sys.path.insert(0,str(Path('../files').resolve()))
# print(sys.path)
import js_utilities as jsutil
from extract import Extractor
from fetch import Fetcher
import argparse

# print(path)
# print(sys.path)
# path = os.path.split(path)[0]

# print(sys.path)

# exit()


parser = argparse.ArgumentParser(description="Relationship Discovery Tool")
parser.add_argument(
    "--fetch",
    nargs=2,
    metavar=("DB_CONFIGS_PATH", "METADATA_OUTPUT_PATH"),
    help="Fetch database metadata and write to file",
)
parser.add_argument(
    "--extract",
    nargs=2,
    metavar=("METADATA_INPUT_PATH", "RELTAIONSHIPS_OUTPUT_PATH"),
    help="Read database metadata, perform relationship discovery, and write to file",
)
parser.add_argument(
    "--gui",
    nargs=1,
    metavar=("RELATIONSHIPS_INPUT_PATH"),
    help="Start local server to display visualization of discovered relationships",
)


def fetch(input_path, output_path):
    fetcher = Fetcher(input_path, output_path)
    fetcher.fetch()
    fetcher.write_to_file()


def extract(input_path, output_path):
    extractor = Extractor(input_path, output_path)
    extractor.extract_relationships()
    extractor.write_to_file()


def gui(input_path):
    jsutil.js_write("./data.js", input_path)
    #server = Server(input_path)
    # server.start()


def parse_arguments():
    args = parser.parse_args()
    print(args)

    if args.fetch:
        fetch(args.fetch[0], args.fetch[1])

    if args.extract:
        extract(args.extract[0], args.extract[1])

    if args.gui:
        gui(args.gui[0])


if __name__ == "__main__":
    parse_arguments()
