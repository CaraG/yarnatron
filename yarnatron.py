# -*- coding: utf-8 -*-
"""
Created on Sun Jun 05 23:13:18 2016

@author: Cara G
"""
import pandas as pd
from easygui import *
from tabulate import tabulate
import sys

#read in file that will be the search space and also contains data needed for output/display
search_df = pd.read_csv('yarn_files/yarn_search.csv', index_col=0, encoding='utf-8')

#initialize list of all possible fiber names (will be used as search options)
fiber_names = ['Acrylic', 'Alpaca', 'Angora', 'Bamboo', 'Bison', 'Camel', 
               'Cashmere', 'Cotton', 'Hemp', 'Linen', 'Llama', 'Merino',
               'Metallic', 'Microfiber', 'Mohair', 'Nylon', 'Other', 
               'Plant fiber', 'Polyester', 'Qiviut', 'Rayon', 'Silk', 'Soy',
               'Tencel', 'Wool', 'Yak']

#initialize list of all possible fiber names (will be used as search options)
yarn_weights = ['Aran', 'Bulky', 'Cobweb', 'DK', 'Fingering', 'Lace',
                'Light Fingering', 'Sport', 'Super Bulky', 'Thread', 'Worsted']

#assign program title
title = 'Yarnatron' 

def get_search_params(title):
	'''use easygui interface boxes to get input form user
	all entries are optional; clicking cancel or selects all moves user to next box'''
    # 0 for single fiber, 1 for blend, 2 if no preference 
    num_fibers_input = indexbox(msg='Single Fiber or Blend?', title=title, 
                                choices=('Single Fiber', 'Blend', 'No preference'))
    
    fiber_type_input = multchoicebox(msg='Choose one or more fibers, then click OK',
                                     title=title, choices=(fiber_names))

    # 0 for machine washable, 1 for not machine washable, 2 if no preference 
    machine_wash_input = indexbox(msg='Machine Washable?', title=title,
                                  choices=('Yes', 'No', 'No preference'))
    
    company_name_input = enterbox(msg='Enter a brand name of yarn, then click OK',
                                  title=title, default='', strip=False)            
    
    yarn_weights_input = multchoicebox(msg='Choose one or yarn weights, then click OK\n(or click Cancel to search all)',
                                     title=title, choices=(yarn_weights))
                                     
    pill_or_split = indexbox(msg="Would you like to find yarns that are less likely to pill,\n or yarns that are less likely to split?", title=title, 
                                choices=("Less Pilly", "Less Splitty"))                                 

    inputs = [pill_or_split, num_fibers_input, fiber_type_input, machine_wash_input, company_name_input, yarn_weights_input]

    return inputs
    
def return_results(search_df, inputs):
    '''copy the pandas dataframe of search space 
	and filter it down to only the results matching the user's query.
	if user did not make a selection for a given filter, skip filtering of dataframe'''
    pill_or_split, num_fibers_input, fiber_type_input, machine_wash_input, company_name_input, yarn_weights_input = inputs

    df2 = search_df.copy()

    if num_fibers_input != 2:
        df2.query('num_fibers == @num_fibers_input')
        
    if machine_wash_input != 2:
        df2.query('machine_washable == @machine_wash_input')
    
    if fiber_type_input != None and len(fiber_type_input) != len(fiber_names):
        #get only rows with non-excluded fibers
        exclude_these_fibers = [x for x in fiber_names if x not in fiber_type_input]
        df2 = df2[~df2['fiber_type'].str.contains('|'.join(exclude_these_fibers), case=False)]
    
    if company_name_input != None:
        #get only rows for this company
        df2 = df2[df2['company_name'].str.contains(company_name_input, case=False)]
    
    if yarn_weights_input != None and len(yarn_weights_input) != len(yarn_weights):
        #get only rows for these weights
        exclude_these_weights = [x for x in yarn_weights if x not in yarn_weights_input]
        df3 = df2['weight_name'].str.contains('|'.join(exclude_these_weights), case=False)
        df2 = df2[~df3]
    
	'''if search is too narrow to return any results, 
	tell the user and give them option to either search again or exit the program'''
    if len(df2) == 0:
        if ccbox(msg='Sorry, your search returned no results. Try again?', title=title, choices=('New Yarn Search', 'Exit')):
            one_run(search_df)
        else:
            sys.exit(0)            
			
	'''otherwise, build text to display the query to the user'''
    else:    
        you_searched_for = 'You searched for yarn:'
        
        you_didnt_specify = "You didn't specify:"
        
        if num_fibers_input == 0:
            you_searched_for = '\n\t'.join([you_searched_for, '- composed entirely of a single fiber'])
        elif num_fibers_input == 1:
            you_searched_for = '\n\t'.join([you_searched_for, '- composed of a blend of fibers'])
        else:
            you_didnt_specify = '\n\t'.join([you_didnt_specify, '- a number of fibers'])
            
        if machine_wash_input == 0:
            you_searched_for = '\n\t'.join([you_searched_for, '- that is machine washable'])
        elif machine_wash_input == 1:
            you_searched_for = '\n\t'.join([you_searched_for, '- that is not machine washable'])
        else:
            you_didnt_specify = '\n\t'.join([you_didnt_specify, '- a preference for machine washability'])
        
        if fiber_type_input == None:
            you_didnt_specify = '\n\t'.join([you_didnt_specify, '- a preference for fiber types'])
        else:
            fibers = ', '.join(fiber_type_input)
            you_searched_for = ''.join([you_searched_for, '\n\t- composed of any of these fibers:  ', fibers])
            
        if company_name_input == None:
            you_didnt_specify = '\n\t'.join([you_didnt_specify, '- a yarn brand'])
        else:
            you_searched_for = ''.join([you_searched_for, '\n\t- made by: ', company_name_input])
            
        if yarn_weights_input == None:
            you_didnt_specify = '\n\t'.join([you_didnt_specify, '- any yarn weights'])
        else:
            weights = ', '.join(yarn_weights_input)
            you_searched_for = ''.join([you_searched_for, '\n\t- matching any of these yarn weights:  ', weights])
        
		'''show user their query'''
        print_out = '\n\n'.join([you_searched_for, you_didnt_specify, 'Click OK to see your results'])    
        textbox(msg='', title=title, text=print_out, codebox=0)

    return df2, inputs

    
def print_results(df2, inputs):
    
    pill_or_split, num_fibers_input, fiber_type_input, machine_wash_input, company_name_input, yarn_weights_input = inputs

	'''if there are more than 50 results, only display the top 50'''
    if len(df2) > 50:
        num_recs = 50
		
	'''otherwise, display all of them'''
    else:
        num_recs = len(df2)

    '''store the string needed to make permalinks into URLs for display'''
	url_root = 'http://www.ravelry.com/yarns/library/'
    
	'''initalize a list of lists for display table of results'''
	table = []

    if pill_or_split==0:
		'''if user requested 'less pilly', sort yarns by least to most pilly, 
		assign pill_rank as the score to display, and create 'pill' message'''
        df2.sort_values(by="pill_rank", ascending=True, inplace=True)
        get_score = df2["pill_rank"]
        msg = "Here are your top results! \nA lower score means the yarn is less likely to pill.\n\nYou'll need to login to Ravelry.com to view the yarn pages."

    else:
        '''if user requested 'less splitty', sort yarns by least to most splitty, 
		assign split_rank as the score to display, and create 'split' message'''
		df2.sort_values(by="split_rank", ascending=True, inplace=True)
        get_score = df2["split_rank"]
        msg = "Here are your top results! \nA lower score means the yarn is less likely to split.\n\nYou'll need to login to Ravelry.com to view the yarn pages."
          
    for i in range(num_recs):
		'''for each line in request results: paste together the yarn URL, 
		extract data from results dataframe by index location 
		and format if necessary (eg, strip brackets from list, round off floats),
		form a list from each row of results,
		and append the list to the results table'''
        yarn_url = url_root + df2["permalink"].iloc[i]
        score, brand, name, weight, fibers, rating, url = round(get_score.iloc[i],2), df2["company_name"].iloc[i], df2["yarn_name"].iloc[i], df2["weight_name"].iloc[i], df2["fiber_type"].iloc[i].strip('[]'), round(df2["rating_avg"].iloc[i],2), yarn_url
        table.append([score, brand, name, weight, fibers, rating, url])
        
    '''assign headers'''
	headers = ["Score", "Brand", "Yarn Name", "Weight", "Fiber Content", "User Rating", "Link"]
    
	'''fancy formatting for results table'''
	results_table = tabulate(table, headers, tablefmt="fancy_grid", stralign="left", numalign="left")
    
	'''display results in easygui'''
	textbox(msg=msg, title=title, text=results_table, codebox=1)
    
	'''give user option of searching again, or exiting program'''
    if ccbox(msg='Would you like to perform another search?', title=title, choices=('New Yarn Search', 'Exit')):
		one_run(search_df)
    else:
        sys.exit(0)    


def one_run(search_df):
	'''call functions above to get and save user input, 
	return dataframe of results, 
	and print both the query and the results'''
    results_df, inputs = return_results(search_df, get_search_params(title))
    print_results(results_df, inputs)


#welcome message
msgbox("Welcome to Yarnatron! We'll help you find the best yarn from Ravelry.", ok_button="I'm ready!")

#run the program
one_run(search_df)