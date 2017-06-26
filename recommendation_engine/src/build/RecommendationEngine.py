# coding: utf-8

# imports
import pandas as pd
import numpy as np
import statsmodels.formula.api as sm
import scipy.sparse as sp
from scipy.sparse.linalg import svds
import os
import random
import ast

'''---------------'''
'''   FILENAMES   '''
'''---------------'''
similarity_matrix_file = os.path.join('cache', 'similarity_matrix.txt')

'''---------------'''
'''LOADING DATASET'''
'''---------------'''

# dataset root
root_dataset_folder = os.path.join('data', 'ml-100k')

# u.user (Users)
user_columns = [
	'user_id', 
	'age', 
	'sex', 
	'occupation', 
	'zip_code'
]
users = pd.read_csv(os.path.join(root_dataset_folder, 'u.user'), sep='|', names=user_columns, encoding='latin-1')

# u.items (Movies)
movie_columns = [
	'movie_id', 
	'movie_title' ,
	'release_date',
	'video_release_date', 
	'IMDb_URL', 
	'unknown', 
	'Action', 
	'Adventure', 
	'Animation', 
	'Children\'s', 
	'Comedy', 
	'Crime', 
	'Documentary', 
	'Drama', 
	'Fantasy', 
	'Film-Noir', 
	'Horror', 
	'Musical', 
	'Mystery', 
	'Romance', 
	'Sci-Fi', 
	'Thriller', 
	'War',
	'Western'
]
movies = pd.read_csv(os.path.join(root_dataset_folder, 'u.item'), sep='|', names=movie_columns, encoding='latin-1')

'''-----------------------------'''
'''CREATING SPARSE RATING MATRIX'''
'''-----------------------------'''
print('loading sparse rating matrix ...')

M = users.user_id.unique().shape[0]
N = movies.movie_id.unique().shape[0]

ratings = np.zeros((M, N))
# reading ratings from 
# (Ratings)
rating_columns = [
	'user_id', 
	'movie_id', 
	'rating', 
	'unix_timestamp'
]
# ua.base
data_base = pd.read_csv(os.path.join(root_dataset_folder, 'ua.base'), sep='\t', names=rating_columns, encoding='latin-1')

for row in data_base.itertuples():
	ratings[row[1]-1 , row[2] -1] = row[3]

sparse_rating_matrix = pd.DataFrame(data=ratings,index=users['user_id'],columns=movies['movie_id'])
sparse_rating_matrix = sparse_rating_matrix.replace('0',np.nan)
sparse_rating_matrix = sparse_rating_matrix.values

def load_similarity_matrix() : 
	if os.path.exists(similarity_matrix_file) : 
		print('loading cached copy of similarity matrix ...')
		with open(similarity_matrix_file, 'r') as f : 
			return np.array(ast.literal_eval(f.read()))
	else : 
		'''-----------------'''
		'''LINEAR REGRESSION'''
		'''-----------------'''
		print('running linear regressinon ...')

		Y = []
		X = []
		mean = np.nanmean(sparse_rating_matrix)
		for m in range(M) : 
			for n in range(N) : 
				if not np.isnan(sparse_rating_matrix[m][n]) : 
					Y.append(sparse_rating_matrix[m][n] - mean)
					x = np.zeros(M+N)
					x[m] = 1
					x[M + n] = 1
					X.append(x)
		X = np.array(X)
		Y = np.array(Y)

		lambda_ = 0.1
		X_transpose = np.transpose(X)
		t1 = np.linalg.inv(np.dot(X_transpose, X) - (lambda_*np.identity(X.shape[1])))
		t2 = np.dot(X_transpose, Y)
		b = np.dot(t1, t2)

		b_u = b[:M]
		b_i = b[M:]

		'''-----------------'''
		'''SIMILARITY MATRIX'''
		'''-----------------'''
		print('generating similarity matrix ...')

		movies = pd.read_csv(os.path.join(root_dataset_folder, 'u.item'), sep='|', names=movie_columns, encoding='latin-1')
		genre_matrix = movies.drop('movie_id', 1).drop('movie_title', 1).drop('release_date', 1).drop('video_release_date', 1).drop('IMDb_URL', 1).drop('unknown', 1)

		# CONSTANTS
		w1 = 1.0
		w2 = 0.675
		ZEROS_SIMILARITY_VALUE = 0.3

		print('\tgenerating g matrix ...')
		g_matrix = genre_matrix.values
		g = np.array([np.array([0.0 for i in range(g_matrix.shape[1])]) for j in range(g_matrix.shape[1])])
		count = 0
		for movie_genres in g_matrix : 
			for i in range(len(movie_genres)) :
				for j in range(i+1, len(movie_genres)) : 
					ij = (movie_genres[i], movie_genres[j])
					if ij == (0, 1) or ij == (1, 0) :
						g[i][j] -= w2 * 1.0
					elif ij == (1, 1) : 
						g[i][j] += w1 * 1.0
					elif ij == (0, 0) : 
						g[i][j] += ZEROS_SIMILARITY_VALUE
					count += 1.0
					
		max_val = max(g.min(), g.max(), key=abs)
		for i in range(len(g)) : 
			for j in range(len(g)) : 
				g[i][j] /= max_val

		print('\tgenerating G matrix ...')
		G = np.array([np.array([0.0 for i in range(g_matrix.shape[0])]) for j in range(g_matrix.shape[0])])
		def G_ij(i, j) : 
			sum_ = 0
			genre_matrix_i = g_matrix[i]
			genre_matrix_j = g_matrix[j]
			count = 0
			for m in range(len(genre_matrix_i)) :
				ei = genre_matrix_i[m]
				if ei : 
					for n in range(len(genre_matrix_j)) :
						ej = genre_matrix_j[n]
						if ej : 
							sum_ += g[m][n]
							count += 1
			if count is not 0 : 
				sum_ /= count
			return sum_

		for i in range(len(g_matrix)) : 
			for j in range(i+1, len(g_matrix)) : 
				G[i][j] = G_ij(i,j)

		print('\tgenerating n matrix ...')
		n = np.zeros((sparse_rating_matrix.shape[1], sparse_rating_matrix.shape[1]))
		for i in range(sparse_rating_matrix.shape[1]) : 
			for j in range(i+1, sparse_rating_matrix.shape[1]) : 
				R_i = sparse_rating_matrix[:, i]
				R_j = sparse_rating_matrix[:, j]
				R_i = np.nan_to_num(R_i)
				R_j = np.nan_to_num(R_j)
				R_i[R_i != 0] = 1
				R_j[R_j != 0] = 1
				n[i][j] = np.dot(R_i, R_j)
				
		def r(u, i) : 
			return sparse_rating_matrix[u][i]

		# r_i
		r_i_value = sparse_rating_matrix.mean(axis=0).tolist()
		def r_i(u) : 
			return r_i_value[u]

		print('\tgenerating rho matrix ...')
		rho = np.zeros((sparse_rating_matrix.shape[1], sparse_rating_matrix.shape[1]))
		for i in range(sparse_rating_matrix.shape[1]) : 
			for j in range(i+1, sparse_rating_matrix.shape[1]) : 
				num = 0
				R_i = sparse_rating_matrix[:, i]
				R_i = R_i - np.nanmean(R_i, axis=0)
				R_j = sparse_rating_matrix[:, j]
				R_j = R_j - np.nanmean(R_j, axis=0)
				R_i = np.nan_to_num(R_i)
				R_j = np.nan_to_num(R_j)
				numerator = np.dot(R_i, R_j)
				denominator = np.dot(R_i, R_i) * np.dot(R_j, R_j)
				val = numerator/denominator
				if np.isnan(val) : 
					rho[i][j] = 0
				else :     
					rho[i][j] = val

		print('\tgenerating rho_ matrix ...')
		w1 = 1
		w2 = 1
		rho_ = (w1*rho) + (w2*G)

		print('\tfinal touches ...')
		lambda_2 = 0
		s = (n/(n + 1)) * rho_

		print('caching similarity matrix ...')
		with open(similarity_matrix_file, 'w') as f : 
			f.write(str(s.tolist()))
		return s

'''--------------'''
'''RECOMMENDATION'''
'''--------------'''

sparse_rating_matrix = pd.DataFrame(data=ratings,index=users['user_id'],columns=movies['movie_id'])
sparse_rating_matrix = sparse_rating_matrix.replace('0',np.nan)
sparse_rating_matrix = sparse_rating_matrix.values

s = load_similarity_matrix()

def k_max_indices(array, k) : 
	return_array = []
	for i in range(k) : 
		max_ = -1000
		max_index = -1
		for j in range(len(array)) : 
			if array[j] > max_ and j not in return_array : 
				max_ = array[j]
				max_index = j
		return_array.append(max_index)
	return return_array

def knn(k, i) :
	row = s[i][i+1:].tolist()
	array = s[:,i][:i].tolist()
	array.append(0)
	array.extend(row)
	return k_max_indices(array, k)

def recommend(user_id) : 
	user_rating_matrix = sparse_rating_matrix[user_id]
	user_rating_matrix[user_rating_matrix == np.nan] = 0
	max_user_rating_matrix = k_max_indices(user_rating_matrix, 5)
	m = []
	for element in max_user_rating_matrix : 
		m.extend([[element, e] for e in knn(5, element)])
	m_ = [s[u,v] for u,v in m]
	m_ = k_max_indices(m_, 15)[7:12]
	m = [m[element] for element in m_]
	recommended_movies_array = []
	with open(os.path.join(root_dataset_folder, 'u.item'), 'r') as f : 
		data = f.read().split('\n')
		for movie in m : 
			recommended_movies_array.append(data[movie[1]].split('|')[1])
	return recommended_movies_array

print('RecommendationEngine.py loaded')
