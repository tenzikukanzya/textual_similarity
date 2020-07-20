import sys

import json
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

import pandas as pd
import MeCab

def get_questions():
    doc_path = './data/train_questions.json'
    questions = []
    with open(doc_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            questions.append(data['question'])
    return questions

def tokenize(text):
    wakati = MeCab.Tagger("-Owakati")
    wakati.parse("")
    return wakati.parse(text).strip().split()

def save_questions(question):
    with open('./data/questions.csv', 'w') as f:
        for i,txt in enumerate(question):
            f.write("{},{}\n".format(i,txt.replace('、','').replace(',','')))

def read_my_csv(csv_path):
    data = dict(pd.read_csv(csv_path, header=None).values.tolist())
    return data



questions = get_questions()
save_questions(questions)

documents = [TaggedDocument(tokenize(doc), [i]) for i, doc in enumerate(questions)]
model = Doc2Vec(dm=1,vector_size=400,windows=5,min_count=0, epochs=100)
model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

model.save("doc2vec.model")