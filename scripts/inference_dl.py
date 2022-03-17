from scripts.sentence_transformer import similarity_search
from ast import literal_eval


def get_score(mood, agg_score):
    res = list(literal_eval(agg_score))
    scores = [d[mood] for d in res if mood in d]
    score = scores[0]
    return score


def get_mapped_mood(in_mood):
    """
    Gets mapped mood from user mood
    :param in_mood:
    :return:
    """
    # mood_list = ["sadness", "joy", "love", "fear", "surprise", "anger"]
    if in_mood == "sadness":
        return "joy"
    elif in_mood == "joy":
        return "joy"
    elif in_mood == "love":
        return "love"
    elif in_mood == "anger":
        return "love"
    elif in_mood == "fear":
        return "fear"
    elif in_mood == "surprise":
        return "surprise"


def get_reccs(finaldf, in_mood, in_query, stmodel, doc_emb):
    """
    Get recommendations from final dataframe, input mood, model, doc embeddings, and input query
    :param finaldf:
    :param in_mood:
    :param in_query:
    :param stmodel:
    :param doc_emb:
    :return:
    """
    finaldf["aggregate_score"] = finaldf["aggregate_score"].tolist()
    mapped_mood = get_mapped_mood(in_mood)
    print(f"Recommending {mapped_mood} movies")
    finaldf["mood_score"] = finaldf["aggregate_score"].apply(
        lambda score: get_score(mapped_mood, score)
    )

    # takes 100/200 largest by mood score for that particular mood
    srted = finaldf.nlargest(
        200, "mood_score"
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
