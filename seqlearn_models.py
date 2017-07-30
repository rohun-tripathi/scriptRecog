import pickle
import logging
import numpy as np

from seqlearn.perceptron import StructuredPerceptron

import script_recognition.repository.global_values as global_values

from script_recognition.repository.global_values import get_data

logging.basicConfig(filename="logs\\perceptron.log", level=logging.INFO)


def train_experiment(train_features, train_labels, train_lengths, max_iter=1000, lr_exponent=0.5):
    clf = StructuredPerceptron(verbose=1, max_iter=max_iter, lr_exponent=lr_exponent)
    clf.fit(train_features, train_labels, train_lengths)
    return clf


def predict(feature_values, label_values, length_values, clf):
    model_output = clf.predict(feature_values, length_values)
    perceptron_log("Per Entry Accuracy : " + str(sum([1 if a == b else 0 for a, b in zip(model_output, label_values)])))
    overall_match_loss(label_values, length_values, model_output)

    # json.dump(model_output.tolist(),
    #           open("prediction\\model_" + str(datetime.now().timestamp()).replace(".", "") + ".json", "w"))


def overall_match_loss(label_values, length_values, pred):
    correct_pred = 0

    ends = np.cumsum(length_values)
    start = ends - np.array(length_values)

    for index in range(len(length_values)):
        pred_array = pred[start[index]:ends[index]]
        initial_array = label_values[start[index]:ends[index]]

        if global_values.most_common(pred_array) == global_values.most_common(initial_array):
            correct_pred += 1

    perceptron_log(len(length_values))
    perceptron_log(correct_pred)
    perceptron_log(float(correct_pred) / float(len(length_values)))


def structured_perceptron_model(PERCEPTRON_MODE="train", train_level="Char", train_source="Original",
                                infer_model_source="model\\perceptron_hin_eng_3000_instance_training_71.json"):
    perceptron_log("_".join([PERCEPTRON_MODE, train_level, train_source]))

    language_labels = ["hindi", "english"]

    perceptron = None
    if PERCEPTRON_MODE.lower() == "train":
        data_partition = "train"
        global_feature_values, global_label_values, global_lengths = \
            get_data(language_labels, data_partition, train_level, train_source)

        perceptron = train_experiment(global_feature_values, global_label_values, global_lengths, max_iter=200,
                                      lr_exponent=0.01)

        model_file_name = global_values.get_filename(train_level, language_labels, data_partition, train_source,
                                                     "perceptron")
        pickle.dump(perceptron, open(model_file_name, "wb"))
        perceptron_log("Model dumped to  : " + model_file_name)

    elif PERCEPTRON_MODE.lower() == "infer":
        perceptron_log("Model infer source : " + infer_model_source)
        perceptron = pickle.load(open(infer_model_source, "rb"))

    if train_level == "Char":
        data_partition = "val"
        data_source = "strokeRecov"
        level = "Char"
        perceptron_log("_".join([data_partition, level, data_source]))
        test_features, test_labels, test_lengths = get_data(language_labels, data_partition, level, data_source)
        predict(test_features, test_labels, test_lengths, perceptron)

        if train_source == "Original":
            data_partition = "test"
            data_source = "Original"
            level = "Char"
            perceptron_log("_".join([data_partition, level, data_source]))
            test_features, test_labels, test_lengths = get_data(language_labels, data_partition, level, data_source)
            predict(test_features, test_labels, test_lengths, perceptron)

    if train_source == "Original":
        data_partition = "test"
        data_source = "Original"
        level = "Word"
        perceptron_log("_".join([data_partition, level, data_source]))
        test_features, test_labels, test_lengths = get_data(language_labels, data_partition, level, data_source)
        predict(test_features, test_labels, test_lengths, perceptron)

    data_partition = "test"
    data_source = "strokeRecov"
    level = "Word"
    perceptron_log("_".join([data_partition, level, data_source]))
    test_features, test_labels, test_lengths = get_data(language_labels, data_partition, level, data_source)
    predict(test_features, test_labels, test_lengths, perceptron)

    perceptron_log("structured_perceptron_model Process Done")


def perceptron_log(msg):
    logging.info(msg)
    print(msg)


if __name__ == '__main__':
    structured_perceptron_model("train")
