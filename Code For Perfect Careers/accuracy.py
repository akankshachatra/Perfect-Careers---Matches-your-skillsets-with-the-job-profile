#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 20:46:51 2017

@author: Yuvarajand Akanksha
"""

from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.feature_extraction.text import TfidfVectorizer
file_path = '~/Desktop/MLproject/jobs.csv'

df = pd.read_csv(file_path)


#train=df
train=df.sample(frac=0.9,random_state=200)
test=df.drop(train.index)

def concat(job_title, job_summary):
    job_details = job_title + ' : ' + job_summary
    return job_details

def getJobDetails(table):
    job_details_list = []
    for row in table.itertuples():
        #print(row)
        job_details = concat(row[6].lower(), row[5])
        job_details_list.append(job_details)
        #print(job_details_list)
    return job_details_list



def model(train_data,test_data,train,test):
    
    #print('vectorised')
    transformer = TfidfVectorizer(sublinear_tf=True,max_df=0.1,stop_words="english")
    traintf=transformer.fit_transform(train_data)
    testtf=transformer.transform(test_data)
    #print(traintf)
    selector=SelectPercentile(f_classif,percentile=90)
    selector.fit(traintf,train['comp_name'])
    traintransform=selector.transform(traintf).toarray()
    testtransform=selector.transform(testtf).toarray()

    
    gnb=GaussianNB()
    dst=DecisionTreeClassifier()
    knn=KNeighborsClassifier(n_neighbors=1)
    X=traintransform
    Y=train['comp_name']
    
    print('Fitting')
    dst.fit(X,Y)#.todense()
    gnb.fit(X,Y)
    knn.fit(X,Y)
    print('Predicting')
    preddst = dst.predict(testtransform)#.todense())
    predgnb=gnb.predict(testtransform)
    predknn=knn.predict(testtransform)
    #print('Predicting Accuracy of Decision Tree')
    #print(pred)
    accuracydst = accuracy_score(preddst, test['comp_name'])
    accuracygnb = accuracy_score(predgnb, test['comp_name'])
    accuracyknn = accuracy_score(predknn, test['comp_name'])
    print('Predicting Accuracy of Decision Tree')
    print(accuracydst)
    print('Predicting Accuracy of GaussainNB')
    print(accuracygnb)
    print('Predicting Accuracy of KNN')
    print(accuracyknn)
 


train_details=getJobDetails(train)
test_details=getJobDetails(test)

model(train_details,test_details,train,test)


