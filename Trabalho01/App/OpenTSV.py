import csv
import re

with open("data.tsv", 'r',  encoding="iso-8859-1") as myfile:
    with open("data.csv", 'w') as csvfile:
        for line in myfile:
            fileContent = re.sub("\t", ",", line)
            csvfile.write(fileContent)
    print("Sucess")


with open("data.tsv", encoding="iso-8859-1") as file:
    tsv_file = csv.reader(file, delimiter="\t")
    for line in tsv_file:
        print(line)