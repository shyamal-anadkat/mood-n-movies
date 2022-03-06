from transformers import pipeline
import pandas as pd

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
    prediction = classifier(
        "I love using transformers. The best part is wide range of support and its easy to use",
    )

    # TO-DO: prediction for each user review and aggregate scores

    print(prediction)
