import logging

import script_recognition.repository.global_constants as gc
import script_recognition.repository.seqlearn_models as sq_learn

logging.basicConfig(filename="logs\\perceptron.log", level=logging.INFO)

if __name__ == '__main__':
    sq_learn.structured_perceptron_model("train", train_source=gc.STROKE_RECOVERY, train_level="Word")
