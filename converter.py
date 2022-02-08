from lxml import etree
import argparse
import csv
import codecs
import os
import sys
from xml.dom import minidom
from io import BytesIO
from pathlib import Path

#Arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("file", type=str, help="The file to convert")
argparser.add_argument("source", type=str, help="The original language of the website. Example : 'en' for english")
argparser.add_argument("target", type=str, help="The targeted language of the website. Example : 'fr' for french")

args = argparser.parse_args()
path = os.path.dirname(__file__)
fullpath = os.path.join(os.path.dirname(__file__), args.file)
file = args.file
filename = os.path.basename(args.file)
langOG = args.source
langTR = args.target
type = file[file.rfind('.') + 1::]


def csv_to_xlf(): #Function for the csv to xlf conversion
    # INITIALIZING XML FILE WITH ROOT IN PROPER NAMESPACE
    xliffAttribute = {'xmlns' : 'urn:oasis:names:tc:xliff:document:1.2', "version" : "1.2"}
    fileAttribute = {'source-language' : langOG, "target-language" : langTR, "datatype" : "plaintext", "original" : "file.ext"}
    toolAttribute = {'tool-id' : 'symfony', "tool-name" : "Symfony"}
    xliff = etree.Element("xliff", xliffAttribute)
    efile = etree.SubElement(xliff, "file", fileAttribute)
    header = etree.SubElement(efile, "header")
    tool = etree.SubElement(header, "tool", toolAttribute)
    body = etree.SubElement(efile, "body")
    try:
        # READING CSV FILE
        with open(fullpath) as f:
            reader = csv.reader(codecs.open(file, 'rU', 'ansi'))

            # WRITE INITIAL XML NODES
            for row in reader:
                if len(row) > 0:
                    if row[0] != "id (do not edit)":
                        transunitAttribute = {'id': row[0], 'resname':row[1]}
                        transunit = etree.SubElement(body, "trans-unit",transunitAttribute)
                        source = etree.SubElement(transunit, "source").text = row[2]
                        target = etree.SubElement(transunit, "target").text = row[3]
        f.close()
        tree = etree.ElementTree(xliff)
        xmlstr = minidom.parseString(etree.tostring(xliff)).toprettyxml(indent="   ", encoding='utf-8')
        with open(outputPath, "w") as f:
            f.write(xmlstr.decode('utf-8'))
            f.close()
    except Exception:
        print("File not found : "+fullpath)
    print("Done ! \nYou can check the file at the following path : "+ outputPath)

def xlf_to_csv(): #Function for the xlf to csv conversion
    try:
        tree = etree.parse(fullpath)
        root = tree.getroot()
        with open(path+"\convertedFiles\\"+filename+".csv", 'w', encoding="utf-8", newline='') as output:
            csvwriter = csv.writer(output)
            row = ["id (do not edit)", "resname (do not edit)", "source (do not edit)", "translation"]
            csvwriter.writerow(row)
            row = ["<missing translation>"]*4
            for transname in root[0][1]:
                row[0] = transname.attrib["id"]
                row[1] = transname.attrib["resname"]
                for elem in transname:
                    if row[2] == "<missing translation>":
                        row[2] = (elem.text)
                    else:
                        if elem.text == "__"+row[2]:
                            break
                        else:
                            row[3] = (elem.text)  
                csvwriter.writerow(row)
                row = ["<missing translation>"]*4
    except Exception:
        print("File not found : "+fullpath)
    print("Done ! \nYou can check the file at the following path : "+ path+"\convertedFiles\\"+filename+".csv")

#Prepare the folder for converted files
Path("./convertedFiles").mkdir(parents=True, exist_ok=True)


if type == "csv":
    outputPath=path+"\convertedFiles\\"+filename[:-4]
    fileExist = Path(outputPath).is_file()
    if fileExist:
        print("There is already a file at the output location with this exact same name and path ("+path+"\convertedFiles\\"+filename[:-4]+")")
        reply = str(input("Are you sure you wish to OVERWRITE it ? "+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            csv_to_xlf()
        elif reply[0] == 'n':
            print("Task canceled")
        else:
            print('Invalid input, task canceled.\nPlease be sure to answer with "y" or "n"')
    else:
        csv_to_xlf() 
elif type == "xlf":
    outputPath=path+"\convertedFiles\\"+filename+".csv"
    fileExist = Path(outputPath).is_file()
    if fileExist:
        print("There is already a file at the output location with this exact same name and path ("+path+"\convertedFiles\\"+filename[:-4]+")")
        reply = str(input("Are you sure you wish to OVERWRITE it ? "+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            xlf_to_csv()
        elif reply[0] == 'n':
            print("Task canceled")
        else:
            print('Invalid input, task canceled.\nPlease be sure to answer with "y" or "n"')
    else:
        xlf_to_csv()
    
else:
    print("Only CSV and XLF file type are accepted.")
    sys.exit(1)