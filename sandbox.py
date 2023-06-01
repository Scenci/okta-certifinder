import os
import csv



def generateLink(file):
    with open(file,'r') as f:
        reader = csv.DictReader(f)
        firstNames = []
        lastNames = []
        for row in reader:
            firstNames.append(row["firstName"])
            lastNames.append(row["lastName"])

        for i in range(len(firstNames)):
            fn = firstNames[i]
            ln = lastNames[i]
            URL = "https://www.credly.com/users/"+fn+"-"+ln+"/badges?filter%5Buser_name%D="+fn+"%20"+ln+"&source=earner_directory"
            print(URL)
file_path = "export_test.csv"
generateLink(file_path)