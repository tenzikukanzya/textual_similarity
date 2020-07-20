import sys
from gensim.models.doc2vec import Doc2Vec
import MeCab
args = sys.argv

def tokenize(text):
    wakati = MeCab.Tagger("-Owakati")
    wakati.parse("")
    return wakati.parse(text).strip().split()

model = Doc2Vec.load("doc2vec.model")
result = model.docvecs.similarity_unseen_docs(model,tokenize(args[1]),tokenize(args[2]))
print('類似度:{}'.format(result))