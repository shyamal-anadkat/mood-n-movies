from transformers import pipeline
import pandas as pd


def _get_emotion_scores(clf, reviews):
    return clf(
        reviews,
    )


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

    rows_to_keep = [0, 3]
    reviews_data = pd.read_csv(
        "../data/raw/reviews_data_raw.csv", skiprows=lambda x: x not in rows_to_keep
    )
    print(reviews_data)
    reviews_data["emotion_scores_user_reviews"] = reviews_data["user_reviews"].apply(
        lambda x: _get_emotion_scores(classifier, x)
    )

    # print(reviews_data)
    # TO-DO: prediction for each user review and aggregate scores
    # reviews_data.to_csv('reviews_data_with_emotion_scores.csv', index=False)
