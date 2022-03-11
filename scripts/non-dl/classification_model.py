#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 16:05:05 2022

@author: snigdharudraraju
"""

import pandas as pd
import smart_open
import spacy
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

#!python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

import gensim

import warnings

warnings.filterwarnings("ignore")

imdb_data = pd.read_csv("../../data/processed/IMDB_top_1000_clean.csv")
Plot_summary = pd.read_csv("../../data/processed/with_plot_summary.csv")
imdb_data = imdb_data.merge(
    Plot_summary, how="left", left_on="mc_link", right_on="mc_link"
)
Working_df = pd.DataFrame()
# Working_df["Plot"]=imdb_data["plot"]
# Working_df["Movie_name"]=imdb_data["title_x"]
# Working_df["genre_new"]=imdb_data["genre"]
movies = imdb_data["title_x"]
moviesList = []
plotList = []
for movie in movies:
    for j in range(len(Plot_summary["title"])):
        if movie in Plot_summary["title"][j]:
            moviesList.append(movie)
            plotList.append(Plot_summary["plot"][j])
Working_df["Movie"] = moviesList
Working_df["Plot"] = plotList
Working_df = Working_df.merge(
    imdb_data, how="left", left_on="Movie", right_on="title_x"
)
Working_df = Working_df.drop(
    ["certificate", "votes", "directors", "stars", "runtime", "produce_year"], axis=1
)
Working_df = Working_df.drop(
    ["title_x", "title_href", "mc_link", "introduction"], axis=1
)
Working_df = Working_df.drop(["plot", "title_y", "wiki_link"], axis=1)

genre3 = Working_df["genre"].str.split(",", expand=True)


Working_df["genre0"] = genre3[0]
Working_df["genre1"] = genre3[1]
Working_df["genre2"] = genre3[2]

for i in range(len(Working_df["genre1"])):
    if Working_df["genre1"][i] == None:
        Working_df["genre1"][i] = Working_df["genre0"][i]

for i in range(len(Working_df["genre1"])):
    if Working_df["genre2"][i] == None:
        Working_df["genre2"][i] = Working_df["genre0"][i]


def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for x, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [x])


def read_corpus_from_list(lst, tokens_only=False):
    for y, line in enumerate(lst):
        tokens = gensim.utils.simple_preprocess(line)
        if tokens_only:
            yield tokens
        else:
            # For training data, add tags
            yield gensim.models.doc2vec.TaggedDocument(tokens, [y])


xtrain, xtest, ytrain, yval = train_test_split(
    Working_df["Plot"], Working_df["genre1"], test_size=0.2, random_state=0
)
corpus = list(read_corpus_from_list(Working_df["Plot"].tolist()))

train_tokens = list(read_corpus_from_list(xtrain.tolist(), tokens_only=True))
test_tokens = list(read_corpus_from_list(xtest.tolist(), tokens_only=True))

doc2vec_model = gensim.models.doc2vec.Doc2Vec(
    vector_size=25, min_count=2, dbow_words=0, epochs=20
)
doc2vec_model.build_vocab(corpus)
doc2vec_model.train(
    corpus, total_examples=doc2vec_model.corpus_count, epochs=doc2vec_model.epochs
)

X_train = [doc2vec_model.infer_vector(doc) for doc in train_tokens]
X_test = [doc2vec_model.infer_vector(doc) for doc in test_tokens]


logreg_model = LogisticRegression(solver="saga")
logreg_model.fit(X_train, ytrain)
preds = logreg_model.predict(X_train)
acc = sum(preds == ytrain) / len(ytrain)
print("Accuracy on the training set is {:.3f}".format(acc))
