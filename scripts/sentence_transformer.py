# import dependencies
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# @author: AIPI 540 Team #5


def similarity_search(query, df, model, doc_emb):
    """A sentence-transformer model - multi-qa-MiniLM-L6-cos-v1

    This is a sentence-transformers model: It maps sentences & paragraphs to a
    384 dimensional dense vector space and was designed for semantic search.
    It has been trained on 215M (question, answer) pairs from diverse sources.
    For an introduction to semantic search, have a look at: SBERT.net -
    Semantic Search. The multi-qa-MiniLM-L6-cos-v1 model will be used to
    conduct a similarity search for top 10 movie plot recommendations based
    on user query.
    https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1

    :param query: string input from user text
    :param df: DataFrame{title_x:str, plot:str}
    :param model: sentence_transformers.SentenceTransformer
    :param doc_emb: int containing doc embeddings

    :return: top 10 recommendations for similar movie plots based on user
    query.
    """
    sample = df[["title_x", "plot"]]
    titles = sample["title_x"].tolist()
    docs = sample["plot"].tolist()

    # Encode query and documents
    query_emb = model.encode(query)

    # Compute dot score between query and all document embeddings
    scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()

    # Combine docs & scores
    doc_score_pairs = list(zip(docs, scores, titles))

    # Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    # Output passages & scores
    print(f"Total Results:{len(doc_score_pairs)}")
    retVal = list()
    # only return top 10 matches
    for doc, score, title in doc_score_pairs[0:10]:  # pylint: disable=unused-variable
        retVal.append([title, score])
    return retVal


if __name__ == "__main__":
    # get preloaded model (see model.py)
    # from sentence_transformers import SentenceTransformer
    modelPath = (
        "../models/multi-qa-MiniLM-L6-cos-v1"  # "../models/multi-qa-MiniLM-L6-cos-v1"
    )
    stmodel = SentenceTransformer(modelPath)
    testdf = pd.read_csv("../data/outputs/finaldf.csv")
    print(similarity_search("1940", testdf, stmodel, None))
