# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 08:51:43 2016

@author: Cara G
"""

import pandas as pd
import numpy as np

yarn = pd.read_csv('yarn_stats_manually_imputed.csv', index_col=0)
yarn.columns
# in yarn_texture -- replace empty cells with 0, 'TRUE' with 1, and 'FALSE' with -1
yarn_texture = pd.read_csv('yarn_texture_refined.csv', index_col=0)
yarn_texture.replace([False, True], [-1, 1], True)
yarn_texture.replace(['FALSE', 'TRUE'], [-1, 1], True)
yarn_texture.replace([None], [0], True)

# clusters - get 8 normalized cluster features
# tally comment count per cluster per yarn  (adding 8 columns, one for each cluster)	
# divide each count by total comments per yarn	add to rest of data
clusters = pd.read_csv('clusters_per_comment_final.csv', index_col=0)
clusters.drop(['comment', 'km_8clusters'], axis=1, inplace=True)
clusters.columns = ['yarn_id', 'cluster']
#get clusters as separate cols for each cluster
clusters = pd.get_dummies(clusters, prefix='Cluster', columns=['cluster'])
#get cluster count per yarn
clusters_per_yarn = clusters.groupby(['yarn_id'], as_index=True).sum()
#divide each cluster count per yarn by total clusters per yarn
normal_clusters = clusters_per_yarn.div(clusters_per_yarn.sum(axis=1), axis='index')
#rename clusters
normal_clusters.columns = ['cl_1', 'cl_2', 'cl_3', 'cl_4', 'cl_5', 'cl_6', 'cl_7', 'cl_8']
#REPLACE MISSING CLUSTER ASSIGNMENTS WITH 0
normal_clusters.replace([None], [0], True)



# drop some columns ... 
#* indicates a col we don't want for modeling but may want back for user querying
cols_to_drop = ['company_name', #*
                'weight_name', #*
                'yarn_name', #*
                'permalink', #***
                'fiber_type_name_list', 'fiber_id_list', 'company_permalink',
                 'rating_tot', 'texture', 'discontinued']
yarn.drop(cols_to_drop, axis=1, inplace=True)

#machine_washable	& organic: turn to 3 factors (yes, no, NA … 1, -1, 0 ???)		
yarn['organic'].replace([False, True, None], [-1, 1, 0], True)
yarn['machine_washable'].replace([False, True, None], [-1, 1, 0], True)

# expand cells that are lists into their own columns (keep only first 3 vals in each list)

#ANIMAL BOOLEAN
#split list to cols
animal_fiber_bool = yarn['animal_fiber_list'].apply(lambda x: pd.Series(x.split(',')))
#replace missing with 0
animal_fiber_bool.replace([np.nan], [0], True)
#reverse
animal_fiber_bool[animal_fiber_bool.columns[::-1]]
#rename
animal_fiber_bool = animal_fiber_bool.rename(columns = lambda x : 'animal_fiber_bool_' + str(x))
#add first 3 columns back to main df
yarn = pd.concat([yarn[:], animal_fiber_bool.iloc[:,0:3]], axis=1)

#VEGETABLE BOOLEAN
#split list to cols
vegetable_fiber_bool = yarn['vegetable_list'].apply(lambda x: pd.Series(x.split(',')))
#replace missing with 0
vegetable_fiber_bool.replace([np.nan], [0], True)
#reverse
vegetable_fiber_bool[vegetable_fiber_bool.columns[::-1]]
#rename
vegetable_fiber_bool = vegetable_fiber_bool.rename(columns = lambda x : 'vegetable_fiber_bool_' + str(x))
#add to main df
yarn = pd.concat([yarn[:], vegetable_fiber_bool.iloc[:,0:3]], axis=1)

#SYNTHETIC BOOLEAN
#split list to cols
synthetic_fiber_bool = yarn['synthetic_list'].apply(lambda x: pd.Series(x.split(',')))
#replace missing with 0
synthetic_fiber_bool.replace([np.nan], [0], True)
#reverse
synthetic_fiber_bool[synthetic_fiber_bool.columns[::-1]]
#rename
synthetic_fiber_bool = synthetic_fiber_bool.rename(columns = lambda x : 'synthetic_fiber_bool_' + str(x))
#add to main df
yarn = pd.concat([yarn[:], synthetic_fiber_bool.iloc[:,0:3]], axis=1)

#FIBER TYPE ID
#strip
fiber_type_id = yarn['fiber_type_id_list'].apply(lambda x: pd.Series(x.strip('[]')))
#split
fiber_type_id = fiber_type_id[0].apply(lambda x: pd.Series(x.split(',')))
#replace missing
fiber_type_id.replace([np.nan], [0], True)
#reverse
fiber_type_id[fiber_type_id.columns[::-1]]
#rename 
fiber_type_id = fiber_type_id.rename(columns = lambda x : 'fiber_type_id_' + str(x))
#add to main df
yarn = pd.concat([yarn[:], fiber_type_id.iloc[:,0:3]], axis=1)

#FIBER PCT
#FIBER TYPE ID
#strip
fiber_pct = yarn['fiber_pct_list'].apply(lambda x: pd.Series(x.strip('[]')))
#split
fiber_pct = fiber_pct[0].apply(lambda x: pd.Series(x.split(',')))
#replace missing
fiber_pct.replace([np.nan], [0], True)
#reverse
fiber_pct[fiber_pct.columns[::-1]]
#rename 
fiber_pct = fiber_pct.rename(columns = lambda x : 'fiber_pct_' + str(x))
#add to main df
yarn = pd.concat([yarn[:], fiber_pct.iloc[:,0:3]], axis=1)


#DROP LISTS THAT ARE NOW DERIVED INTO SEPARATE COLUMNS
yarn.drop(['animal_fiber_list', 'synthetic_list', 'vegetable_list',
           'fiber_type_id_list', 'fiber_pct_list', 'TEXTURE MISSING FROM RAV'], axis=1, inplace=True) 
yarn.columns

#CONCATENATE YARN TEXTURE BOOLS (MAY DROP SOME LATER)
yarn = pd.concat([yarn[:], yarn_texture[:]], axis=1)

#CONCATENATE CLUSTERS
yarn = pd.concat([yarn[:], normal_clusters[:]], axis=1)

yarn.replace([np.nan], [0], True)

#ADD CUSTOM LABELS SO FAR
labs = pd.read_csv('old_labels.csv', index_col=0)
labs.replace([np.nan], [0], True)
yarn = pd.concat([yarn[:], labs[:]], axis=1)


#DROP ROWS MISSNIG MOST VALS (FOUND MANUALLY)
yarn.drop([8418, 23316, 75725], axis=0, inplace=True)

# DROP THESE BECAUSE THEY ARE WEIRD YARNS (RIBBON, FUR, ETC)
drop_these_rows = yarn[yarn["unspun/roving"]==1].index
drop_these_rows = drop_these_rows.append(yarn[yarn["weight_id"]==0].index)
drop_these_rows = drop_these_rows.append(yarn[yarn["eyelash/fur/novelty"]==1].index)
drop_these_rows = drop_these_rows.append(yarn[yarn["ribbon"]==1].index)
drop_these_rows = drop_these_rows.append(yarn[yarn["boucle"]==1].index)
yarn.drop(drop_these_rows, axis=0, inplace=True)

#THEN DROP THESE COLUMNS:
yarn.drop(['unspun/roving', 'eyelash/fur/novelty', 'ribbon', 'boucle'], axis=1, inplace=True) 


#NORMALIZING STUFF ... 

#ROBUST SCALING (ALSO TRY MIN MAX??)
from sklearn import preprocessing
robust_scaler = preprocessing.RobustScaler(with_centering=False)
min_max_scaler = preprocessing.MinMaxScaler()
yarn["num_stashes"] = robust_scaler.fit_transform(yarn["num_stashes"])
yarn["num_comments"] = robust_scaler.fit_transform(yarn["num_comments"])
yarn["num_projects"] = robust_scaler.fit_transform(yarn["num_projects"])
yarn["rating_ct"] = robust_scaler.fit_transform(yarn["rating_ct"])
yarn["rating_avg"] = min_max_scaler.fit_transform(yarn["rating_avg"])

#REDUCE COMPANY IDs BEFORE GETTING THEIR DUMMIES
company_count = pd.DataFrame(yarn["company_id"].value_counts())
yarn["company_id"] = [comp_id if company_count["company_id"][comp_id] > 10 else 0 for comp_id in yarn["company_id"]]

#GET COMPANY_ID DUMMIES
yarn = pd.get_dummies(yarn, prefix='company_id', columns=['company_id'])

#DROP COMPANY_ID = 0
yarn.drop(['company_id_0'], axis=1, inplace=True) 

#GET DUMMIES FOR THE REST OF THE CATEGORICAL VARS
yarn_4 = pd.get_dummies(yarn_df, prefix=['weight_id', 'animal_fiber_bool_1',
                                         'animal_fiber_bool_2', 'animal_fiber_bool_3',
                                         'vegetable_fiber_bool_1', 'vegetable_fiber_bool_2',
                                         'vegetable_fiber_bool_3', 'synthetic_fiber_bool_1',
                                         'synthetic_fiber_bool_2', 'synthetic_fiber_bool_3',
                                         'fiber_type_id_1', 'fiber_type_id_2', 'fiber_type_id_3'],
                                         columns=['weight_id', 'animal_fiber_bool_0',
                                         'animal_fiber_bool_1', 'animal_fiber_bool_2',
                                         'vegetable_fiber_bool_0', 'vegetable_fiber_bool_1',
                                         'vegetable_fiber_bool_2', 'synthetic_fiber_bool_0',
                                         'synthetic_fiber_bool_1', 'synthetic_fiber_bool_2',
                                         'fiber_type_id_0', 'fiber_type_id_1', 'fiber_type_id_2'])



fiber_combos = pd.read_csv('fiber combos fixed.csv', index_col=0)
fiber_combos_updated = pd.read_csv('fiber combos fixed.csv', index_col=0)
val_cts = pd.DataFrame(fiber_combos["fiber_combo"].value_counts())

fiber_combos_updated["fiber_combo"] = [combo if val_cts["fiber_combo"][combo] > 8 else 0 for combo in fiber_combos["fiber_combo"]]



fiber_combos_2 = pd.get_dummies(fiber_combos_updated, prefix=['blend'],
                                         columns=['fiber_combo'])

fiber_combos_2.drop(['blend_0'], axis=1, inplace=True)

fiber_combos_2.to_csv('new_fiber_pcts_dummies.csv', index_col=0)

newest = pd.concat([fiber_combos_2[:], yarn[:]], axis=1)

yarn_new.to_csv('check_this.csv', index_col=0)

yarn_new = pd.read_csv('check_this.csv', index_col=0)

#drop organic
yarn_new.drop(['organic'], axis=1, inplace=True) 

#scale stuff
yarn_new["plies"] = min_max_scaler.fit_transform(yarn_df["plies"])
yarn_new["num_fibers"] = min_max_scaler.fit_transform(yarn_df["num_fibers"])

yarn_new.drop(['single-ply', '2-ply', '3-ply', '4-ply', 'more-ply'], axis=1, inplace=True) 

yarn_new.drop(['vegetable_fiber_bool_2_1','vegetable_fiber_bool_3_1',
              'synthetic_fiber_bool_2_1','synthetic_fiber_bool_3_1'], axis=1, inplace=True) 

#bin weights 7-9
yarn_new["weight_id_7_8_9"] = yarn_new[["weight_id_7", "weight_id_8","weight_id_9"]].sum(axis=1)
yarn_new.drop(['weight_id_7','weight_id_8', 'weight_id_9'], axis=1, inplace=True) 

#drop all columns with less than 15 values
yarn_trimmed = yarn_new[yarn_new.columns[yarn_new.sum(axis=0) > 14]]
yarn_trimmed["is_pilly"] = pill_labs["is_pilly"]
yarn_trimmed.drop(['is_pilly'], axis=1, inplace=True)

yarn_trimmed.to_csv('all_rows_all_cols_reduced.csv', index_col=0)

pill_labs_yarn_trimmed = pd.concat([yarn_trimmed, pill_labs], axis=1, join='inner')

pilly_rows = pill_labs_yarn_trimmed[pill_labs_yarn_trimmed["is_pilly"]==1]
not_pilly_rows = pill_labs_yarn_trimmed[pill_labs_yarn_trimmed["is_pilly"]==0]

pilly_rows.drop(['is_pilly'], axis=1, inplace=True) 
not_pilly_rows.drop(['is_pilly'], axis=1, inplace=True) 


pilly_rows.to_csv('pilly_rows.csv', index_col=0)
not_pilly_rows.to_csv('not_pilly_rows.csv', index_col=0)

yarn_trimmed.columns


#change normalization from robust to min-max regular
from sklearn.preprocessing import normalize
yarn_old = pd.read_csv('yarn_orig.csv', index_col=0)
yarn_trimmed = pd.read_csv('all_rows_all_cols_reduced.csv', index_col=0)

yarn_trimmed.drop(['num_stashes', 'rating_avg', 'plies', 'num_fibers',
                   'num_comments', 'num_projects', 'rating_ct'],
                   axis=1, inplace=True)

this_too = pd.read_csv('plies.csv', index_col=0)

yarn_old_2 = pd.concat([yarn_trimmed, yarn_old, this_too], axis=1, join='inner')


yarn_old_3 = yarn_old_2[yarn_old_2.columns[144:]]
yarnMat = np.mat(yarn_old_3.values)
yarn_old_3.columns

yarn_re_norm = pd.DataFrame(index=yarn_old_3.index)
yarn_re_norm['num_fibers'] = normalize(yarn_old_3['num_fibers'], norm='l2').reshape(-1,1)
yarn_re_norm['num_stashes'] = normalize(yarn_old_3['num_stashes'], norm='l2').reshape(-1,1)
yarn_re_norm['num_comments'] = normalize(yarn_old_3['num_comments'], norm='l2').reshape(-1,1)
yarn_re_norm['num_projects'] = normalize(yarn_old_3['num_projects'], norm='l2').reshape(-1,1)
yarn_re_norm['rating_ct'] = normalize(yarn_old_3['rating_ct'], norm='l2').reshape(-1,1)
yarn_re_norm['rating_avg'] = normalize(yarn_old_3['rating_avg'], norm='l2').reshape(-1,1)
#yarn_re_norm['plies'] = normalize(yarn_old_3['plies'], norm='l2').reshape(-1,1)

yarn_trimmed_reg_norm = pd.concat([yarn_trimmed, yarn_re_norm, this_too], axis=1, join='inner')

yarn_norm = pd.read_csv('all_reduced_reg_norm.csv', index_col=0)
split_labs = pd.read_csv('split_labels.csv', index_col=0)
split_labs_yarn_trimmed = pd.concat([yarn_norm, split_labs], axis=1, join='inner')


splitty_rows = split_labs_yarn_trimmed[split_labs_yarn_trimmed["is_splitty"]==1]
not_splitty_rows = split_labs_yarn_trimmed[split_labs_yarn_trimmed["is_splitty"]==0]

splitty_rows.drop(['is_splitty'], axis=1, inplace=True) 
not_splitty_rows.drop(['is_splitty'], axis=1, inplace=True) 

splitty_rows.to_csv('splitty_rows.csv', index_col=0)
not_splitty_rows.to_csv('not_splitty_rows.csv', index_col=0)

split_labs_yarn_trimmed.drop(['is_splitty'], axis=1, inplace=True) 
split_labs_yarn_trimmed.to_csv('data_only_for_split_labels.csv', index_col=0)



"""
DONE: 
manually imputed all fiber info for yarn_id 75725; drop yarn_ids 105627, 23316, 8418 (should have been dropped in first preprocessing bc many null vals)		
texture	    finish processing with openrefine; create multiple columns where there are currently 2 values (eg, "soft, smooth") and factorize all into separate variables (eg a 0/1 variable for each possible texture feature)	merge results from 'yarn texture refined.csv'	
yarn_notes	drop	
fiber_type_name_list	drop		
fiber_id_list	drop		
company_permalink	drop		
company_name	drop		
weight_name	drop		
weight_knit_gauge	drop		
weight_ply	drop		
weight_wpi	drop		
discontinued	drop (no discontinued yarns in dataset)		
grams	drop		
yarn_name	drop		
permalink	drop		
rating_tot	drop
wpi	drop		
yardage	drop		
gauge_divisor	drop		
max_gauge	drop		
min_gauge	drop		
last_updated	drop		
common_price	drop (mostly missing)
8 normalized cluster features	   tally comment count per cluster per yarn  (adding 8 columns, one for each cluster)	divide each count by total comments per yarn	add to rest of data
machine_washable	turn to 3 factors (yes, no, NA … 1, -1, 0 ???)		
organic	    mpute missing OR turn to 3 factors (yes, no, NA … 1, -1, 0 ???)		
animal_fiber_list	reverse list	expand to 3 cols (drop last 2 vals)	possibly drop … should be 100% correlated with fiber_type_id but fiber_type_id is more specific
fiber_type_id_list	reverse list	expand to 3 cols (drop last 2 vals)	
synthetic_list	reverse list	expand to 3 cols (drop last 2 vals)	possibly drop … should be 100% correlated with fiber_type_id but fiber_type_id is more specific
vegetable_list	reverse list	expand to 3 cols (drop last 2 vals)	possibly drop … should be 100% correlated with fiber_type_id but fiber_type_id is more specific
fiber_pct_list	reverse list	expand to 3 cols (drop last 2 vals)	figure out what to do with 'none' values (possible manual imputation)
num_projects	normalize … robust?		
rating_avg	normalize (across all yarns)		
rating_ct	robust normalize (across all yarns)		
num_stashes	normalize … robust?		
company_id	 -- GET DUMMIES FOR COMPANIES THAT OCCUR MORE THAN 10 TIMES
weight_id	-- GET DUMMIES 
fiber bools and fiber id -- GET DUMMIES
cluster cols -- impute 0 where missing val
"""