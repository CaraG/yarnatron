## version 0.8
A search tool for knitters and other fiber artists that ranks results by a predicted score regarding unwanted attributes of yarn (e.g., pilling and splitting). Uses data from Ravelry.com

## Contents
1. yarn_scrape.py: various functions for scraping all required data from the Ravelry API and from ravelry.com
2. yarn_scrape_implementation_redacted.py: script to run functions from yarn_scrape.py and save all retrieved data to CSV (private auth and login info removed)
3. yarn_stats_df.csv: output of non-comment data from yarn_scrape_implementation.py 
4. comments.csv:  output of scraped comments, indexed by yarn_id (one row per yarn, each column is a comment)		
5. comments_with_yarn_ids.csv: output of scraped comments, indexed by yarn_id (one row per comment, multiple rows per yarn_id)		33,753 rows of comments
6. yarn_stats_manually_imputed.csv: yarn_stats_df.csv after using OpenRefine to munge some missing values and do some fuzzy matching of messy database entries.  Manual labels were created with the help of OpenRefine and Excel by viewing yarn statistics and their comments side by side and using domain expertise as to the generally previously known characteristics of yarn content and construction (e.g., tightly twisted many-ply wool-nylon blend yarn does not generally pill, whereas single-ply, worsted weight, super soft, loosely spun, 100% merino is known to pill badly).
7. yarn_preprocessing.py: script for all preprocessing of yarn data before classification modeling, including normalization of numeric variables and factorizing (getting dummy variables) of categorical variables, as well as reducing data by removing columns with very low frequency of values and dropping a small subset of rows missing most of their data (due to erroneous database entries not previously discovered in munging process). Cluster assignments from text mining and kmeans clustering were merged with the rest of the data in this step
8. pilly_rows.csv, not_pilly_rows.csv, split_rows.csv, not_splitty_rows.csv: output data from yarn_preprocessing.py
9. preprocessing_search_data.py: preparing data for app (search space, ranking info and data needed to print output)
10.	yarn_search.csv: output data from preprocessing_search_data.py, used by and packaged with app 
11.	TO BE UPLOADED: text processing Jupyter notebook; includes exporation of unigrams and bigrams, stemming, removal of stop words, POS labeling, TF-IDF vectorization, kmeans clustering of TF-IDF results, cluster silhouette analysis, Davies Bouldin index analysis
12.	process_comments.py: first version of code to process text (TO BE IMPROVED)
13. TO BE UPLOADED: classification Jupyter notebook; adds cluster assignment from text processing as an attribute; includes exploration of SVM, Rocchio prototype vectors, logistic regression, LDA, random forests, etc
14. Sample Data and Description.xlsx: The first tab of the spreadsheet contains a sample of the data used by the Yarnatron app, The second tab contains a Data Dictionary of the same data.
15. yarnatron.py: the app!
16. setup.py: additional script for compiling the app
17. Sample Runs.docx: Detailed description of app with screenshots


## Planned improvements
- increase size of training set by manually labelling 100-200% more yarns
- re-run all exploration of classification methods with the larger training set
- build SQL database and adapt the app to use this database instead of using local CSVs
- ditch easygui for a much more user friendly web-based interface
- add more unwanted attributes, i.e., scratchy, smelly, knotty

