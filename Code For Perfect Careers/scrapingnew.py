#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 23:54:22 2017

@author: Yuvaraj and Akanksha
"""

from bs4 import BeautifulSoup as Soup
import urllib, requests, re, pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

file_path = '~/Desktop/MLproject/job.csv'

#pd.set_option('max_colwidth',500)    # to remove column limit (Otherwise, we'll lose some info)
#salary_label_list = ['$80,000','$90,000','$100,000','$110,000','$120,000']


def getJobDesc():
    try:
        df = pd.read_csv(file_path)
    except OSError:
        df = pd.DataFrame()

    salary_label_list_SoftDeveloper = ['$125,000','$115,000','$105,000','$95,000','$85,000']
    salary_label_list = ['$120,000','$100,000','$85,000','$70,000','$50,000']

    
    for i in salary_label_list:
        #base_url = 'http://www.indeed.com/jobs?q=data+scientist&jt=fulltime&sort='
        base_url = 'https://www.indeed.com/jobs?q=software+developer%s&l=New+York,+NY&radius=100&sort=' % i
        #base_url = 'https://www.indeed.com/jobs?q=data+analyst+$50,000&radius=100&sort='
        sort_by = 'date'          
        start_from = '&start='

        print(base_url)
        for page in range(1,101): # able to fetch only 100 pages (1101 jobs)
            page = (page-1) * 10  
            url = "%s%s%s%d" % (base_url, sort_by, start_from, page)  
            target = Soup(urllib.request.urlopen(url), "lxml") 

            targetElements = target.findAll('div', attrs={'class': re.compile('row result')})
            #print(targetElements)
    
            for elem in targetElements:
                try:
                    job_key = elem.attrs['data-jk']
                    comp_name = elem.find('span', {'class': re.compile('company')}).text.strip()
                    job_title = elem.find('a', {'class': 'turnstileLink'}).attrs['title']
                    job_location = elem.find('span', {'class': 'location'}).text.strip()
                except (KeyError, AttributeError):
                    pass


                try:
                    if (df['job_key'] == job_key).any():
                        print('inside')
                        continue
                except KeyError:
                    pass
        
                '''pattern = re.compile('.*data.scientist.*')
                if pattern.match(job_title.lower()) == None:
                    continue'''
        
                indeed_url = "https://www.indeed.com/viewjob?jk="
                job_link = "%s%s" % (indeed_url,job_key)
        
                targetDesc = Soup(urllib.request.urlopen(job_link), "lxml")
                job_summary = targetDesc.find('span', {'id': 'job_summary'}).text.strip()
                job_summary=re.sub('[^a-zA-Z\d]',' ',job_summary)
                job_summary=re.sub(' +',' ',job_summary).strip()
                tokenized_job_summary = word_tokenize(job_summary)
                filtered_job_summary = [word for word in tokenized_job_summary if word not in stopwords.words('english')]
        #break
        
                #break
                df = df.append({'comp_name': comp_name,
                                'job_title': job_title,
                                'job_location': job_location,
                                'job_key': job_key,
                                'job_link': job_link,
                                'job_summary':job_summary,
                                'salary_label': i
                                }, ignore_index=True)


            print(page)
    return df    



job_desc_df=getJobDesc()    
job_desc_df.to_csv(path_or_buf='jobs.csv', index=False)