import csv
from sys import argv

fieldnames = ['source_ip', 'dest_port', 'count']
key1 = fieldnames[0]
key2 = fieldnames[1]
valueKeys = ['count']
updateKeys = ['addedDate', '']

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

if len(argv) == 2:
    filename = argv[1]
newitems = readCsv(name=filename, fieldnames=fieldnames)
data = constructDataDict(newitems, key1=key1, key2=key2, valueKeys=valueKeys)
print(data)