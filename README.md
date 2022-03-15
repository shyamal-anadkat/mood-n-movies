[![build](https://github.com/shyamal-anadkat/AIPI540_NLP/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/shyamal-anadkat/AIPI540_NLP/actions/workflows/main.yml)

# Mood & Movies <br/>
> Better movie recommendations, based on your mood
#### AIPI 540 NLP Team Project | Spring Semester 2022

**Team Members:** Shyamal Anadkat, Hearsch Jariwala, Snigdha Rudraraju

**Project:** Building NLP based movie recommendation web application based on mood & user query/free text input. 

## Getting Started

### Running the Application (User Interface)

Run the Streamlit interface from root of the project: `streamlit run app.py`
- Note the pre-loading would take ~2mins on CPU but after the pre-loading the recommendation search would be quick.

### Contributing (_detailed_)

 1. Update `imdb_scraper.py` as necessary to scrape additional movie lists from IMDB; ensure the output csv gets persisted
to `data/raw` as `data/raw/imdb_top_1000_lang_en.csv`
 2. Clean the IMDB data from (1) by executing `clean_imdb_dataset.py`; the cleaned output file will be saved in `data/processed`
 3. Using the cleaned IMDB data as input, execute `metacritic_scraper.py` to scrape the Metacritic user/critic reviews;
the resulting reviews data will be persisted to `data/raw/reviews_data_raw.csv`
 4. Using the cleaned IMDB data as input, execute `wiki_movie_scraper.py` to scrape the Wikipedia movie plots which will
be used for semantic search as part of the recommendation system. The output of this will be saved in `data/processed/with_plot_summary.csv`
Now we have all data from IMDB for the movie list, the corresponding metacritic user/critic reviews, and movie plots from Wiki.
 5. Execute `emotion_distilbert.py` next using the `reviews_data_raw` as input in order to tag reviews with corresponding 
emotion scores, using the user reviews. Distilbert-base-uncased is finetuned on the emotion dataset. 
The output will be saved as `data/processed/reviews_data_with_emotion_scores.csv`
 6. Next, the aggregated emotion scores for each movie will be calculated by executing `make_dataset.py`; the output will be saved
as `data/processed/reviews_data_with_aggregate_emotion_scores.csv`
 7. Finally, `model.py` and `sentence_transformer.py` is where we implement our pipeline around similarity/semantic search. 
The pre-trained sentence-transformers model is saved within `models/` by executing `model.py`
 8. Next, the final dataframe used for outputting recommendations is aggregated using `build_features.py` 
 9. `inference.py` houses the main `get_reccs(finaldf, in_mood, in_query, stmodel, doc_emb)` method which takes in the 
`finaldf` from step 8 (`build_features.py`), the user's input mood, the user's input query, and the pre-computed document embeddings 
for the wikipedia plots. The output for this method is a list of top 10 movie recommendations. 
 10. `app.py` is the main streamlit application which calls `get_reccs(...)` from `inference.py`. 
The sentence transformer model is pre-loaded from `models/multi-qa-MiniLM-L6-cos-v1` and cached. Consequently,
the document embeddings for the movie plots are calculated in `preload()` and cached for faster real-time inference.


**Before pushing any code:**

* Run `make clean` before pushing your code (which will format and do the linting for you)
* Please ensure the build on github passes after you merge your code to master/push your commit 

### UI Screenshot

![Screen Shot 2022-03-11 at 6 10 00 PM](https://user-images.githubusercontent.com/12115186/158288113-06eaf36d-0ad1-4d2a-aee1-a84a7ffe16aa.png)



## Project Structure 

```
├── README.md               <- description of project and how to set up and run it
├── requirements.txt        <- requirements file to document dependencies
├── Makefile                <- setup and run project from command line
├── app.py                  <- main script to run user interface
├── scripts                 <- directory for pipeline scripts or utility scripts (see scripts/README.md)
├── models                  <- directory for trained model
├── data                    <- directory for project data
    ├── raw                 <- directory for raw data or script to download
    ├── processed           <- directory to store processed data
    ├── outputs             <- directory to store any output data
├── notebooks               <- directory to store any exploration notebooks used
├── .gitignore              <- git ignore file
```
Documentation for [scripts](https://github.com/shyamal-anadkat/mood-n-movies/blob/master/scripts/README.md)

## Deep Learning Pipeline Overview 

<img width="1245" alt="image" src="https://user-images.githubusercontent.com/12115186/158284817-0287b006-501d-4078-a089-b4de7861818d.png">



