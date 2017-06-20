#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:22:08 2017

@author: Yuvaraj and Akanksha
"""

import io
import PyPDF2
import codecs
import re
from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif



file_path = '~/Desktop/MLproject/jobs.csv'
df = pd.read_csv(file_path)
train=df
def pdfextraction():
     pdffile=open('Yuvaraj_DataEngineering.pdf','rb')
     pdfreader=PyPDF2.PdfFileReader(pdffile)
     np=pdfreader.numPages
     pagecontent=pdfreader.getPage(0)
     pagedata=pagecontent.extractText()
     pagedata=re.sub('[^a-zA-Z\d]',' ',pagedata)
     pagedata=re.sub(' +',' ',pagedata).strip()
     tokenized_pagedata = word_tokenize(pagedata)
     filtered_pagedata = [word for word in tokenized_pagedata if word not in stopwords.words('english')]
     filtered=' '.join(filtered_pagedata)
     return filtered

resumedata=pdfextraction()
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

test=[resumedata]

def model(train_data,train,test):
    
    
    transformer = TfidfVectorizer(sublinear_tf=True,max_df=0.1,stop_words="english")
    traintf=transformer.fit_transform(train_data)
    testtf=transformer.transform(test)
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
    '''accuracydst = accuracy_score(preddst, test['comp_name'])
    accuracygnb = accuracy_score(predgnb, test['comp_name'])
    accuracyknn = accuracy_score(predknn, test['comp_name'])'''
    print('Prediction using  Decision Tree')
    print(preddst)
    print('Prediction using  GaussainNB')
    print(predgnb)
    print('Prediction using KNN')
    print(predknn)
    
    
    
 


train_details=getJobDetails(train)


model(train_details,train,test)
