#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from data import Analysis
import numpy as np

NUM_REVIEW=100
FUNNY_TH=1
COOL_TH=1
USEFUL_TH=1

NUM_TRAIN=600

LEN_SUMMARY=283 # average word length of summary: 283   #250

NUM_REVIEW_FOR_SUMMARY=10


def get_summary_data():
    b_list = Analysis()

    # select business for summarization
    new_b_list = []
    for b in b_list:
        if len(b.reviews) > NUM_REVIEW:
            reviews = []
            for i, r in enumerate(b.reviews):
                funny, useful, cool = int(r.json_target['votes']['funny']), int(r.json_target['votes']['useful']), int(
                    r.json_target['votes']['cool'])
                if funny > FUNNY_TH and cool > COOL_TH and useful > USEFUL_TH:
                    summary_score = useful + funny + cool
                    # print funny,useful,cool
                    reviews.append((summary_score, r, i))
            # print len(reviews)
            if len(reviews) > 0:
                # reviews.sort()
                reviews = sorted(reviews, key=lambda x: (x[0]))
                summary_text = reviews[-1][1].text.strip()

                review_index = reviews[-1][2]
                del b.reviews[review_index]  # remove summary review

                b.summary_text = summary_text

                b.reviews = b.reviews[:NUM_REVIEW_FOR_SUMMARY]

                new_b_list.append(b)
    print(len(new_b_list))

    return new_b_list

def get_summary_data2():

    b_list = Analysis()

    # select business for summarization
    new_b_list = []
    for b in b_list:
        if len(b.reviews) > NUM_REVIEW:
            reviews = []
            for i, r in enumerate(b.reviews):
                funny, useful, cool = int(r.json_target['votes']['funny']), int(r.json_target['votes']['useful']), int(
                    r.json_target['votes']['cool'])
                if funny > FUNNY_TH and cool > COOL_TH and useful > USEFUL_TH:
                    summary_score = useful + funny + cool
                    # print funny,useful,cool
                    reviews.append((summary_score, r, i))
            # print len(reviews)
            if len(reviews) > 0:
                # reviews.sort()
                reviews = sorted(reviews, key=lambda x: (x[0]))
                summary_text = reviews[-1][1].text.strip()

                review_index = reviews[-1][2]
                del b.reviews[review_index]  # remove summary review

                b.summary_text = summary_text

                b.reviews = [b.reviews[i] for i in np.random.choice(len(b.reviews), NUM_REVIEW_FOR_SUMMARY)]

                # b.reviews = b.reviews[:NUM_REVIEW_FOR_SUMMARY]

                new_b_list.append(b)
    print(len(new_b_list))

    return new_b_list
def get_summary_data3():
    b_list = Analysis()

    # select business for summarization
    new_b_list = []
    for b in b_list:
        if len(b.reviews) > NUM_REVIEW:
            reviews = []
            new_reviews = []
            for i, r in enumerate(b.reviews):
                funny, useful, cool = int(r.json_target['votes']['funny']), int(r.json_target['votes']['useful']), int(
                    r.json_target['votes']['cool'])
                new_reviews.append((useful + funny + cool, r, i))
                if funny > FUNNY_TH and cool > COOL_TH and useful > USEFUL_TH:
                    summary_score = useful + funny + cool
                    # print funny,useful,cool
                    reviews.append((summary_score, r, i))
            # print len(reviews)
            if len(reviews) > 0:
                reviews = sorted(reviews, key=lambda x: (x[0]))
                summary_text = reviews[-1][1].text.strip()
                b.summary_text = summary_text

                review_index = reviews[-1][2]
                del new_reviews[review_index]
                new_reviews = sorted(new_reviews, key=lambda x: (x[0]), reverse=True)
                b.reviews = [r[1] for r in new_reviews[:NUM_REVIEW_FOR_SUMMARY]]

                new_b_list.append(b)
    print(len(new_b_list))

    return new_b_list


def get_golds(b_list):
    golds=[]
    for b in b_list:
        golds.append(b.summary_text)
    return golds