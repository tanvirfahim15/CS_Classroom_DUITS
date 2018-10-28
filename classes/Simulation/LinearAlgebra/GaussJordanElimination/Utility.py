import numpy as np


def validate_entry(string):
    mat = []
    rows = string.split('\\r\\n')
    for row in rows:
        colf = []
        col = row.split(' ')
        for num in col:
            try:
                n = float(str(num).replace('\"', ''))
                colf.append(n)
            except ValueError:
                return False
        mat.append(colf)
    cols = mat[0].__len__()
    for row in mat:
        if row.__len__() != cols:
            return False
    return True


def get_matrix(string):
    if validate_entry(string) is False:
        return None
    mat = []
    rows = string.split('\\r\\n')
    for row in rows:
        colf = []
        col = row.split(' ')
        for num in col:
            n = float(str(num).replace('\"', ''))
            colf.append(n)
        mat.append(colf)
    return np.asanyarray(mat)
