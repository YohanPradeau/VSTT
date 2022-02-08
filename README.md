# Converter-xlf-csv-for-symfony
A small python soft which can be used to parse xlf files to csv and csv to xlf. This tool is made to work for symfony.

"./converter.py -h" for help

Take 3 parameters : 
- file (path to the file you want to parse)
- source (original language)
- target (targeted language

example :
"converter.py file-to-convert.en.xlf en fr" will create a csv of this file in the ./convertedFiles/ of the converter.py directory.
You can now translate in the csv directly, for ease of work it will replace every standard missing translations ("__word" in symfony) to \<missing translation> so you can simply ctrl+f and search for every \<missing translation>. Once this is done, you can type :
"converter.py ./convertedFiles/file-to-convert.en.xlf.csv en fr" and it will create in the ./convertedFiles/ folder a file-to-convert.en.xlf, ready to be used!

Open source
