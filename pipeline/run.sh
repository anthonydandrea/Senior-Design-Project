FILES_DIR=$(pwd)/../files
python main.py --fetch $FILES_DIR/db_configs.json $FILES_DIR/db_metadata.json --extract $FILES_DIR/db_metadata.json $FILES_DIR/db_relationships.json --gui $FILES_DIR/db_relationships.json

