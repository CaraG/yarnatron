# ADD TO STOP WORDS: 'hi', 'hello', 'oh', 'color'


def text_to_snow_stem(comment):
    meaningful_words = [w for w in re.sub("[^a-zA-Z0-9]", " ", comment).lower().split() if not w in stops]
    return [Snst.stem(w) if w != 'worsted' else 'worsted' for w in meaningful_words]  #FIXED THIS SO IT CATCHES WORSTED CORRECTLY

def process_comments(yarntxts):  #where yarntxts is a df with 2 columns, "comments" and "yarnId"
	from collections import Counter
	from nltk.stem import SnowballStemmer
	import re
    Snst = SnowballStemmer("english")    #create obj of Snowball Stemmer
	clean_comment_lists = [text_to_snow_stem(comment) for comment in yarntxts["comment"]] 	#get each comment as a clean list
    overall_word_freq = dict(Counter([word for comment in clean_comment_lists for word in comment]))   #get word frequency dict
    clean_comment_strings = [" ".join(comment) for comment in clean_comment_lists]  	#get each comment as a clean string
    yarntxts["word_count"] = [len(text) for text in clean_comment_lists]  #add column of word count per cleaned comment to yarntxts 
    
    return overall_word_freq, clean_comment_strings, yarntxts

#EXAMPLE -- returns a word frequency dict, comment as cleaned strings, and input df of comments/ids with added word count column
word_freq_dict, clean_texts, yarntxts_with_word_counts = process_comments(yarnspud)

# EXAMPLE OF REMOVING ALL COMMENTS THAT ARE EMPTY AFTER CLEANING
reduced_yarn_txts = yarntxts_with_word_counts[yarntxts_with_word_counts["word_count"]==0]

### OPTIONAL -- PRINT SUMMARY OF OVERALL TOP N TERMS AND FREQUENCIES
def summarize_top_terms(word_freq_dict, N_terms):
    sorted_word_freq = sorted(word_freq_dict.items(), key=operator.itemgetter(1), reverse=True)
    print '{}\t\t{}'.format('Term', 'Overall Frequency')
    for top_overall_term in range(len(sorted_word_freq_dict[:N_terms])):
        print '{}\t\t{}'.format(sorted_word_freq[top_overall_term][0], sorted_word_freq[top_overall_term][1])

	
#EXAMPLE -- PRINT OUT 20 TOP TERMS FROM word_freq_dict AND THEIR FREQUENCIES
#summarize_top_terms(word_freq_dict, 20)