import csv
import json
from sys import argv
import datetime


def readConfig(file):
    with open(file, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)            
    return json_data    


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


def updateDataDict(sourceDataDict, updateDataDict, addKeys, updateKeys, compareKeys):
    for key1 in sourceDataDict:
        level1 = updateDataDict.get(key1)
        if level1 == None:
            updateDataDict[key1] = sourceDataDict[key1]
            level1 = updateDataDict[key1]
            for k2 in level1:
                for ak in addKeys:
                    level1[k2][ak] = datetime.datetime.now(tz=datetime.timezone.utc)
                for uk in updateKeys:
                    level1[k2][uk] = datetime.datetime.now(tz=datetime.timezone.utc)
        else:
            pass
            # level1 not None, but level2 key does not exist
            
            # for key2 in level1:
            #     print(f'key2 {key2}')
            #     level2 = level1.get(key2)
            #     print(level2)
            #     if level2 == None:
            #         pass
            #         print('not found')
            #     else:
            #         for ak in addKeys:
            #             if level2.get(ak) == '':
            #                 level2[ak] = datetime.datetime.now(tz=datetime.timezone.utc)
            #                 for uk in updateKeys:
            #                     if level2.get(uk) == '':
            #                         level2[uk] = datetime.datetime.now(tz=datetime.timezone.utc)
            #             else:
            #                 pass


if len(argv) == 5:
    input_config = argv[1]
    input_file = argv[2]
    update_config = argv[3]
    update_file = argv[4]
else:
    print("need to specify input and output files and their configs")


input_config = readConfig(input_config)
update_config = readConfig(update_config)
input_items = readCsv(name=input_file, fieldnames=input_config['fieldnames'])
input_data = constructDataDict(input_items, key1=input_config['key1'], key2=input_config['key2'], valueKeys=input_config['valueKeys'])
update_items = readCsv(name=update_file, fieldnames=update_config['fieldnames'])
update_data = constructDataDict(update_items, key1=update_config['key1'], key2=update_config['key2'], valueKeys=update_config['valueKeys'])
#print(update_data)
updateDataDict(sourceDataDict=input_data, updateDataDict=update_data, addKeys=update_config['addKeys'], updateKeys=update_config['updateKeys'], compareKeys=update_config['compareKeys'])
writeCsv(update_file, update_data, fieldnames=update_config['fieldnames'], key1=update_config['key1'], key2=update_config['key2'])