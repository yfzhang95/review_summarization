#! /usr/bin/env python
#coding=utf-8
from document import get_summary_data,NUM_TRAIN,get_golds
# import nn_summary
import numpy as np
import pickle
import svm


# b_list=get_summary_data()
# pickle.dump(b_list, open('../data/business_list.pkl', 'wb'))

b_list = np.load('../data/business_list.pkl')
trains = b_list[:NUM_TRAIN]
# tests = b_list[NUM_TRAIN:]
# pickle.dump(tests, open('../data/products.txt', 'wb'))
tests = np.load('../data/products.txt')
# V = svm.get_vocabrary(trains,10000)
# pickle.dump(V, open('../data/vocab.txt', 'wb'))
V = np.load('../data/vocab.txt')

res = svm.svm_predict(tests[10], V)
print(res)
print("hahha")