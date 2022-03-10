from scripts.sentence_transformer import similarity_search
from ast import literal_eval


def get_score(mood, agg_score):
    res = list(literal_eval(agg_score))
    scores = [d[mood] for d in res if mood in d]
    score = scores[0]
    return score


def get_reccs(finaldf, in_mood, in_query, stmodel, doc_emb):
    finaldf["aggregate_score"] = finaldf["aggregate_score"].tolist()
    finaldf["mood_score"] = finaldf["aggregate_score"].apply(
        lambda score: get_score(in_mood, score)
    )

    # takes 100 largest by mood score for that particular mood
    srted = finaldf.nlargest(
        100, "mood_score"
    )  # https://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.nlargest.html

    # srted.to_csv("test.csv", index=False)

    # based on input mood, get the 10 highest scores for love across finaldf aggregate_score
    retVal = similarity_search(in_query, srted, stmodel, doc_emb)
    reccs = list()
    for title, score in retVal:  # pylint: disable=unused-variable
        reccs.append(title)
    return reccs


if __name__ == "__main__":
    mood_list = ["sadness", "joy", "love", "fear", "surprise", "anger"]
    input_mood = "love"
    input_query = "romance at the beach"
    # uncomment for testing
    # reccomendations = get_reccs(input_mood, input_query)
    # print(reccomendations)
