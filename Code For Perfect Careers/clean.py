#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 08:51:11 2017

@author: Akanksha
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
import re

file_path = '~/Desktop/MLproject/job.csv'

try:
    df = pd.read_csv(file_path)
except OSError:
    pass

def clean(job_summary):
    js = re.sub('[^a-zA-Z\d]',' ',job_summary)
    js = re.sub(' +', ' ', js).strip()

    words = nltk.word_tokenize(js.lower())

    filtered_words = [word for word in words if word not in stopwords.words('english')]

    return ' '.join(filtered_words)

def cleanJobDesc():
    for index, summary in enumerate(df['job_summary']):
        cleaned_summary = clean(summary)
        df.set_value(index, 'job_summary', cleaned_summary)
        print(index)

cleanJobDesc()
df.to_csv('jobs.csv', index=False)
