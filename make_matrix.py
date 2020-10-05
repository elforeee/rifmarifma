from rupo.rupo.api import Engine
import pandas as pd

engine = Engine(language="ru")
engine.load('rupo/data/stress_models/stress_ru.h5', 'rupo/data/dict/zaliznyak.txt')

with open('poems.txt', encoding='utf-8') as f:
    corpus_poems = f.read()
corpus_poems = corpus_poems.splitlines()

lines_json = []
for line in corpus_poems:
    markup = engine.get_improved_markup(line)
    last = markup[0].lines[0].words[-1]
    if last.text == '':
        last = markup[0].lines[0].words[-2]
    twogram = last.text[-2:].lower()
    lines_json.append([markup[1].metre,engine.count_syllables(line),twogram[0],twogram[-1]])

df = pd.DataFrame(lines_json, columns=['metre','n_syll','two_gram_0','two_gram_1'])

twograms0 = sorted(df.two_gram_0.unique().tolist())
twograms1 = sorted(df.two_gram_1.unique().tolist())
metres = sorted(df.metre.unique().tolist())

with open('twograms0.txt', 'w', encoding='utf-8') as f:
    for twogram0 in twograms0:
        f.write(twogram0+'\n')
with open('twograms1.txt', 'w', encoding='utf-8') as f:
    for twogram1 in twograms1:
        f.write(twogram1+'\n')
with open('meters.txt', 'w', encoding='utf-8') as f:
    for metre in metres:
        f.write(metre+'\n')

df_w_dummies = pd.concat([df, pd.get_dummies(df.two_gram_0, prefix='2gram0')], axis=1).drop(['two_gram_0'],axis=1)
df_w_dummies = pd.concat([df_w_dummies, pd.get_dummies(df.two_gram_1, prefix='2gram1')], axis=1).drop(['two_gram_1'],axis=1)
df_w_dummies = pd.concat([df_w_dummies, pd.get_dummies(df.metre, prefix='metre')], axis=1).drop(['metre'],axis=1)

df_w_dummies.to_csv('poems_matrix.csv', index=False)