# りどみ

入力された文章同士の類似度を計算する
大学SW工学用。機械学習完全に理解したにすら至ってないので色々不備は許してほしい。
結果のmodelや、それを作成するのに要したテキストファイル（jsonファイル）はgithubには載せてないので、「やったこと」を参照のこと。
別リポジトリ内から分離したためコミットログはありません。申し訳ない。

**参考にさせて頂いたサイト様**

[Doc2Vecの仕組みとgensimを使った文書類似度算出チュートリアル - DeepAge](https://deepage.net/machine_learning/2017/01/08/doc2vec.html)

[文章をベクトル化して類似文章の検索 - Qiita](https://qiita.com/akira_/items/f9bb46cad6834da32367)

[日本語Wikipediaで学習したdoc2vecモデル - Out-of-the-box](https://yag-ays.github.io/project/pretrained_doc2vec_wikipedia/)

[gensimでWikipedia日本語版からコーパスを作ってトピックモデリング :: takuti.me](https://takuti.me/ja/note/gensim-jawiki/)
[Doc2Vecについてまとめる - Qiita](https://qiita.com/g-k/items/5ea94c13281f675302ca)

## 使用したデータセットなど

[JAQKET:クイズを題材にした日本語QAデータセット](https://www.nlp.ecei.tohoku.ac.jp/projects/jaqket/)


***わからなかったら見る***

[gensim: models.doc2vec – Doc2vec paragraph embeddings](https://radimrehurek.com/gensim/models/doc2vec.html)

## 開発環境

Python 3.8.4(brew)
pip 20.1.1(brew install python@3.8同梱)

## やったこと・下準備

$から始まるのはコマンドライン操作

`pip install mecab-python3`

`pip install gensim`

`pip install unidic-lite`

`pip install pandas`

`$ curl https://jaqket.s3-ap-northeast-1.amazonaws.com/data/train_questions.json -O`

`$ mkdir data`

`$ mv train_questions.json data/train_questions.json`

## やれること

`$ python FAQ_model.py`

`$ python use_model.py  '火を神聖視ため拝火教とも呼ばれる紀元前6世紀のペルシアで始まった宗教は?等任意の文字' `

`$ python cosine_similarity_test.py 朝ごはんパンだった 朝ご飯はなにも食べなかった`

## 内部処理
- MeCabでテキストを分かち書きにする
- pandasはcsvデータ処理用
- gensimでDoc2Vecのモデル作成・利用

### Doc2Vecとは？
Word2Vecは単語の類似度を求めるものだった。
これをドキュメントに入った単語群を1つとしてあつかう。
つまり1つの文章を1つのベクトルにするという技術で、Word２Vecよりも文章を扱うのに特化している。

アルゴリズムとしてはPV-DMとPV-DBOWの2つの方法がある。今回ライブラリに支持したのはPV-DM。これは文章のidと単語群から次の単語を予測するというタスクを行うという学習を行う。
ベクトル化するときに文脈を保持するように振る舞うという特性があるらしい。

### FAQ_model.pyの解説
FAQ_model.pyでモデルの作成を行っている。
get_questions関数は[JAQKET:クイズを題材にした日本語QAデータセット](https://www.nlp.ecei.tohoku.ac.jp/projects/jaqket/)の問題文を抽出し、配列で返す事を行っている。この問題文を学習させる。

tokenize関数はMeCabで単語に分けている。

save_questions関数は学習した問題文をcsv形式で保存している。理由としては、Doc2Vecは「文章」と「ラベル」を学習し、文章が入力されるとそれに近い「ラベル」が出力されるため、そのラベル（今回は０から始まる番号）を保存する事で後に確認する際にjsonファイルを再度解析しなくても良くなるためである。

TaggedDocumentはgensimが「文章」と「ラベル」を読み込む際に用いる型に変換するものである。
Doc2Vechaはどの様に学習するかを指定するものである。詳細は[gensim: models.doc2vec – Doc2vec paragraph embeddings](https://radimrehurek.com/gensim/models/doc2vec.html)。

build_vocabは先程作成したTaggedDocumentの配列を入れ、学習させるデータを渡している。

trainで実際に学習させている。