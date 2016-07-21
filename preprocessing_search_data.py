# -*- coding: utf-8 -*-
"""
Created on Sun Jun 05 17:11:08 2016

@author: Cara G
"""
#Prepare data for search
import pandas as pd

yarn = pd.read_csv('yarn_stats_df.csv', index_col=0, encoding='utf-8')
pill_rank = pd.read_csv('pilly_distances.csv', index_col=0)
split_rank = pd.read_csv('splitty_distances.csv', index_col=0)

from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()

split_scaled = min_max_scaler.fit_transform(split_rank)
split_rank = pd.DataFrame.from_records(split_scaled, index=split_rank.index, columns=['split_rank'])

pill_scaled = min_max_scaler.fit_transform(pill_rank)
pill_rank = pd.DataFrame.from_records(pill_scaled, index=pill_rank.index, columns=['pill_rank'])

#drop rows that were dropped when we built our models
yarn = pd.concat([yarn, pill_rank], axis=1, join="inner")
yarn.drop(['cosine_dist'], axis=1, inplace=True) 

#drop columns we don't need for user search
columns_to_keep = ["num_fibers", "fiber_type_name_list", "company_name", 
                   "weight_name", "machine_washable", "yarn_name", "permalink", "rating_avg"]

yarn = yarn[columns_to_keep]
yarn.columns

#check value counts for each column and deal with missing values and inconsistencies
yarn["num_fibers"].value_counts()
yarn["num_fibers"].replace([1], [0], True)
yarn["num_fibers"].replace([2,3,4,5], [1,1,1,1], True)

yarn["company_name"].value_counts()

yarn["weight_name"].value_counts()
yarn["weight_name"].replace(['DK / Sport'], ['DK'], True)

yarn["machine_washable"].value_counts()
yarn["machine_washable"].replace([True, False], [0, 1], True)

yarn["yarn_name"].value_counts()

yarn["rating_avg"].describe()

yarn["fiber_type_name_list"].value_counts()
yarn["fiber_type_name_list"].replace(['[]'], ['Wool'], True) #one missing val

pill_rank = pill_rank.rename(columns={'cosine_dist':'pill_rank'})
split_rank = split_rank.rename(columns={'cosine_dist':'split_rank'})
yarn = yarn.rename(columns={'fiber_type_name_list':'fiber_type'})

yarn = pd.concat([yarn, pill_rank, split_rank], axis=1, join="inner")

yarn.to_csv('yarn_search.csv', index_col=0, encoding='utf-8')