#!/usr/bin/env python

import logging
import time

import numpy as np

from hmmlearn import hmm
from scipy import *
from sklearn.externals import joblib

import script_recognition.repository.global_constants
import script_recognition.repository.global_values as GB
from script_recognition.repository.global_values import get_data

logging.basicConfig(filename= "logs\\hmm.log")


def train_hmm_model():
    language_labels = ["hindi", "english"]

    data_partition = "train"
    data_source = "Original"
    level = "Word"

    language_hmm_dictionary = {}

    model_time = time.strftime("%d_%m_%H_%M")
    for one_language in language_labels:

        print ("\n" + one_language)

        global_feature_values, global_label_values, global_lengths = \
            get_data([one_language], data_partition, level, data_source)

        best_hmm = None
        best_score = -np.inf
        for train_attempt in range(script_recognition.repository.global_constants.HMM_TRAIN_ATTEMPTS):

            print ("Train Attempt : " + str(train_attempt))

            model_attempt = hmm.GaussianHMM(n_components=10, covariance_type="full", n_iter=10, verbose=True)
            try:
                model_attempt.fit(global_feature_values, global_lengths)
                model_score = model_attempt.score(global_feature_values, global_lengths)
            except Exception as e:

                print("First Failure")

                logging.error(e)
                model_attempt = hmm.GaussianHMM(n_components=10, covariance_type="full", n_iter=10, verbose=True)
                try:
                    model_attempt.fit(global_feature_values, global_lengths)
                    model_score = model_attempt.score(global_feature_values, global_lengths)
                except Exception as e:
                    print("Second Failure")

                    logging.error(e)
                    continue

            if model_score > best_score:
                best_score = model_score
                best_hmm = model_attempt

        if best_hmm == None:
            raise Exception("exceptions must have occured, no model attempt converged")

        language_hmm_dictionary[one_language] = best_hmm
        joblib.dump(best_hmm, GB.get_filename(level, [one_language], data_partition, data_source, "HMM", model_time))

    data_partition = "train"
    data_source = "Original"
    level = "Word"
    calculate_hmm_prediction_accuracy(data_partition, data_source, [language_hmm_dictionary], language_labels, level)

    # data_partition = "test"
    # data_source = "Original"
    # level = "Char"
    # calculate_accuracy(data_partition, data_source, [language_hmm_dictionary], language_labels, level)

    data_partition = "test"
    data_source = "Original"
    level = "Word"
    calculate_hmm_prediction_accuracy(data_partition, data_source, [language_hmm_dictionary], language_labels, level)

    # data_partition = "test"
    # data_source = "strokeRecov"
    # level = "Char"
    # calculate_accuracy(data_partition, data_source, [language_hmm_dictionary], language_labels, level)

    data_partition = "test"
    data_source = "strokeRecov"
    level = "Word"
    calculate_hmm_prediction_accuracy(data_partition, data_source, [language_hmm_dictionary], language_labels, level)

    print("Done")


def calculate_hmm_prediction_accuracy(data_partition, data_source, language_hmm_dictionary_list, language_labels, level):

    logging.error(data_partition + "_" + level + "_" + data_source)

    language_accuracy_list = []

    for one_language in language_labels:
        global_feature_values, global_label_values, global_lengths = \
            get_data([one_language], data_partition, level, data_source)

        ends = np.cumsum(global_lengths)
        start = ends - np.array(global_lengths)

        for hmm_index, language_hmm_dictionary in enumerate(language_hmm_dictionary_list):
            in_correct_pred = 0

            for index in range(len(global_lengths)):
                pred_array = global_feature_values[start[index]:ends[index]]
                language_hmm = language_hmm_dictionary[one_language]
                label_prob = language_hmm.score(pred_array)

                for language in language_hmm_dictionary:
                    if language == one_language:
                        continue

                    model_prob = language_hmm_dictionary[language].score(pred_array)
                    if model_prob > label_prob:
                        in_correct_pred += 1
                        break
            logging.critical("\nLanguage : " + one_language)
            logging.critical("\nIndex : " + str(hmm_index))

            logging.critical("Total : " + str(len(global_lengths)))

            correct_pred = len(global_lengths) - in_correct_pred
            logging.critical("Correct : " + str(correct_pred))

            accuracy = float(correct_pred) / float(len(global_lengths))
            logging.critical("Accuracy : " + str(accuracy))

            language_accuracy_list.append(accuracy)

    logging.critical("Overall Accuracy : " + str(np.array(language_accuracy_list).mean()))


if __name__ == '__main__':
    train_hmm_model()
