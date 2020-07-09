import pandas as pd
import numpy as np
import collections

def find_duplicates_map(data):
    dups = collections.defaultdict(list)
    for index, item in enumerate(data):
        dups[item].append(index)
    return dups

def filter_data(data, time):
    dups = find_duplicates_map(data)
    result = []
    for index, item in enumerate(data):
        repetitions = dups[item]
        if index-1 in repetitions or index+1 in repetitions:
            string = time[index] + "," + item
            result.append(string)
    return result

def filterCsv(raw_data_path, output_path):
    filtered = []
    with open(raw_data_path + '\\emotions.csv', 'r') as f:
        temp = [line.strip() for line in f]
        data = []
        time = []
        for index, item in enumerate(temp):
            arr = item.split(",")
            time.append(arr[0])
            data.append(arr[1])

        if len(time) == 1 and len(data) == 1:
            print("NO FACE DETECTED. COULD NOT CREATE FACIAL EXPRESSIONS GRAPH.")
            return False

        filtered = filter_data(data, time)
        f.flush()

    with open(output_path + '\\emotions.csv', 'w', newline='') as fd:
        fd.write("Time,Emotions\n")
        for s in filtered:
            fd.write(s+"\n")
        fd.flush()

    return True