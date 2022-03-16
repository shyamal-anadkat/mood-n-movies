# import dependencies
import pandas as pd
from ast import literal_eval


def safe_div(x, y):
    """Allows division of undefined to be 0.

    The function checks to see if division by 0 is occurring and lets the
    value return 0 or proceed further.

    :param x: float containing the emotion score
    :param y: float containing total reviews score

    :return: float value containing calculated score or 0.
    """
    if y == 0:
        return 0
    return x / y


def calculate_aggregate(scores):
    """Calculate user reviews aggregated movie's overall emotion score.

    Finds each of the user review emotion scores and then aggregates it to
    give overall emotion score for that labeled movie.

    :param scores: DataFrame with emotion scores for user reviews

    :return: the aggregated emotion scores for movies based off user reviews.
    """
    data = literal_eval(scores)
    sadness = joy = love = anger = fear = surprise = 0
    total_reviews = len(data)
    for score in data:
        labels = score[0]
        # print(labels)
        for label in labels:
            if label["label"] == "sadness":
                sadness += label["score"]
            elif label["label"] == "joy":
                joy += label["score"]
            elif label["label"] == "love":
                love += label["score"]
            elif label["label"] == "anger":
                anger += label["score"]
            elif label["label"] == "fear":
                fear += label["score"]
            elif label["label"] == "surprise":
                surprise += label["score"]
    agg = [
        {"sadness": safe_div(sadness, total_reviews)},
        {"joy": safe_div(joy, total_reviews)},
        {"love": safe_div(love, total_reviews)},
        {"anger": safe_div(anger, total_reviews)},
        {"fear": safe_div(fear, total_reviews)},
        {"surprise": safe_div(surprise, total_reviews)},
    ]
    return agg


if __name__ == "__main__":
    emotion_scores = pd.read_csv(
        "../data/processed/reviews_data_with_emotion_scores.csv"
    )
    emotion_scores.emotion_scores_user_reviews = (
        emotion_scores.emotion_scores_user_reviews.to_list()
    )
    # pylint: disable=unsubscriptable-object
    # pylint: disable=unnecessary-lambda
    # pylint: disable=unsupported-assignment-operation)
    emotion_scores["aggregate_score"] = emotion_scores[
        "emotion_scores_user_reviews"
    ].apply(lambda x: calculate_aggregate(x))
    path = "../data/processed/reviews_data_with_aggregate_emotion_scores.csv"
    emotion_scores.to_csv(path, index=False)
    print(f":: All done. Saved in {path} ::")
