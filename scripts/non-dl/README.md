Here is the process followed in non-dl approach

* `Data Processing` : Got all the data(movie names, IMDB rating, Metacritic rating, introduction, genre, plot summary to a single dataframe and cleaned the data
* `Mood ---> Genre`: Assigned a genre manually to different moods as follows 
*  ```
├── Joy                     <- Action,Adventure,Fantasy,Sci-Fi
├── Sadness                 <- Comedy
├── Surprise                <- Crime,Thriller,Mystery
├── Anger                   <- Family
├── Fear                    <- Horror
├── Love                    <- Drama

```
* `Genre mapping`: We have compared the genres classified based on movies to genres classified in the input data by IMDB

* `LDA topic modeling`: We take input from the user as to describe the movie they want to watch after selecting the mood. The movvies in the input data are classified into certain topics based on LDA unsupervised approach. We also use the same on the input user is providing and compare the scores using MSE to see the closest mapping. 

* `Sentence Mapping`: We have done tokenization, lemmatization and removed stop words from the plot summary and the input given by the user. Now we see how many common words are there between plot summary and input. this ratio is used to filter the best match
