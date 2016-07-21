import requests, json, mechanize, cookielib, re
from bs4 import BeautifulSoup
from itertools import izip
from urllib2 import HTTPError
import pandas as pd
import numpy as np
from yarn_scrap import * #all our custom functions

#1) set up API and web auth
auth = 'your_Ravelry_API_email_address', 'your_Ravelry_API_appname'  #auth for API (api stats)
br = ravelryLogin('your_regular_Ravelry_username', 'your_regular_Ravelry_password') #auth for web scraping (web stats and yarn comments)

#2) get urls for search query that returns all yarns, ordered by most frequently used in knitting projects 
# also url of all yarns that are 100% acrylic, so that they can be excluded.
yarn_search_url = 'https://foauth.org/api.ravelry.com/yarns/search.json?sort=projects&discontinued=no&ratings=-0%2B-1%2B-2'
yarn_search_url_del = 'https://foauth.org/api.ravelry.com/yarns/search.json?fiber=acrylic&fiberc=1&sort=projects'

#3) get dict of all yarn_id:yarn_permalink pairs for these yarns -- since we web-scrape comments by permalink but call API by id
all_yarn = get_yarn_dict(yarn_search_url, yarn_search_url_del, auth)

##OPTIONAL: write yarn dict to file
#json.dump(all_yarn, open("yarn_permalinks_ids.txt",'w'))

#4) build df of yarn stats 
##OPTIONAL: read yarn dict from file
#all_yarn = json.load(open("yarn_permalinks_ids.txt"))	

#4a) scrape stats from API
api_columns = getApiColumns()
		   
yarn_api_stats_df = pd.DataFrame(index=all_yarn.keys(), columns=api_columns)

for yarn_id in all_yarn.keys():
    yarn_api_stats_df.loc[yarn_id] = parseYarn(yarn_id, auth)

with open('yarn_api_stats_df.csv', 'w') as f:	#save this to file since it takes a while to call
	yarn_api_stats_df.to_csv(f, sep=',', encoding='utf-8', index_label='yarn_id')	

#del yarn_api_stats_df   # OPTIONAL: REMOVE FROM MEMORY (READ BACK IN FROM CSV WHEN WE NEED IT AGAIN)

#4b) scrape stats from web
web_columns = getWebColumns()

yarn_web_stats_df = pd.DataFrame(index=all_yarn.keys(), columns=web_columns)
 
for yarn_id, yarn_permalink in all_yarn.iteritems():
	yarn_web_stats_df.loc[yarn_id] = getYarnSumStats(yarn_permalink, br)

with open('yarn_web_stats_df.csv', 'w') as f:	#save this to file since it takes a while to call
	yarn_web_stats_df.to_csv(f, sep=',', encoding='utf-8', index_label='yarn_id')		

#del yarn_web_stats_df   # OPTIONAL: REMOVE FROM MEMORY (READ BACK IN FROM CSV WHEN WE NEED IT AGAIN)

#4c) concatenate web and api stats together; drop yarns with zero comments; drop yarns missing permalinks
yarn_api_stats = pd.read_csv('yarn_api_stats_df.csv', index_col=0)	#read api stats back in from file
yarn_web_stats = pd.read_csv('yarn_web_stats_df.csv', index_col=0)	#read web stats back in from file

yarn_stats = pd.concat([yarn_api_stats, yarn_web_stats], axis=1)	#concatenate api + web stats

##OPTIONAL: DELETE yarn_api_stats AND yarn_web_stats FROM ENVIRONMENT TO FREE UP MEMORY
# del yarn_api_stats
# del yarn_web_stats
yarn_stats = yarn_stats[yarn_stats.num_comments != 0]	#drop rows where num_comments = 0
yarn_stats = yarn_stats[yarn_stats.permalink.notnull()]	#drop rows where permalink is a missing value from api (indicates lack of most info)

##OPTIONAL: SAVE TO FILE
with open('yarn_stats_df.csv', 'w') as f:
	yarn_stats.to_csv(f, sep=',', encoding='utf-8', index_label='yarn_id')		

#5) get comments for every yarn left in yarn_stats
# format of each row is: [yarn_index, comment_1, comment_2, ..., comment_n]
# file is in unicode and must be decoded when read back into Python for further processing
with open('comments.csv','ab') as f: #NEEDS TO BE DECODED FOR UTF-8 WHEN READ BACK IN
    writer=csv.writer(f) 
    for yarn_index, permalink, num_comments in izip(yarn_stats.index, yarn_stats["permalink"], yarn_stats["num_comments"]):
        if num_comments < 100:
            writeFewYarnComments(yarn_index, permalink, br)
        else:
            writeManyYarnComments(yarn_index, permalink, num_comments, br)

#to get comments and yarn IDs in long format
from csv import reader
new_comments_index = []
new_comments = []
with open('comments.csv', 'rb') as f_in:   #read back in the file we just created
    reader = reader(f_in)
    reader.next()     #skip header row in csv
    for row in reader:
        this_index = row.pop(0)     #get yarn index
        row_mod = [s.decode('utf-8') for s in row if s != '']   
        this_index = [this_index for s in row_mod]
        new_comments.extend(row_mod)
        new_comments_index.extend(this_index)
        #print new_comments

comms_with_index = pd.DataFrame({'comment' : new_comments}, index=new_comments_index)
comms_with_index.to_csv('comments_with_yarn_ids.csv', encoding='utf-8', index_label='yarn_id')              

#to get comments and yarn IDs with each set of comments collapsed (to one document per yarn)
from csv import reader
new_comments_index = []
new_comments_collapsed = []
with open('comments.csv', 'rb') as f_in:   #read back in the file we just created
    reader = reader(f_in)
    reader.next()     #skip header row in csv
    for row in reader:
        this_index = row.pop(0)     #get yarn index
        row_mod = ' '.join([s.decode('utf-8') for s in row if s != ''])
        this_yarn_comments.extend(row_mod)
        new_comments_index.extend(this_index)
        #print new_comments

collapsed_comms_with_index = pd.DataFrame({'comment' : new_comments}, index=new_comments_index)
collapsed_comms_with_index.to_csv('collapsed_comments_with_yarn_ids.csv', encoding='utf-8', index_label='yarn_id')               


