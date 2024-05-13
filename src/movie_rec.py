import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
import difflib
from utils.helper_func import get_closest_matches


def data_prep():
    movies = pd.read_csv("./data/movies.csv")
    movies['title'] = movies['title'].str.replace(
        r"\s\(\d{4}\)", "", regex=True)

    ratings = pd.read_csv("./data/ratings.csv")
    final_dataset = ratings.pivot(
        index='movieId', columns='userId', values='rating')
    final_dataset.fillna(0, inplace=True)
    no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
    no_movies_voted = ratings.groupby('userId')['rating'].agg('count')
    final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]
    final_dataset = final_dataset.loc[:,
                                      no_movies_voted[no_movies_voted > 50].index]
    sample = np.array([[0, 0, 3, 0, 0], [4, 0, 0, 0, 2], [0, 0, 0, 0, 1]])
    sparsity = 1.0 - (np.count_nonzero(sample) / float(sample.size))
    return final_dataset, sample, sparsity, movies


def create_model(sample: np.array, final_dataset: pd.DataFrame):
    csr_sample = csr_matrix(sample)
    csr_data = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)
    knn = NearestNeighbors(
        metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    knn.fit(csr_data)
    return csr_data, knn


def get_movie(movie_name, movies: pd.DataFrame):
    # print(movie_name)
    movie = movies[movies['title'].str.lower() == movie_name.lower()]
    print("he")
    if len(movie) == 0:
        # movie = movies[movies['title'].str.lower().str.contains(
        #     movie_name.lower())]
        # if len(movie) != 0:
        #     # make movie the least len(title) out of all movies
        #     movie = movie[movie['title'].str.len(
        #     ) == movie['title'].str.len().min()]
        #     print("hi")
        #     print(movie)

        # else:
        movie = get_closest_matches(movie_name, movies, 'title')
        print(movie)
        print("ho")

    # print(movie)
    return movie


def get_movie_recommendation(movie_name, final_dataset: pd.DataFrame, movies: pd.DataFrame, csr_data: csr_matrix, knn: NearestNeighbors):
    n_movies_to_reccomend = 10

    movie_list = get_movie(movie_name, movies)
    # movie id list
    movie_id_list = []

    for i in range(len(movie_list)):
        movie_idx = movie_list.iloc[i]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx]
        if movie_idx.empty:
            continue
        else:
            movie_idx = movie_idx.index[0]
            distances, indices = knn.kneighbors(
                csr_data[movie_idx], n_neighbors=n_movies_to_reccomend+1)
            rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(
            ), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
            recommend_frame = []
            for val in rec_movie_indices:
                movie_idx = final_dataset.iloc[val[0]]['movieId']
                movie_id_list.append(movie_idx)
                idx = movies[movies['movieId'] == movie_idx].index
                recommend_frame.append(
                    {'Title': movies.iloc[idx]['title'].values[0], 'Distance': val[1]})
            df = pd.DataFrame(recommend_frame, index=range(
                1, n_movies_to_reccomend+1))
            return movie_id_list

    return None


# use case
# final_dataset, sample, sparsity, movies = data_prep()
# csr_data, knn = create_model(sample, final_dataset)

# r = get_movie_recommendation('Toy story', final_dataset, movies, csr_data, knn)
# r
