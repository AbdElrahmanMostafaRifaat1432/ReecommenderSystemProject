#!/usr/bin/env python
# coding: utf-8

# In[4]:


import warnings as w
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import gc

import torch
from deepctr_torch.inputs import SparseFeat, VarLenSparseFeat, get_feature_names
from deepctr_torch.models import DeepFM
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from IPython.display import display
plt.style.use('ggplot')

w.filterwarnings(action='ignore')
pd.set_option('display.max_columns', None)

key2index = {}
key3index = {}


def split(x, gen):
    global key2index, key3index

    key_ans = x.split('|')
    for key in key_ans:
        if ((key not in key2index) and gen == 1) or ((key not in key3index) and gen == 0):
            # Notice : input value 0 is a special "padding",so we do not use 0 to encode valid feature for sequence input
            if gen:
                key2index[key] = len(key2index) + 1
            else:
                key3index[key] = len(key3index) + 1
    if gen:
        return list(set(map(lambda x: key2index[x], key_ans)))
    else:
        return list(set(map(lambda x: key3index[x], key_ans)))


def user_recomm(user_id, k=10):
    global key2index, key3index
    data1 = pd.read_csv('data.csv')
    data = data1.copy()
    # all without genere , title , time stamp , rating
    sparse_features = ["movieId", "userId", ]
    target = ['rating']

    # 1.Label Encoding for sparse features,and process sequence features
    for feat in sparse_features:
        lbe = LabelEncoder()
        data[feat] = lbe.fit_transform(data[feat])
    # preprocess the sequence feature

    genres_list = list(
        map(split, data['genres'].values, np.ones(len(data['genres'].values))))
    concatenated_tags_list = list(map(split, data['concatenated_tags'].values, np.zeros(
        len(data['concatenated_tags'].values))))

    # print(genres_list) [[1,2],[3,4]]
    genres_length = np.array(list(map(len, genres_list)))
    concatenated_tags_length = np.array(list(map(len, concatenated_tags_list)))

    # print(concatenated_tags_length) #[2 ,3,4]
    max_len_gen = max(genres_length)
    max_len_tag = max(concatenated_tags_length)
    # Notice : padding=`post`
    genres_list = pad_sequences(
        genres_list, maxlen=max_len_gen, padding='post', )
    concatenated_tags_list = pad_sequences(
        concatenated_tags_list, maxlen=max_len_tag, padding='post', )

    # print(genres_list) [[1,2,0,0,0],[]]
    # 2.count #unique features for each sparse field and generate feature config for sequence feature

    """
    fixlen_feature_columns = [
    SparseFeat('user_id', 1000, embedding_dim=4),
    SparseFeat('movie_id', 5000, embedding_dim=4),
    """

    fixlen_feature_columns = [SparseFeat(feat, data[feat].nunique(), embedding_dim=16)
                              for feat in sparse_features]

    # get the mean of embeddings of the sequence
    varlen_feature_columns = [VarLenSparseFeat(SparseFeat('genres', vocabulary_size=len(key2index) + 1, embedding_dim=16), maxlen=max_len_gen, combiner='mean'),
                              VarLenSparseFeat(SparseFeat('concatenated_tags', vocabulary_size=len(
                                  key3index) + 1, embedding_dim=16), maxlen=max_len_tag, combiner='mean')
                              ]  # Notice : value 0 is for padding for sequence input feature

    linear_feature_columns = fixlen_feature_columns + varlen_feature_columns
    dnn_feature_columns = fixlen_feature_columns + varlen_feature_columns

    # instantiate the model
    model = DeepFM(linear_feature_columns, dnn_feature_columns,)
    model.load_state_dict(torch.load('DeepFM'))

    item_ids = data['movieId'].unique()  # Example: IDs from 1 to num_items
    user_features = {
        'userId': [user_id] * len(item_ids),  # User ID
    }
    user_df = pd.DataFrame(user_features)
    item_df = pd.DataFrame({'movieId': item_ids})

    genres_list = np.array([genres_list[data[data['movieId'] == item].index[0]]
                           for item in item_df['movieId'].values])

    conc_list = np.array([concatenated_tags_list[data[data['movieId'] == item].index[0]]
                         for item in item_df['movieId'].values])

    all_data = pd.concat([user_df, item_df], axis=1)

    # Create input data dictionary for the model
    model_input = {
        name: all_data[name].values for name in ['userId',	'movieId']}
    # genres_features#all_data['genres'].values
    model_input['genres'] = genres_list
    # tag_features #all_data['concatenated_tags'].values
    model_input['concatenated_tags'] = conc_list

    # Predict ratings or probabilities using the trained model
    predictions = model.predict(model_input, batch_size=256)

    # 3. Sort the predicted ratings or probabilities in descending order
    # Get the indices that would sort the predictions in descending order
    sorted_indices = np.argsort(predictions.flatten())[::-1]

    # 4. Exclude items that the user has interacted with
    # Replace interacted_item_ids with the IDs of items the user has interacted with
    interacted_item_ids = set(data[data['userId'] == user_id]['movieId'])

    # Filter out the interacted items from the sorted indices
    filtered_indices = [
        index for index in sorted_indices if item_ids[index] not in interacted_item_ids]

    # 5. Select the top k recommendations
    # Get the indices of the top k recommendations
    top_k_indices = filtered_indices[:k]
    # Get the IDs of the top k recommended items
    top_k_items = item_ids[top_k_indices]

    # Print or return the top k recommendations
    print("Top {} Recommendations: {}".format(k, top_k_items))
    i = 1
    for top in top_k_items:
        print("Top {} Recommendations: {}".format(
            i, data[data['movieId'] == top]['title'].iloc[0]))
        i += 1

    return top_k_items


# if __name__ == "__main__":

#     key2index = {}
#     key3index = {}

#     user_id = 123
#     k = 20
#     user_recomm(user_id, k)


# In[ ]:
