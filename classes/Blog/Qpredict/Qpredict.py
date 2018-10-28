from bs4 import BeautifulSoup


def load_idf():
    input = open('classes/Blog/Qpredict/idf.txt', encoding="utf8").readlines()

    idf = {}
    for line in input:
        tokens = line.replace("\n", "").split(",")
        key = tokens[0]
        value = float(tokens[1])
        idf[key] = value
    return idf


def Qpredict(input=None):
    idf = load_idf()
    input = BeautifulSoup(input,features="html.parser").text.replace('\n', '').replace('\xa0',' ')
    sentences = input.split('.')
    out = []
    for line in sentences:
        tokens = line.lower().replace('\n', '').replace(',', '').split(' ')
        max_score = 0.0
        token = tokens[0]
        if len(tokens) < 3:
            continue
        for tok in tokens:
            if tok in idf.keys() and idf[tok] > max_score:
                max_score = idf[tok]
                token = tok
        ans = line.lower().replace('\n', '').replace(token, '____')

        out.append((ans, token, max_score))
    sorted_out = sorted(out, key=lambda tup: (tup[2], tup[1]))

    return sorted_out[0:5]

