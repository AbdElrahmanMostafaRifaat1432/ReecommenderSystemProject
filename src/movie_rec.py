

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


def data_prep():
    movie = pd.read_csv("./data/movies.csv")
    rating = pd.read_csv("./data/ratings.csv")
    data = pd.merge(movie, rating)
    data.drop(["genres", "timestamp"], axis=1, inplace=True)
    data_pivot = data.pivot_table(
        index='userId', columns='title', values='rating')
    data_pivot2 = pd.pivot(index="movieId", columns="userId",
                           data=rating, values="rating")
    Movie_voted = pd.DataFrame(rating.groupby("movieId")[
                               "rating"].agg("count"))
    Movie_voted.reset_index(level=0, inplace=True)
    User_Voted = pd.DataFrame(rating.groupby("userId")["rating"].agg("count"))
    User_Voted.reset_index(level=0, inplace=True)
    data_pivot2.fillna(0, inplace=True)
    dataLast = data_pivot2.loc[Movie_voted[Movie_voted["rating"]
                                           > 10]["movieId"], :]
    dataLast = dataLast.loc[:, User_Voted[User_Voted["rating"] > 60]["userId"]]
    return dataLast, movie, data_pivot


def movie_recommendation(movie_name, dataLast, movie, n_movies_to_reccomend=10):
    csr_data = csr_matrix(dataLast.values)
    dataLast.reset_index(inplace=True)
    knn = NearestNeighbors(metric='cosine', algorithm='brute',
                           n_neighbors=20, n_jobs=-1)
    knn.fit(csr_data)
    movie_list = movie[movie['title'].str.contains(
        movie_name)]  # Fint movie name

    if len(movie_list):

        movie_idx = movie_list.iloc[0]['movieId']
        movie_idx = dataLast[dataLast['movieId'] == movie_idx].index[0]

        distances, indices = knn.kneighbors(
            csr_data[movie_idx], n_neighbors=n_movies_to_reccomend+1)
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(
        ), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        recommend_frame = []

        for val in rec_movie_indices:
            movie_idx = dataLast.iloc[val[0]]['movieId']
            idx = movie[movie['movieId'] == movie_idx].index
            recommend_frame.append(
                {'Title': movie.iloc[idx]['title'].values[0], 'Distance': val[1]})
        df = pd.DataFrame(recommend_frame, index=range(
            1, n_movies_to_reccomend+1))
        return df

    else:
        return "No movies found. Please check your input"
# dataLast, movie, data_pivot = data_prep()
# movie_recommendation('Gladiator', dataLast, movie)
