import sys
import xml.etree.ElementTree as ET 
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
import MeCab

def tokenize(text):
    wakati = MeCab.Tagger("-Owakati")
    wakati.parse("")
    return wakati.parse(text).strip().split()

def read_my_csv(csv_path):
    data = dict(pd.read_csv(csv_path, header=None).values.tolist())
    return data

args = sys.argv

model = Doc2Vec.load("doc2vec.model")
questions = read_my_csv('data/questions.csv')
result = model.docvecs.most_similar([model.infer_vector(tokenize(args[1]))])
print("対象:{}\n最も似た文章:{}\n次に似ている文章:{}\n".format(args[1],questions[result[0][0]],questions[result[1][0]]))