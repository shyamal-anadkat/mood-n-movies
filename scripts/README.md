Here's where we are housing all the scripts:

* `imdb_scraper.py` : this is the script that we're using to scrape the data for top 1000 movies on IMDB. 
* `metacritic_scraper.py`: this is the script we're using to scrape user/critic from Metacritic. Metacritic offers the most balanced aggregate score. If you don't mind which critics' opinions go into the final score and prefer seeing a general average, then you should use Metacritic. Its standards are mostly unknown, but Metacritic makes it easy to compare professional and user reviews side-by-side.
* `emotion_distilbert.py`: get emotion score inferences (for 6 moods) using Distilbert and save it to processed file
* `sentence_transformer.py`: similarity search using sentence transformer. Pretrained model -- maps sentences & paragraphs to a 384 dimensional dense vector space designed for semantic search.
* `clean_imdb_dataset.py`: cleans raw imdb dataset 
* `model.py`: saves sentence-transformers/multi-qa-MiniLM-L6-cos-v1 pretrained model for future use 
* `wiki_movie_scraper.py`: scrapes movie plots from wikipedia to be used by recommendation system
* `build_features.py`: merges processed datasets to creat the final output df
* `inference.py` & `app.py`: real-time inference helper and streamlit application script

### Non-Deep Learning Approach

<img width="1211" alt="image" src="https://user-images.githubusercontent.com/12115186/159188461-ae902742-4e60-4968-aba7-009a2e16c96f.png">

* `non-dl/classification_model.py` : this is one of the model types we experimented but havent got good results due to unequal distribution in the data
* `non-dl/final_non_dl_approach.py`: LDA approach is used in this model which gave better results compared to other models.
* `non-dl/multi_label_classification_check.py`: this script has code to show how the data is distributed showing how it is effecting the model to not perform very well using non-dl approach.

## Deep Learning Approach Flow

<img width="1324" alt="image" src="https://user-images.githubusercontent.com/12115186/159188430-7b7397d5-2c47-4ef8-b890-dd164e49e90a.png">

<img width="1321" alt="image" src="https://user-images.githubusercontent.com/12115186/159188439-f66ed929-bbc7-48ab-b78b-40daded1c93c.png">
