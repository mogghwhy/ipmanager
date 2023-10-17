import csv

fieldnames = ['source_ip', 'dest_port', 'count']

def readCsv(name, fieldnames):
    with open(name, newline='') as csvfile:
        reader = csvfile.DictReader(csvfile, fieldnames=fieldnames)


