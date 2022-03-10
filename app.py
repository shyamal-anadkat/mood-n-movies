import streamlit as st
from scripts.inference_dl import get_reccs

# streamlit run app.py
input_text = st.text_input(
    "What do you want to watch?", "I like Gotham City", max_chars=250
)
st.write("You typed: ", input_text)

mood = st.selectbox(
    "How would you like to feel?:",
    ("sadness", "joy", "love", "fear", "surprise", "anger"),
)
st.write("You selected:", mood)

if st.button("Recommend me some movies!"):
    # st.write(input_text, mood)
    recommendations = get_reccs(mood, input_text)
    st.write(
        "Here are your top 10 movie recommendations for today:"
    )  # displayed when the button is clicked
    st.write(recommendations)
