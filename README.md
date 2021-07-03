# DBS Projekt

## Dependencies

python3 with packages:

- pandas
- bokeh

Run to install all necessary dependencies:

```
$ pip install -r requirements.txt
```

## Build

Run commands from root of project directory:

### Sanitize

Sanitize CSV files located in ./csv_input directory
and save new CSV files to ./csv_output directory

```
$ python3 ./src/sanitize.py
```

### Export to Database

Read clean data from CSV files located in ./csv_output directory,
create schema and export that data to a sqlite database file
located in ./ressources directory

```
$ python3 ./src/export_to_db.py
```

### Visualize

Read data from sqlite database and create an interactive web page
displaying various charts using that data

```
bokeh serve ./src/visualize.py
```
