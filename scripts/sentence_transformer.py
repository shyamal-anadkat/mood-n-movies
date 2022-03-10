import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load the model
# https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1

# This is a sentence-transformers model: It maps sentences & paragraphs to a 384 dimensional dense vector space and was
# designed for semantic search. It has been trained on 215M (question, answer) pairs from diverse sources.
# For an introduction to semantic search, have a look at: SBERT.net - Semantic Search

# get preloaded model (see model.py)
# from sentence_transformers import SentenceTransformer
modelPath = "../models/multi-qa-MiniLM-L6-cos-v1"
model = SentenceTransformer(modelPath)

df = pd.read_csv("../data/processed/with_plot_summary.csv")
sample = df[["title", "plot", "mc_link"]]

query = "rich kid"
titles = sample["title"].tolist()
docs = sample["plot"].tolist()

# Encode query and documents
query_emb = model.encode(query)
doc_emb = model.encode(docs)

# Compute dot score between query and all document embeddings
scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()

# Combine docs & scores
doc_score_pairs = list(zip(docs, scores, titles))

# Sort by decreasing score
doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

# Output passages & scores
print(f"Total Results:{len(doc_score_pairs)}")
for doc, score, title in doc_score_pairs[0:20]:
    print(title, score, doc)
