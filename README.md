# Senior-Design-Project

## Environment Setup
### Initial Dependencies
  - python (>= 3.7)
  - conda 4.7.12
  - pip (>= 19 for python 3.7)
  
### Creating Environment
`conda env create -f conda-environment.yml`

`pip install -r requirements.txt`

## Usage
Ensure your conda environment is activated: `conda activate senior-design-env` 

### Database Metadata Extraction
`cd pipeline && python main.py --fetch /absolute/path/to/db_configs.json /absolute/output_path/for/db_metadata.json`

### Relationship Discoverey Extraction
`cd pipeline && python main.py --extract /absolute/path/to/db_metadata.json /absolute/output_path/for/db_relationships.json`
