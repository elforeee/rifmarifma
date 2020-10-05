from rupo.rupo.api import Engine
import numpy as np
import random
import pandas as pd
import re
from sklearn.neighbors import NearestNeighbors

engine = Engine(language="ru")
engine.load('/data/stress_models/stress_ru.h5', '/data/dict/zaliznyak.txt')

poems_matrix = pd.read_csv('poems_matrix.csv',encoding='utf-8')

with open('twograms0.txt', encoding='utf-8') as f:
    twograms0 = f.read()
twograms0 = twograms0.splitlines()
with open('twograms1.txt', encoding='utf-8') as f:
    twograms1 = f.read()
twograms1 = twograms1.splitlines()
with open('meters.txt', encoding='utf-8') as f:
    metres = f.read()
metres = metres.splitlines()
with open('poems.txt', encoding='utf-8') as f:
    corpus_poems = f.read()
corpus_poems = corpus_poems.splitlines()


def line2vector(new_line):
    vector = np.zeros(71)
    markup = engine.get_improved_markup(new_line)
    if markup[0].lines[0].words == []:
        return vector
    else:
        last = markup[0].lines[0].words[-1]
        if last.text == '':
            last = markup[0].lines[0].words[-2]
        twogram_0 = last.text[-2].lower()
        twogram_1 = last.text[-1].lower()
        metre = markup[1].metre

        vector[0] = engine.count_syllables(new_line)
        if twogram_0 in twograms0:
            vector[twograms0.index(twogram_0)+1] = 1
        if twogram_1 in twograms1:
            vector[twograms1.index(twogram_1) + len(twograms0) + 1] = 1
        if metre in metres:
            vector[metres.index(metre) + len(twograms0) + len(twograms1) + 1] = 1
        return vector


def chose_rhyme(matrix, vector):
    nn = NearestNeighbors(metric='euclidean')
    nn.fit(matrix)
    r = nn.kneighbors(vector.reshape(1, -1), 1)[0][0][0]
    return random.choice(nn.radius_neighbors(vector.reshape(1, -1), r)[1][0])


def clean_line(line):
    line = re.sub(r'[-,.:;_]+$',r'', line)
    return line


def line2rhyme(line):
    vector = line2vector(line)
    return clean_line(corpus_poems[chose_rhyme(poems_matrix, vector)])

