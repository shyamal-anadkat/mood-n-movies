#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 09:52:12 2022

@author: snigdharudraraju
"""

# Lets start with tokenizing the data to get all the inputs in a single row
# Sorting data into dataframes

# Sorting data into dataframes
import string

from spacy.lang.en.stop_words import STOP_WORDS
import numpy as np
import pandas as pd
import spacy
import nltk
from numpy import array

#!python -m spacy download en_core_web_md
nlp = spacy.load("en_core_web_sm")
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from nltk.corpus import stopwords


import warnings

nltk.download('stopwords')
warnings.filterwarnings("ignore")

imdb_data = pd.read_csv("../../data/processed/IMDB_top_1000_clean.csv")
movies = array(imdb_data["title"])
Introduction = array(imdb_data["introduction"])

genre3 = imdb_data["genre"].str.split(",", expand=True)

imdb_data["genre0"] = genre3[0]
imdb_data["genre1"] = genre3[1]
imdb_data["genre2"] = genre3[2]

imdb_data = imdb_data.drop(
    ["certificate", "votes", "directors", "stars", "runtime", "produce_year"], axis=1
)



# Processing data taken from customer and getting their mood
val = input("what do you feel like watching: ")
mood = input("Enter your mood: [Sadness, Joy, Fear, Anger, Surprise, Love]")


# Map the mood to genres
# data for mapping
topic_list = [
    "Action",
    "Comedy",
    "Crime",
    "Drama",
    "Adventure",
    "Horror",
    "Mystery",
    "Family",
    "Fantasy",
    "Thriller",
    "Romance",
    "Sci-Fi",
]
feelings = [
    "Joy",
    "Sadness",
    "Surprise",
    "Love",
    "Joy",
    "Fear",
    "Surprise",
    "Anger",
    "Joy",
    "Surprise",
    "love",
    "Joy",
]

rows_map = []
for i in range(len(topic_list)):
    rows_map.append([feelings[i], topic_list[i]])
mapping_table = pd.DataFrame(rows_map, columns=["Mood_map", "Genre_map"])


# Comparision with genres basis our classification

list_of_genres = []
for i in range(len(mapping_table["Mood_map"])):
    if mapping_table["Mood_map"][i] == mood:
        list_of_genres.append(mapping_table["Genre_map"][i])

#%% LDA classification
Plot_summary = pd.read_csv("../../data/processed/with_plot_summary.csv")
imdb_data = imdb_data.merge(
    Plot_summary, how="left", left_on="mc_link", right_on="mc_link"
)


movies = list(imdb_data["title_x"])

for i in range(len(movies)):
    for j in range(len(Plot_summary["title"])):
        if movies[i] in Plot_summary["title"][j]:
            imdb_data["plot"][i] = Plot_summary["plot"][j]
imdb_data = imdb_data.dropna(subset=["plot"])
P_r = imdb_data["plot"]


def vectorize(documents, vectorizer_type="count"):
    # Use both 1-grams and 2-grams
    n_gram_range = (1, 2)

    if vectorizer_type == "count":
        vectorizr = CountVectorizer(
            max_df=0.6, ngram_range=n_gram_range, stop_words=stopwords.words("english")
        )
        f_vecs = vectorizr.fit_transform(documents)
        f_vecs = f_vecs.todense().tolist()
    else:
        vectorizr = TfidfVectorizer(
            max_df=0.6, ngram_range=n_gram_range, stop_words=stopwords.words("english")
        )
        f_vecs = vectorizr.fit_transform(documents)
        f_vecs = f_vecs.todense().tolist()

    return f_vecs, vectorizr


def model_topics(vectorized_text, vectorizer, n_topics, n_words, model_type):
    if model_type == "lda":
        # Perform LDA
        model = LatentDirichletAllocation(
            n_components=n_topics, learning_method="online", random_state=1
        )
        topic_assignments = model.fit_transform(vectorized_text)
    else:
        # Use LSA
        model = TruncatedSVD(n_components=n_topics, n_iter=500, random_state=0)
        topic_assignments = model.fit_transform(vectorized_text)

    # Get the main keywords and scores corresponding to each topic
    vocab = vectorizer.get_feature_names()
    topics = []
    for comp in model.components_:
        # Get the top keywords for each topic
        sorted_words = [vocab[score] for score in np.argsort(comp)[::-1]][:n_words]
        # Get the scores for each top keyword
        sorted_scores = np.sort(comp)[::-1][:n_words]
        words_scores = zip(sorted_words, sorted_scores)
        topics.append(words_scores)

    return model, topics, topic_assignments


feature_vecs, vectorizer = vectorize(P_r, vectorizer_type="tfidf")
model, topics, topic_assignments = model_topics(
    feature_vecs, vectorizer, n_topics=32, n_words=3, model_type="lda"
)

#%%% Selecting movies based on mean squared error.

val_df = pd.Series([val])
feature_vecs1 = vectorizer.transform(val_df)
a = model.transform(feature_vecs1)
b = np.mean(np.square(topic_assignments - a), axis=1)
c = np.argsort(b)
imdb_data["scores"] = c

#%%Comparing and selecting the movies
genreCountCheck = 0
for genre in list_of_genres:
    if genreCountCheck == 0:
        genreCount = imdb_data["genre0"] == genre
        genreCount = genreCount.astype("int32")
    else:
        temp = imdb_data["genre0"] == genre
        genreCount = genreCount.add(temp.astype("int32"))
    temp = imdb_data["genre1"] == genre
    genreCount = genreCount.add(temp.astype("int32"))
    temp = imdb_data["genre2"] == genre
    genreCount = genreCount.add(temp.astype("int32"))
    genreCountCheck += 1


Final_df = pd.DataFrame()
Final_df["Titles"] = imdb_data["title_x"]
Final_df["Count"] = genreCount.values
Final_df["MetaS"] = imdb_data["metascore"]
Final_df["imdbr"] = imdb_data["rating"]
Final_df["score"] = imdb_data["scores"]

Final_df = Final_df.sort_values(
    ["Count", "MetaS", "imdbr", "score"], ascending=[False, False, False, True]
)

Recommendations = pd.DataFrame()

Recommendations = Final_df.iloc[0:20, :]
#%% Sentence Matching

Recommendations = Recommendations.merge(
    imdb_data, how="left", left_on="Titles", right_on="title_x"
)
Recommendations = Recommendations.drop(
    [
        "title_x",
        "title_href",
        "mc_link",
        "genre0",
        "genre1",
        "genre2",
        "introduction",
        "title_y",
        "wiki_link",
    ],
    axis=1,
)
W_r = Recommendations["plot"].tolist()
for i in range(len(W_r)):
    # if pd.isnull(W_r[i])== "True":
    #     imdb_data_summary['plot'][i]= "Nothing"
    # else:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(W_r[i])

    tokens = [token for token in doc]
    tokens = [token.lemma_.lower().strip() for token in tokens]


    stopwords = set(STOP_WORDS)
    punctuations = string.punctuation

    tokens = [
        token
        for token in tokens
        if token.lower() not in stopwords and token not in punctuations
    ]
    # print((tokens))
    Recommendations["plot"][i] = tokens


nlp = spacy.load("en_core_web_sm")
doc = nlp(val)

tokens_cus = [token for token in doc]
tokens_cus = [token.lemma_.lower().strip() for token in tokens_cus]



stopwords = set(STOP_WORDS)
punctuations = string.punctuation

tokens_cus = [
    token
    for token in tokens_cus
    if token.lower() not in stopwords and token not in punctuations
]
# print((tokens))
customer_tokens = tokens_cus
b = set()
for i in customer_tokens:
    b.add(i)
match = []

for plot in Recommendations["plot"]:
    a = set(plot)
    match.append(len(a.intersection(b)) / float(len(b)))

Recommendations["ratios"] = match
Recommendations = Recommendations.sort_values("ratios", ascending=False)

print(Recommendations.head())
