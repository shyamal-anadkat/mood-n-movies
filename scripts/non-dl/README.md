Here is the process followed in non-dl approach

## Data Processing
* Got all the data to a single dataframe(Movies,plot summary, IMDB rating,Metacritic rating,Genre) and cleaned the data

## Mood ---> Genre
* Assigned a genre manually to different moods as follows 
```
├── Joy                     <- Action,Adventure,Fantasy,Sci-Fi
├── Sadness                 <- Comedy
├── Surprise                <- Crime,Thriller,Mystery
├── Anger                   <- Family
├── Fear                    <- Horror
├── Love                    <- Drama
```

## Genre Mapping
* We have compared the genres classified based on movies to genres classified in the input data by IMDB

## LDA Topic Modeling
* We take input from the user  to describe the movie they want to watch after selecting the mood. 
* All the movies in the input data are classified into certain topics based on LDA unsupervised approach.
* We use the same modeling on the input user has provided and compare the scores using MSE to see the closest mapping. 

## Sentence Mapping
* We did tokenization, lemmatization and removed stop words from the plot summary and the input given by the user. 
* We then calculated ratio between number of common words to number of words in input. this ratio is used to filter the best match

## How to run it!!!!
* Run the final_non_dl_approach.py file
* Enter what movie you want to watch. For example - " I like to watch a movie where a person teleports to space using a spaceship "
* Enter your mood from the 6 moods mentioned
* Just wait.....
