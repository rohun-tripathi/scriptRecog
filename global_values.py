import csv
import time
from collections import Counter

import numpy as np
from numpy.core.multiarray import array

import script_recognition.repository.compile_data_from_source as LE

def get_numeric_label(labelName):
    if labelName == "hindi":
        return 0
    elif labelName == "english":
        return 1
    elif labelName == "bangla":
        return 2


def most_common(prediction_list):
    return Counter(prediction_list).most_common()[0][0]


def get_filename(level, labels, function, dataSource, keyword, record_time=time.strftime("%d_%m_%H_%M")):
    label_string = "_".join([keyword] + labels + [level, function, dataSource])
    return "model\\" + label_string + "_" + record_time + ".json"


def export_matlab_data(data_source, language_input, label, length_raw_values, level, data_partition):
    ends = np.cumsum(length_raw_values)
    start = ends - np.array(length_raw_values)
    data = []
    for index in range(len(length_raw_values)):
        flattened = []
        for row in language_input[start[index]:ends[index]]:
            flattened.extend(row[0:2])
            flattened.append(row[2] + 1)
        data.append(flattened)

    matlab_file_name = "matlab_data\\" + label + "_" + data_partition + "_" + level + "_" + data_source
    with open(matlab_file_name.lower() + ".csv", "w", newline="") as m_data:
        csv.writer(m_data).writerows(data)


def get_data(labels, partition, level, data_source):
    seqDims = []
    seqLengths = []
    targetStrings = []
    wordTargetStrings = []
    seqTags = []
    inputs = []

    feature_values = []
    label_values = []
    lengths = []

    for label in labels:
        inputlanguage = []
        inputMeans, inputStds, a, labels_raw_values, length_raw_values = LE.main(partition, seqDims, seqLengths,
                                                                                 targetStrings,
                                                                                 wordTargetStrings, seqTags,
                                                                                 inputlanguage, label, level,
                                                                                 data_source, False)

        inputMeans = array([inputMeans[0], inputMeans[1], 0])
        inputStds = array([inputStds[0], inputStds[1], 1])

        inputlanguage = ((array(inputlanguage) - inputMeans) / inputStds).tolist()
        inputs.extend(inputlanguage)
        feature_values.extend(inputlanguage)
        label_values.extend(labels_raw_values)
        lengths.extend(length_raw_values)

    return feature_values, label_values, lengths