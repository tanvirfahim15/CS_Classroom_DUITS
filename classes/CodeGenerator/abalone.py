import pandas as pd
import numpy as np


def get_dataset():
    df = pd.read_csv('classes/CodeGenerator/abalone.csv', sep=',', header=None)
    arr = np.array(df)[:, 0:8]

    header = ['Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight',
              'Rings']
    ret = '<table class="table"><thead><tr>'
    for item in header:
        ret += '<th>' + item + '</th>'
    ret += '</tr></thead>'
    for row in arr:
        ret += '<tr>'
        for col in row:
            ret += '<td>' + str(col) + '</td>'
        ret += '</tr>'
    ret += '</table>'
    return ret


def get_X():
    df = pd.read_csv('classes/CodeGenerator/abalone.csv', sep=',', header=None)
    arr = np.array(df)
    X = arr[:, 0:7]
    ret=''
    for row in X:
        ret+='['
        for col in row:
            ret+=str(col)+', '
        ret += ']<br/>'
    return ret


def get_y():
    df = pd.read_csv('classes/CodeGenerator/abalone.csv', sep=',', header=None)
    arr = np.array(df)
    y = arr[:, 7]
    ret='['
    for item in y:
        ret+= str(item)+',<br/>'
    ret+=']'
    return ret


def get_X_select(selections_js):
    df = pd.read_csv('classes/CodeGenerator/abalone.csv', sep=',', header=None)
    arr = np.array(df)
    X = arr[:, 0:7]
    y = arr[:, 7]
    selections = [];
    for item in selections_js.split(','):
        if item == 'true':
            selections.append(True);
        else:
            selections.append(False);
    selections = np.asarray(selections);
    X = X[:, selections]
    ret=''
    for row in X:
        ret+='['
        for col in row:
            ret+=str(col)+', '
        ret += ']<br/>'
    return ret


def get_feature_distribution(feature):
    df = pd.read_csv('classes/CodeGenerator/abalone.csv', sep=',', header=None)
    arr = np.array(df)
    X = arr[:, int(feature)]
    ret = ''
    for item in X:
        ret += str(item) + ','
    return ret
