#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 12:17:41 2022

@author: snigdharudraraju
"""
import os
import numpy as np
import pandas as pd
import string
import json
import nltk
import re
import csv
import matplotlib.pyplot as plt 
import seaborn as sns
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import time
from sklearn.linear_model import LogisticRegression
import urllib.request
import zipfile
from sklearn.model_selection import train_test_split
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
#!python -m spacy download en_core_web_md
nlp = spacy.load('en_core_web_sm')

import gensim

import warnings
warnings.filterwarnings('ignore')

imdb_data=pd.read_csv("IMBD_top_1000_Processed.csv")
Plot_summary=pd.read_csv("with_plot_summary.csv")
imdb_data=imdb_data.merge(Plot_summary,how="left",left_on='mc_link',right_on='mc_link')
Working_df=pd.DataFrame()
# Working_df["Plot"]=imdb_data["plot"]
# Working_df["Movie_name"]=imdb_data["title_x"]
# Working_df["genre_new"]=imdb_data["genre"]
movies=imdb_data["title_x"]
moviesList = []
plotList = []
for movie in movies:
    for j in range(len(Plot_summary["title"])):
        if movie in Plot_summary["title"][j]:
            moviesList.append(movie)
            plotList.append(Plot_summary["plot"][j])
Working_df["Movie"]=moviesList
Working_df["Plot"]=plotList
Working_df=Working_df.merge(imdb_data,how="left",left_on='Movie',right_on='title_x')
Working_df=Working_df.drop(['certificate','votes','directors','stars','runtime','produce_year'], axis=1)
Working_df=Working_df.drop(['title_x','title_href','mc_link','introduction'], axis=1)
Working_df=Working_df.drop(['plot','title_y','wiki_link'], axis=1)


for i in range(len(Working_df['genre'])):
    Genre=[]
    Genre.append(Working_df['genre'][i])
    Working_df['genre'][i]=Genre
# get all genre tags in a list
all_genres = sum(Working_df["genre"],[])
len(set(all_genres))

all_genres = nltk.FreqDist(all_genres) 

# create dataframe
all_genres_df = pd.DataFrame({'Genre': list(all_genres.keys()), 
                              'Count': list(all_genres.values())})   
g = all_genres_df.nlargest(columns="Count", n = 50) 
plt.figure(figsize=(12,15)) 
ax = sns.barplot(data=g, x= "Count", y = "Genre") 
ax.set(ylabel = 'Count') 
plt.show() 

