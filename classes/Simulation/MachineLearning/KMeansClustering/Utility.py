
def validate_entry(string):
    mat = []
    rows = string.split('\r\n')
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


def get_points(string):
    if validate_entry(string) is False:
        return None
    points = list()
    rows = string.split('\r\n')
    for row in rows:
        col = row.split(',')
        points.append([float(col[0]), float(col[1])])
    return points
