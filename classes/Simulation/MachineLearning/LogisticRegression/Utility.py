import numpy as np


def validate_entry(data):
    try:
        int(data['iterations'])
        int(data['steps'])
        float(data['alpha'])
    except ValueError:
        return False
    data = data['entry']
    rows = data.split('\r\n')
    for row in rows:
        cols = row.split(',')
        for col in cols:
            try:
                float(col)
            except ValueError:
                return False
        if cols[2] != '0' and cols[2] != '1':
            return False
        if len(cols) != 3:
            return False
    return True


def get_data(data):
    x1 = list()
    x2 = list()
    y = list()
    rows = data.split('\r\n')
    for row in rows:
        cols = row.split(',')
        x1.append(float(cols[0]))
        x2.append(float(cols[1]))
        y.append(float(cols[2]))
    return [x1, x2, y]


def combine(x1, x2):
    x = []
    for i in range(len(x1)):
        x.append([x1[i], x2[i]])
    return np.asarray(x)

