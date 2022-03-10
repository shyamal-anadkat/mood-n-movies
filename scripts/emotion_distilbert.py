from transformers import pipeline
import pandas as pd


def _get_emotion_scores(clf, reviews):
    review_list = reviews.split("</review>")
    scores = []
    for review in review_list[:-1]:
        cleaned_text = review.replace("<review>", "").replace("[", "").replace("]", "")
        # print(len(cleaned_text.split()))
        score = clf(cleaned_text, truncation=True, max_length=512)
        scores.append(score)
    return scores


if __name__ == "__main__":
    # Distilbert is created with knowledge distillation during the pre-training phase which reduces the size of a BERT model
    # by 40%, while retaining 97% of its language understanding. It's smaller, faster than Bert and any other Bert-based model.
    # Distilbert-base-uncased finetuned on the emotion dataset using HuggingFace Trainer with below Hyperparameters:
    # learning rate 2e-5,
    # batch size 64,
    # num_train_epochs=8,
    classifier = pipeline(
        "text-classification",
        model="bhadresh-savani/distilbert-base-uncased-emotion",
        return_all_scores=True,
    )

    reviews_data = pd.read_csv("../data/raw/reviews_data_raw.csv")
    reviews_data["emotion_scores_user_reviews"] = reviews_data["user_reviews"].apply(
        lambda x: _get_emotion_scores(classifier, x)
    )

    # TO DEBUG: print(reviews_data)
    # TO-DO: prediction for each user review and aggregate scores
    reviews_data = reviews_data[
        ["mc_link", "title", "num_user_reviews", "emotion_scores_user_reviews"]
    ]
    path = "../data/processed/reviews_data_with_emotion_scores.csv"
    reviews_data.to_csv(path, index=False)
    print(f":: All done. Saved in {path} ::")
