# mygaz

A python package of command-line tools designed for creation and maintenance of simple, arbitrary gazetteers. The package uses a simple, ad hoc JSON file format as its default gazetter storage form and intends to provide mechanisms for exporting same to well-known target formats.

## **names2gaz**: create initial gazetteer from a list of placenames

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

The JSON output looks like this (note that spelling errors and typos in the original data are clearly not reconciled):

```json
{
    "abdera": {
        "names": [
            "Abdera"
        ]
    },
    "abdereitoi": {
        "names": [
            "Abdereitoi"
        ]
    },
    "achaia": {
        "names": [
            "Achaia?",
            "Achaia"
        ]
    },
    "aematini": {
        "names": [
            "[Ae]matini"
        ]
    },
    "africaproconsularis": {
        "names": [
            "Africa Proconsularis",
            "Africa proconsularis"
        ]
    },
    "agerdenthaliatis": {
        "names": [
            "ager Denthaliatis"
        ]
    },
    "agerdenthialitis": {
        "names": [
            "ager Denthialitis"
        ]
    },
    "ansienses": {
        "names": [
            "An[sienses?]",
            "Ansienses"
        ]
    }
}
```

To review the results on the command line in a more compact format, set the output format to "plain":

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
