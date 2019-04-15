#! /usr/bin/env python
#coding=utf-8
import simplejson as json
import random
import re

dataset_path='../data/yelp13/yelp_phoenix_academic_dataset-new' # new dataset path
business_id_path='../data/yelp13/business-id-random-list.txt'
user_id_path='../data/yelp13/users-id-random-list.txt'

class Business:
    def __init__(self,business_id,json_target):
        self.business_id=business_id
        self.attributes=json_target['attributes']
        self.reviews=[]
        self.json_target=json_target
    
    def addReview(self,review):
        self.reviews.append(review)


class Review:
    def __init__(self, business_id, json_target):
        self.user_id = json_target['user_id']
        self.stars = float(json_target['stars'])
        self.text = str(json_target['text'].encode('utf-8').strip(), encoding="utf-8")  # encode to utf-8
        self.business_id = business_id
        self.json_target = json_target

        self.sentences = split_sentences(self.text)


class User:
    def __init__(self, user_id, json_target):
        self.user_id = user_id
        self.reviews = []
        self.json_target = json_target
        self.friends = set(json_target['friends'])

    def addReview(self, review):
        self.reviews.append(review)


def readBusinessIDList():
    return [str(line.strip(), encoding="utf-8") for line in open(business_id_path, 'rb')]

def readUserIDList():
    return [line.strip() for line in open(user_id_path,'rb')]

def Analysis():
    business_dict={}
    
    users_dict={}
    user_review_dict={}
    line_count=0
    for line in open(dataset_path,'rb'):
        line=line.strip()
        if len(line)>0:
            json_target=JsonDecoder(line)
            # Business
            if json_target['type']=='business':
                business_id=json_target['business_id']
                business_dict[business_id]=Business(business_id,json_target)
            # review
            if json_target['type']=='review':
                business_id=json_target['business_id']
                user_id=json_target['user_id']
                # business-review
                if business_id in business_dict:
                    business_dict[business_id].addReview(Review(business_id,json_target))
                # user-review
                if user_id not in user_review_dict:
                    user_review_dict[user_id]=[]
                user_review_dict[user_id].append(Review(business_id,json_target))
                
            # user
            if json_target['type']=='user':
                user_id=json_target['user_id']
                u=User(user_id,json_target)
                if user_id in user_review_dict:
                    u.reviews=user_review_dict[user_id]
                if len(u.friends)>0 and len(u.reviews)>0:
                    users_dict[user_id]=u
            
            # line count
            line_count+=1
            if line_count%10000==0:
                print(line_count)
    
    #print 'len of business:',len(business_dict)
    #print 'len of reviews:', sum([len(v.reviews) for v in business_dict.values()])
    
    #return business_dict.values()
    bList=readBusinessIDList()
    uList=readUserIDList()
    return [business_dict[id] for id in bList if id in business_dict]

def JsonDecoder(line):
    return json.JSONDecoder().decode(line)

def split_sentences(text):
    sentences=[]
    for sentence in re.split('[.!?]\s', text):
        sentence=sentence.strip()
        if len(sentence)>10 and len(sentence.split())>3:
            sentences.append(sentence)
            
    return sentences
