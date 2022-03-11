import streamlit as st
import pandas as pd
from scripts.inference_dl import get_reccs
from sentence_transformers import SentenceTransformer
import copy

# streamlit run app.py


@st.cache
def preload():
    df = pd.read_csv("data/outputs/finaldf.csv")
    # get preloaded model (see model.py)
    # from sentence_transformers import SentenceTransformer
    modelPath = (
        "models/multi-qa-MiniLM-L6-cos-v1"  # "../models/multi-qa-MiniLM-L6-cos-v1"
    )
    model = SentenceTransformer(modelPath)
    emb = model.encode(df["plot"].tolist())
    return df, model, emb


input_text = st.text_input(
    "What do you want to watch?", "I like Gotham City", max_chars=250
)
st.write("You typed: ", input_text)

mood = st.selectbox(
    "What mood are you in ?",
    ("sadness", "joy", "love", "fear", "surprise", "anger"),
)
st.write("You selected:", mood)
finaldf, stmodel, plots_emb = copy.deepcopy(preload())

if st.button("Recommend me some movies!"):
    # st.write(input_text, mood)
    if mood == "sadness" or mood == "anger":
        input_text = "comedy " + input_text
    print(f"Input Text: {input_text}")
    recommendations = get_reccs(
        finaldf, in_mood=mood, in_query=input_text, stmodel=stmodel, doc_emb=plots_emb
    )
    st.write(
        "Here are your top 10 movie recommendations for today:"
    )  # displayed when the button is clicked
    st.write(recommendations)
