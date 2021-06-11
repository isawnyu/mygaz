
# Create gazetteer from list of placenames

The ```names2gaz``` command-line script is designed to take a list of placenames and turn them into a structured JSON file in which very similar names have been grouped together on the basis of conservative string cleanup (spaces, Unicode normalization forms) and comparison of lowercase versions from which punctuation and spacing have been stripped.

```bash
python scripts/names2gaz.py -h
usage: names2gaz.py [-h] [-l LOGLEVEL] [-v] [-w] [-e ENCODING] [-o OUTPUT] input

Covert a list of placenames to a simple gazetteer

positional arguments:
  input                 path to input file

optional arguments:
  -h, --help            show this help message and exit
  -l LOGLEVEL, --loglevel LOGLEVEL
                        desired logging level (case-insensitive string: DEBUG, INFO, WARNING, or ERROR (default: NOTSET)
  -v, --verbose         verbose output (logging level == INFO) (default: False)
  -w, --veryverbose     very verbose output (logging level == DEBUG) (default: False)
  -e ENCODING, --encoding ENCODING
                        text encoding (default: utf-8)
  -o OUTPUT, --output OUTPUT
                        output format (default: json)
```

To review the results on the command line, set the output format to "plain":

```bash
python scripts/names2gaz.py -o plain ~/placenames.txt
INFO:root:using default logging level: INFO
INFO:__main__:Parsing txt file with encoding=utf-8: /Users/paregorios/Documents/files/T/teigaz/demarc/placenames.txt
ERROR:__main__:Skipping entry "," because its key is a zero-length string.
alveritae: ["Alveritae"]
tripolitania: ["Tripolitania"]
eleusis: ["Eleusis"]
eporenses: ["Eporenses"]
suppenses: ["Suppenses"]
cirtenses: ["Cirtenses"]
tisibenenses: ["*Tisibenenses", "Tisiben[e]nses"]
doliche: ["Doliche"]
pyranthos: ["Pyranthos"]
kasturrenses: ["Kasturrenses"]
germanisuperior: ["Germani Superior"]
emeritaaugusta: ["Emerita Augusta"]
constanţa: ["Constanţa"]
thabborenses: ["Thabborenses"]
vicussidoniorum: ["Vicus Sidoniorum"]
thracia: ["Thracia"]
dobropoljci: ["Dobropoljci"]
thessalian: ["Thessalian"]
moesiainferior: ["Moesia (Inferior)", "Moesia Inferior"]
africa: ["Africa"]
dion: ["Dion"]
```
