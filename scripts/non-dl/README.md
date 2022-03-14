Here is the process followed in non-dl approach

* `Data Processing` : Got all the data(movie names, IMDB rating, Metacritic rating, introduction, genre, plot summary to a single dataframe and cleaned the data
* `Mood ---> Genre`: Assigned a genre manually to different moods as follows 
*                                                     `Joy` :Action,Adventure, Fantasy,Scifi
                                                      `Sadness` :Comedy
                                                      `Surprise` :Crime,Thriller,Mystery
                                                      `Anger` :Family
                                                      `Fear` :Horror
                                                      `Love` :Drama

* 
* `non-dl/multi_label_classification_check.py`: this script has code to show how the data is distributed showing how it is effecting the model to not perform very well using non-dl
