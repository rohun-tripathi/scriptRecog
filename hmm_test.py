import logging
logging.basicConfig(filename="logs\\hmm_accuracy_matrix.log", level=logging.INFO)

import glob
from sklearn.externals import joblib
import numpy as np
import re

from script_recognition.repository.hmm_model import calculate_hmm_prediction_accuracy
from script_recognition.repository.global_values import get_data


def load_and_test_hmm_char_combinations():
    file_list = glob.glob("model\\HMM" + "*Char*")

    english_models = []
    hindi_models = []

    for file_name in file_list:
        if "english" in file_name:
            english_models.append(file_name)

        if "hindi" in file_name:
            hindi_models.append(file_name)

    model_dict_list = []

    index = 0
    for english_hmm in english_models:
        for hindi_hmm in hindi_models:
            print(english_hmm + "__________" + hindi_hmm + "__________" + str(index))

            model_dict_list.append({"english" : joblib.load(english_hmm), "hindi" : joblib.load(hindi_hmm)})

            index += 1

    data_partition = "test"
    data_source = "strokeRecov"
    level = "Word"
    calculate_hmm_prediction_accuracy(data_partition, data_source, model_dict_list, ["hindi", "english"], level)


def load_hmm_result_matrix():
    file_list = glob.glob("model\\HMM" + "*Char*")

    english_models = []
    hindi_models = []

    english_object = []
    hindi_object = []

    for file_name in file_list:
        if "english" in file_name:
            english_models.append(file_name)
            english_object.append(joblib.load(file_name))


        if "hindi" in file_name:
            hindi_models.append(file_name)
            hindi_object.append(joblib.load(file_name))

    data_partition = "test"
    data_source = "Original"
    level = "Word"
    calculate_hmm_prediction_array(data_partition, data_source, level, english_object, hindi_object, english_models, hindi_models)


# TODO This function was not completed, hence never tested.
# The goal was to create a matrix form to find the optimal hindi-english HMM pairing.
def calculate_hmm_prediction_array(data_partition, data_source, level, hindi_list, english_list, english_models, hindi_models):

    logging.error(data_partition + "_" + level + "_" + data_source)

    prediction_dictionary = []
    entry_language = []

    for one_language in ["hindi", "english"]:
        global_feature_values, global_label_values, global_lengths = \
            get_data([one_language], data_partition, level, data_source)

        ends = np.cumsum(global_lengths)
        start = ends - np.array(global_lengths)

        for index in range(len(global_lengths)):
            pred_array = global_feature_values[start[index]:ends[index]]

            result_row = []
            for language_hmm in hindi_list + english_list:
                label_prob = language_hmm.score(pred_array)
                result_row.append(label_prob)

            entry_language.append(one_language)
            prediction_dictionary.append(result_row)

    model_result_dictionary = {}
    for hindi_index, hindi_model in hindi_list:
        for english_index, english_model in english_list:

            model_pair_correct = 0
            for language, row in zip(entry_language, prediction_dictionary):

                hindi_prob = row[hindi_index]
                english_prob = row[len(hindi_list) + english_index]

                if language == "hindi" and hindi_prob > english_prob:
                    model_pair_correct += 1
                elif language == "english" and english_prob > hindi_prob:
                    model_pair_correct += 1

            model_result_dictionary[english_models[english_index] + hindi_models[hindi_index]] = model_pair_correct


def calculate_best_accuracy_in_hmm_models():

    # TODO : put the data for just this model in the below named file
    n = open("archive\\extract_best_pair.txt", "r").read()

    # TODO : make sure this regex works for the file
    keyword = "\nCRITICAL:root:Accuracy : "
    regex = keyword + "\d*.\d*"

    entries = re.findall(regex, n)

    first = []
    second = []

    for index, entry in enumerate(entries):
        if index < len(entries) / 2:
            first.append(entry.strip(keyword))
        else:
            second.append(entry.strip(keyword))

    accuracies = []
    for a, b in zip(first, second):
        c = float(a)
        d = float(b)
        print(c, d, (c + d) / 2)
        accuracies.append((c + d) / 2)

    print(np.array(accuracies).max())


if __name__ == '__main__':
    calculate_best_accuracy_in_hmm_models()