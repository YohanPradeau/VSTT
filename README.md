# Converter-json-csv-for-vue
A small python soft which can be used to parse json files to csv and csv to json. This tool is made to work for vue i18n.

"./converter.py -h" for help

Take 2 arguments : 
- source (optionnal : path to a source language file, mandatory for the json -> csv only)
- target (path to the file you want to parse)

example :
"converter.py source-language.json file-to-convert.json" will create a csv of this file in the ./convertedFiles/ of the converter.py directory with the following format :<br/>
| Parent (do not edit)  | Source language | Translation |
| ------------- | ------------- | ------------- |
| key | word | mot |


You can now translate in the csv directly. Once this is done, you can type "converter.py ./convertedFiles/file-to-convert.json.csv" and it will create in the ./convertedFiles/ folder a file-to-convert.json, ready to be used!
