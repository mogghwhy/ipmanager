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
    for source_key1 in sourceDataDict:
        update_level1 = updateDataDict.get(source_key1)
        if update_level1 == None:
            updateDataDict[source_key1] = sourceDataDict[source_key1]
            update_level1 = updateDataDict[source_key1]
            for k2 in update_level1:
                for ak in addKeys:
                    update_level1[k2][ak] = datetime.datetime.now(tz=datetime.timezone.utc)
                for uk in updateKeys:
                    update_level1[k2][uk] = datetime.datetime.now(tz=datetime.timezone.utc)
        else:
            pass
            source_level1 = sourceDataDict[source_key1]
            for source_key2 in source_level1:                
                update_level2 = update_level1.get(source_key2)
                if update_level2 == None:
                    update_level1[source_key2] = source_level1[source_key2]
                    update_level2 = update_level1[source_key2]                    
                    for ak in addKeys:
                        update_level2[ak] = datetime.datetime.now(tz=datetime.timezone.utc)
                        for uk in updateKeys:
                            update_level2[uk] = datetime.datetime.now(tz=datetime.timezone.utc)
                else:
                    for update_key2 in updateKeys:
                        for compare_key in compareKeys:
                            update_value = update_level2[compare_key]
                            source_value = source_level1[source_key2][compare_key]
                            if source_value != update_value:
                                print(f'update_key2 {update_key2}')
                                print(f'update_value {update_value}, source_value {source_value}')
                                update_level2[compare_key] = source_value
                                update_level2[update_key2] = datetime.datetime.now(tz=datetime.timezone.utc)


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
updateDataDict(sourceDataDict=input_data, updateDataDict=update_data, addKeys=update_config['addKeys'], updateKeys=update_config['updateKeys'], compareKeys=update_config['compareKeys'])
writeCsv(update_file, update_data, fieldnames=update_config['fieldnames'], key1=update_config['key1'], key2=update_config['key2'])