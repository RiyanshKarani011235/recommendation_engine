import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import scipy.sparse as sp
from scipy.sparse.linalg import svds

#Reading users file:
from statsmodels.tools.eval_measures import rmse

u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('C:/Users/KEVIN/Downloads/movielens dataset/u.user', sep='|', names=u_cols,
encoding='latin-1')

#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
data = pd.read_csv('C:/Users/KEVIN/Downloads/movielens dataset/u.data', sep='\t', names=r_cols,
encoding='latin-1')
data_base = pd.read_csv('C:/Users/KEVIN/Downloads/movielens dataset/ua.base', sep='\t', names=r_cols,
encoding='latin-1')
data_test = pd.read_csv('C:/Users/KEVIN/Downloads/movielens dataset/ua.test', sep='\t', names=r_cols,
encoding='latin-1')


#Reading items file:
i_cols = ['movie_id', 'movie_title' ,'release_date','video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('C:/Users/KEVIN/Downloads/movielens dataset/u.item', sep='|', names=i_cols,
 encoding='latin-1')

#Creating training_ratings matrix:
n_users = users.user_id.unique().shape[0]
n_movies = movies.movie_id.unique().shape[0]

ratings = np.zeros((n_users, n_movies))
for row in data_base.itertuples():
    ratings[row[1]-1 , row[2] -1] = row[3]

ratings_matrix=pd.DataFrame(data=ratings,index=users['user_id'],columns=movies['movie_id'])
ratings_matrix=ratings_matrix.replace('0',np.nan)
#ratings_matrix.to_csv('C:/Users/KEVIN/Downloads/movielens dataset/ratings.csv', sep=' ', encoding='utf-8')

#Creating test_ratings_matrix
test_ratings= np.zeros((n_users, n_movies))
for row in data_test.itertuples():
    test_ratings[row[1]-1 , row[2] -1] = row[3]

#Creating user_gender_matrix:
user_gender_matrix=pd.DataFrame(0,index=users['user_id'],columns=['M','F'])
for row in users.itertuples():
    a=row[3]
    user_gender_matrix.loc[row[1],a]=1

#Creating user_occupation_matrix:
occupation=['administrator','artist','doctor','educator','engineer','entertainment','executive','healthcare','homemaker',
'lawyer','librarian','marketing','none','other','programmer','retired','salesman','scientist','student','technician','writer']
user_occupation_matrix=pd.DataFrame(0,index=users['user_id'],columns=occupation)
for row in users.itertuples():
    a=row[4]
    user_occupation_matrix.loc[row[1],a]=1

#Creating movie_genre_matrix:
df = movies.drop('IMDb_URL', 1)
df_1 = df.drop('movie_title', 1)
df_2= df_1.drop('release_date', 1)
df_3 = df_2.drop('video_release_date', 1)
df_4 = df_3.set_index('movie_id')
df_5 = df_4.transpose()

def extended_matrix(moviegenre_normalized,ratings_matrix1):
    weight=34
    moviegenre_normalized_weight = moviegenre_normalized * weight
    moviegenre_normalized_weight_transpose = moviegenre_normalized_weight.transpose()
    frames_new = [ratings_matrix1, moviegenre_normalized_weight_transpose]
    result_final = pd.concat(frames_new, axis=0)
    result_final=result_final.replace(np.nan,float(0))
   # matrix_factorization(result_final)

def multiplicativenormalization(ratings_matrix1):
    variable_genre_sum = df_5.sum(axis=1)
    variable_movies_sum = df_5.sum(axis=0)
    temp_1 = 1 / np.sqrt(variable_movies_sum.values) * df_5
    movie_genre_normalized = 1 / np.sqrt(variable_genre_sum.values) * temp_1.transpose()
    extended_matrix(movie_genre_normalized,ratings_matrix1)

def subtractive_normalization():
    user_mean=ratings_matrix.mean(axis=1)
    item_mean=ratings_matrix.mean(axis=0)
    overall_mean=ratings_matrix.mean().mean()
    '''r=pd.DataFrame(data=data_base.rating)
    r['user_avg']=0
    r['item_avg']=0
    r['overall_avg']=overall_mean
    final=sm.ols(formula="rating~overall_avg+user_avg+item_avg",data=r)
    final=final.fit()
    print(final.params)'''
    a = 0.3333
    b = 0.3333
    c = 0.3333
    ratings_matrix1= (ratings_matrix-(a*overall_mean)-(c*item_mean)).sub(b*user_mean,axis=0)
    multiplicativenormalization(ratings_matrix1)

def matrix_factorization(result_final):
    u, s, vt = svds(result_final, k=20)
    s_diag_matrix = np.diag(s)
    X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
    '''print(X_pred)
    print('User-based CF MSE: ' + str(rmse(X_pred, test_ratings)))'''

subtractive_normalization()


