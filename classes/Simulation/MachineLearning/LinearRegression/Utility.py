import numpy as np


def get_data(x, y, theta):
    data = [['feature', 'output', 'prediction']]
    for i in range(x.__len__()):
        data.append([x[i], y[i], theta[0] + theta[1] * x[i]])
    return data


def validate_entry(string):
    mat = []
    rows = string.split('\\r\\n')
    for row in rows:
        colf = []
        col = row.split(',')
        for num in col:
            try:
                n = float(str(num).replace('\"', ''))
                colf.append(n)
            except ValueError:
                return False
        mat.append(colf)
    for row in mat:
        if row.__len__() != 2:
            return False
    return True


def get_matrix(string):
    if validate_entry(string) is False:
        return None
    mat = []
    rows = string.split('\\r\\n')
    for row in rows:
        colf = []
        col = row.split(',')
        for num in col:
            n = float(str(num).replace('\"', ''))
            colf.append(n)
        mat.append(colf)
    mat = np.asarray(mat)
    mat = mat.flatten()
    x = []
    y = []
    for i in range(0, mat.size, 2):
        x.append([mat[i]])
        y.append(mat[i + 1])
    x = np.asarray(x)
    y = np.asarray(y)
    return [x, y]
