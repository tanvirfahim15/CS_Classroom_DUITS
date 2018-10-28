import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
from collections import OrderedDict
import os
print(os.getcwd())

# Returns words from a text
def get_vector(text):
    ret = ""
    stp=["!", "@", "#", "|", "%", "(", ")", "।", "—", ".", "-", "", ",", "’", "•", "‘", ":", "*", "?",
          "০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"]
    for x in text:
        if x in stp:
            ret = ret + " "
        else:
            ret = ret + x
    ret = ret.replace("  ", " ")
    ret = ret.replace("  ", " ")
    ret = ret.split()
    return ret


def classify(text):
    file = open("Fruits.obj", 'rb')
    logisticRegr=pickle.load(file)
    vector = get_vector(text)

    features = OrderedDict()
    features_file = open('feature.txt', 'r', encoding="utf8")
    for line in features_file:
        features[line.split(',')[0]] = 0

    mark = 0
    for v in vector:
        if v in features:
            features[v] = features[v] + 1
            mark = 1

    if mark == 0:
        return "No bangla text found"

    input = []
    for f in features:
        input.append(features[f])
    prediction = logisticRegr.predict([input])

    if prediction[0] == 1:
        return 'Bangladesh'
    elif prediction[0] == 2:
        return 'Economy'
    elif prediction[0] == 3:
        return 'Entertainment'
    elif prediction[0] == 4:
        return 'International'
    elif prediction[0] == 5:
        return 'Sports'

