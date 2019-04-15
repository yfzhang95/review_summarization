import numpy as np
from scipy.sparse import lil_matrix
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import os
from data import split_sentences
from document import LEN_SUMMARY
from collections import Counter


class CDocument:
    def __init__(self, text, label):
        self.text = text
        self.label = label

        self.words = []
        for w in text.split():
            self.words.append(w.lower())

def get_vocabrary(trains, n = 10000):
    # DF
    df = {}
    for b in trains:
        for r in b.reviews:
            # print("--", str(r.text, encoding = "utf-8"))
            for w in r.text.split():
                w=w.lower()
                df[w] = df.get(w, 0) + 1
    c = Counter(df)
    # print("c:",c)
    V = {w: i for i, (w, c) in enumerate(c.most_common(n), start=1)}    #1
    print("v:",V)
    print('length of V:', len(V))

    return V

def get_trains(trains):
    documents = []
    for b in trains:
        # positive
        for sentence in split_sentences(b.summary_text):
            documents.append(CDocument(sentence, 1))
            # print(sentence)

        # negative
        for r in b.reviews:
            for sentence in r.sentences:
                documents.append(CDocument(sentence, 0))

    return documents


def get_tests(product):
    documents = []

    for r in product.reviews:
        for sentence in r.sentences:
            documents.append(CDocument(sentence, 0))

    return documents


def formatK(documents, V):
    m = len(documents)
    n = len(V)
    X = lil_matrix((m, n))  # 构建稀疏矩阵
    y = np.zeros((m,))
    for i,d in enumerate(documents):
        vec = [0] * n
        for w in d.words:
            if w in V:
                vec[V[w] - 1] = 1  # 这里设置为1效果会好一点

        X[i] = vec
        y[i] = d.label
    return X, y


def svm_train(trains, V):
    cTrains = get_trains(trains)

    train_x, train_y = formatK(cTrains, V)

    transformer = TfidfTransformer()
    train_x = transformer.fit_transform(train_x)
    clf = CalibratedClassifierCV(LinearSVC(random_state=0))
    if os.path.exists('review_summary_model.m'):
        clf = joblib.load("review_summary_model.m")
        print("---------------hahahaha-------------")
    else:
        clf.fit(train_x, train_y)
        joblib.dump(clf, "review_summary_model.m")
    clf = joblib.load("review_summary_model.m")

    return clf

#svm测试结果
def svm_predict(tests, V):

    cTests = get_tests(tests)

    test_x, _ = formatK(cTests, V)

    transformer = TfidfTransformer()

    test_x = transformer.fit_transform(test_x)

    clf = joblib.load("review_summary_model.m")

    x_pred = clf.predict_proba(test_x)

    print("len:", len(x_pred))

    pr_results = []
    i = 0
    for r in tests.reviews:
        for sentence in r.sentences:
            pr_results.append((x_pred[i][1], sentence))
            i += 1

    pr_results.sort()
    pr_results.reverse()

    summary_text = ''
    for score, sentence in pr_results:
        summary_text += ' %s' % sentence
        if len(summary_text.split()) > LEN_SUMMARY:
            break

    summary_text = summary_text.strip()

    return summary_text
