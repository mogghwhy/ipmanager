import csv
from sys import argv

fieldnames = ['source_ip', 'dest_port', 'count']
key1 = fieldnames[0]
key2 = fieldnames[1]
valueKeys = ['count']
addKeys = ['addedDate']
updateKeys = ['updatedDate']

def readCsv(name, fieldnames):
    dictList = None
    with open(name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        dictList = list(reader)
    return dictList[1:]

def constructDataDict(dictlist, key1, key2, valueKeys):
    data = {}
    for item in dictlist:
        level1key = item[key1]
        level2key = item[key2]
        dataLevel1 = data.get(level1key)
        if dataLevel1 == None:
            data[level1key] = {}
            dataLevel1 = data[level1key]
            dataLevel1[level2key] = {}
            dataLevel2 = dataLevel1[level2key]
            for vk in valueKeys:
                dataLevel2[vk] = item[vk]
        else:
            dataLevel2 = dataLevel1.get(level2key)
            if dataLevel2 == None:
                dataLevel1[level2key] = {}
                dataLevel2 = dataLevel1[level2key]
                for vk in valueKeys:
                    dataLevel2[vk] = item[vk]
            else:
                for vk in valueKeys:
                    dataLevel2[vk] = item[vk]
    return data


def writeCsv(name, dictList, fieldnames, key1, key2):
    with open(name, 'w', newline='') as csvfile:        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for k1value in dictList:
            level1 = dictList[k1value]
            for k2value in level1:
                level2 = level1[k2value]                
                row = {key1: k1value, key2: k2value} | level2
                writer.writerow(row) 


if len(argv) == 3:
    input_file = argv[1]
    output_file = argv[2]
else:
    print("need to specify input and output file")


newitems = readCsv(name=input_file, fieldnames=fieldnames)
data = constructDataDict(newitems, key1=key1, key2=key2, valueKeys=valueKeys)
writeCsv(output_file, data, fieldnames=fieldnames, key1=key1, key2=key2)