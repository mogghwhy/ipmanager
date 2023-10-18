import csv
import json
from sys import argv
import datetime


def read_config(file):
    with open(file, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)            
    return json_data    


def read_csv(name, fieldnames):
    dict_list = None
    with open(name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        dict_list = list(reader)
    return dict_list[1:]


def construct_data_dict(dict_list, key1, key2, value_keys):
    data = {}
    for item in dict_list:
        level1_key = item[key1]
        level2_key = item[key2]
        data_level1 = data.get(level1_key)
        if data_level1 == None:
            data[level1_key] = {}
            data_level1 = data[level1_key]
            data_level1[level2_key] = {}
            data_level2 = data_level1[level2_key]
            for vk in value_keys:
                data_level2[vk] = item[vk]
        else:
            data_level2 = data_level1.get(level2_key)
            if data_level2 == None:
                data_level1[level2_key] = {}
                data_level2 = data_level1[level2_key]
                for vk in value_keys:
                    data_level2[vk] = item[vk]
            else:
                for vk in value_keys:
                    data_level2[vk] = item[vk]
    return data


def write_csv(name, dict_list, field_names, key1, key2):
    with open(name, 'w+', newline='') as csvfile:        
        writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='excel')
        writer.writeheader()
        for k1_value in dict_list:
            level1 = dict_list[k1_value]
            for k2_value in level1:
                level2 = level1[k2_value]                
                row = {key1: k1_value, key2: k2_value} | level2
                writer.writerow(row) 


def update_data_dict(source_data_dict, update_data_dict, add_keys, update_keys, compare_keys):
    for source_key1 in source_data_dict:
        update_level1 = update_data_dict.get(source_key1)
        if update_level1 == None:
            update_data_dict[source_key1] = source_data_dict[source_key1]
            update_level1 = update_data_dict[source_key1]
            for k2 in update_level1:
                for ak in add_keys:
                    update_level1[k2][ak] = datetime.datetime.now(tz=datetime.timezone.utc)
                for uk in update_keys:
                    update_level1[k2][uk] = datetime.datetime.now(tz=datetime.timezone.utc)
        else:
            pass
            source_level1 = source_data_dict[source_key1]
            for source_key2 in source_level1:                
                update_level2 = update_level1.get(source_key2)
                if update_level2 == None:
                    update_level1[source_key2] = source_level1[source_key2]
                    update_level2 = update_level1[source_key2]                    
                    for ak in add_keys:
                        update_level2[ak] = datetime.datetime.now(tz=datetime.timezone.utc)
                        for uk in update_keys:
                            update_level2[uk] = datetime.datetime.now(tz=datetime.timezone.utc)
                else:
                    for update_key2 in update_keys:
                        for compare_key in compare_keys:
                            update_value = update_level2[compare_key]
                            source_value = source_level1[source_key2][compare_key]
                            if source_value != update_value:
                                update_level2[compare_key] = source_value
                                update_level2[update_key2] = datetime.datetime.now(tz=datetime.timezone.utc)


if len(argv) == 5:
    input_config = argv[1]
    input_file = argv[2]
    update_config = argv[3]
    update_file = argv[4]
else:
    print("need to specify input and output files and their configs")


input_config = read_config(input_config)
update_config = read_config(update_config)
input_items = read_csv(name=input_file, fieldnames=input_config['fieldnames'])
input_data = construct_data_dict(input_items, key1=input_config['key1'], key2=input_config['key2'], value_keys=input_config['valueKeys'])
update_items = read_csv(name=update_file, fieldnames=update_config['fieldnames'])
update_data = construct_data_dict(update_items, key1=update_config['key1'], key2=update_config['key2'], value_keys=update_config['valueKeys'])
update_data_dict(source_data_dict=input_data, update_data_dict=update_data, add_keys=update_config['addKeys'], update_keys=update_config['updateKeys'], compare_keys=update_config['compareKeys'])
write_csv(update_file, update_data, field_names=update_config['fieldnames'], key1=update_config['key1'], key2=update_config['key2'])