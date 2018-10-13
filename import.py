import sys 
import os
import csv
import json

if __name__ == '__main__':
    jsondict = {"visits":[], "captures":[]}
    logfd = open('game_log.tsv', 'rb')
    with open('game_log.tsv', 'rb') as logfd:
        spamreader = csv.reader(logfd, delimiter='	', quotechar='|')
        print "Processing……"

        for row in spamreader:
            if row[3] == "captured portal" and row[4] != "failed" and [row[1], row[2]] not in jsondict["captures"]:
                jsondict["captures"].append([row[1], row[2]])

        logfd.seek(0)
        for row in spamreader:
            if row[4] != "failed" and ((row[3].startswith("hacked") and row[3].endswith("portal")) or row[3].endswith("deployed")) and [row[1], row[2]] not in jsondict["visits"] and [row[1], row[2]] not in jsondict["captures"]:
                jsondict["visits"].append([row[1], row[2]])

        export_data = open("html/data.json", "w+")
        export_data.write(json.dumps(jsondict))
        export_data.close()

