import pandas as pd
import numpy as np
# pass in column names for each CSV

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('C:/Users/KEVIN/Downloads/BE project/new user dataset/ratings.csv', sep=',', names=r_cols,
                      encoding='latin-1')
# the movies file contains columns indicating the movie's genres
# let's only load the first five columns of the file with usecols
i_cols = ['movie_id', 'movie_title' ,'genres' ]
movies = pd.read_csv('C:/Users/KEVIN/Downloads/BE project/new user dataset/movies.csv', sep=',', names=i_cols,
 encoding='latin-1',index_col='movie_id')
#print(movies.loc[1].movie_title)
#print(movies)

k=[]
count=0