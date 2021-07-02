from os import path
from os import makedirs as mkdir

project_root_dir = path.join(path.dirname(__file__), path.pardir) 
csv_input_dir = path.join(project_root_dir, 'csv_input') 
csv_output_dir = path.join(project_root_dir, 'csv_output') 
db_dir = path.join(project_root_dir, 'ressources') 

if not path.exists(csv_output_dir):
    mkdir(csv_output_dir)

if not path.exists(db_dir):
    mkdir(db_dir)

def csv_in_loc(fname):
    return path.abspath(path.join(csv_input_dir, fname)) 

def csv_out_loc(fname):
    return path.abspath(path.join(csv_output_dir, fname)) 

def db_loc(fname):
    return path.abspath(path.join(db_dir, fname))
