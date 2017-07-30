import os
import sys
from os import walk

import script_recognition.repository.info_for_different_folders as ID
import global_values

from random import Random


def process(pathname):
    if "Offline" in pathname:
        return pathname

    dirs = []
    for (r, d, f) in walk(pathname):
        dirs.extend(d)
        break
    for g1 in dirs:
        pathname = os.path.join(pathname, g1)
        dirs2 = []
        for (r, d, f) in walk(pathname):
            dirs2.extend(d)
            break
        return os.path.join(pathname, dirs2[0])
    print("PathName processing failed for pathname == " + pathname)
    sys.exit(0)


def main(function, seqDims, seqLengths, targetStrings, wordTargetStrings, seqTags, inputs, labelName, level, dataSource,
         debug=False):
    pathname, inputMeans, inputStds = ID.getPathName(labelName, level, dataSource)

    feature_values = []
    label_values = []
    lengths = []

    numeric_label = global_values.get_numeric_label(labelName)

    pathname = process(pathname)

    f = []
    for (dirpath, dirnames, filenames) in walk(pathname):
        f.extend(filenames)
        break
    start, end = ID.dataShareToUse(len(f), function, labelName, level, dataSource)
    start = int(start)
    end = int(end)

    Random(4).shuffle(f)

    for index, onefile in enumerate(f[start:end]):  # Running for each data file

        # Reason: There are files with no data for training. They are named usrX.txt and are to be avoided
        if not "txt" in onefile: continue

        word = labelName
        wordmod = labelName

        firstlinechk = 0  # To make sure that the lines of code before the data lines are avoided when necessary
        oldlen = len(inputs)
        thirdval = 0.0

        AtleastsomeDataFlag = False

        k = open(os.path.join(pathname, onefile)).readlines()
        for line in k:
            line = line.strip()
            parts = line.split()
            if len(parts) == 0: continue

            if firstlinechk == 0 and line != ".PEN_DOWN":  # Skip these lines as they donot have needed info
                continue
            elif line == ".PEN_DOWN":
                firstlinechk = 1  # Nolonger the firstlines part, now all the information is relevant
                thirdval = 1.0  # Stores the value for the third column of the first point in the stroke to signify "PENDOWN"
            elif line == ".PEN_UP":
                continue
            else:
                coordinates = line.split()
                inputs.append([float(coordinates[0]), float(coordinates[1]), thirdval])  # append the point to the others of this stroke
                thirdval = 0.0
                AtleastsomeDataFlag = True

                # Sequence Learning
                feature_values.append([float(coordinates[0]), float(coordinates[1]), thirdval])
                label_values.append(numeric_label)

        if AtleastsomeDataFlag == True:
            seqTags.append(onefile)  # appending to seqtags
            wordTargetStrings.append(word)
            targetStrings.append(wordmod)
            seqLengths.append(len(inputs) - oldlen)
            seqDims.append([seqLengths[-1]])

            lengths.append(len(inputs) - oldlen)

            if debug == True:
                print("Sequence lengths " + str([seqLengths[-1]]))
            if seqLengths[-1] == 0:
                print("raw input has been removed?")
            # raw_input("The seqLengths for this instance is zero.\nThis should not have happened and will cause errors later (core dump while training).\nProceed with caution.")
        else:
            # print(onefile + " has no data at all\n")
            pass
        # here the iteration for this file ends
    return inputMeans, inputStds, feature_values, label_values, lengths
