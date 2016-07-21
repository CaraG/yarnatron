"""API AUTH"""
def ravelryLogin(uname, pw):
	"""auth for web scraping -- need to update/improve this function to be faster and simpler before submitting project"""
    br = mechanize.Browser();
    cj = cookielib.LWPCookieJar();
    br.set_cookiejar(cj);
    br.set_handle_equiv(True);
    br.set_handle_gzip(True);
    br.set_handle_redirect(True);
    br.set_handle_referer(True);
    br.set_handle_robots(False);
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1);
    br.addheaders = [('User-agent', 'Chrome')];
    br.open('https://www.ravelry.com/account/login');
    br.select_form(nr=0);
    br.form['user[login]'] = uname;
    br.form['user[password]'] = pw;
    br.submit();
    return br

"""GETTING DICT OF ALL YARNS WE WANT TO USE (HAVE COMMENTS, NOT 100% ACRYLIC)"""
def get_all_yarn_from_url(yarn_search_url, auth):
    all_yarns = {}       
        
    r = requests.get(yarn_search_url, auth=auth)
    numPages = 110 #to limit to top 5500 responses
    
    while numPages > 0: 
        yarn_list_url = yarn_search_url + '&page=' + str(numPages)
        r = requests.get(yarn_list_url, auth=auth)
        yarn_results_page = r.json()["yarns"]
        
        while len(yarn_results_page) > 0:    #while there are still more lines
            yarn = yarn_results_page.pop(0) #    #take one
    	
            all_yarns[yarn["id"]] = yarn["permalink"]
    
        if len(yarn_results_page) == 0:
            numPages -= 1
        
    #now i have a dictionary (key:value = yarn_id:yarn_permalink) for all yarns
    return all_yarns

def get_yarn_dict(yarn_search_url, yarn_search_url_del, auth):
    """
    to get top 6,000 yarns (by number of projects),  minus any yarns that are 100% acrylic
    """
    all_yarn_dict = get_all_yarn_from_url(yarn_search_url, auth)
    del_yarn_dict = get_all_yarn_from_url(yarn_search_url_del, auth)
        
    #remove 100% acrylic yarns from main dict
    for k in del_yarn_dict:
        all_yarn_dict.pop(k, None)
    
    return all_yarn_dict

"""CALL API, PARSE RESPONSE, SAVE YARN STATS"""
def getApiColumns():
	return ("num_fibers", "animal_fiber_list", "fiber_type_id_list", "fiber_type_name_list",
           "synthetic_list", "vegetable_list", "fiber_pct_list", "fiber_id_list", 
           "company_permalink", "company_name", "weight_name", "weight_knit_gauge",
           "weight_ply", "weight_wpi", "discontinued", "grams", "machine_washable",
           "yarn_name", "yarn_notes", "organic", "permalink", "rating_avg", 
           "rating_ct", "rating_tot", "texture", "wpi", "yardage", "gauge_divisor", 
           "max_gauge", "min_gauge", "company_id", "weight_id")
		   
def parseYarn(yarnID, auth):
	"""NEED TO COMMENT ON WHAT THIS FXN DOES"""
    yarn_url = 'https://foauth.org/api.ravelry.com/yarns/' + str(yarnID) + '.json'
    r = requests.get(yarn_url, auth=auth)
    try:
        yarn = r.json()['yarn']

        #initialize empty row so that all returned rows are the same length
        (num_fibers, animal_fiber_list, fiber_type_id_list, fiber_type_name_list, 
             synthetic_list, vegetable_list, fiber_pct_list, fiber_id_list, 
             company_permalink, company_name, weight_name, weight_knit_gauge, 
             weight_ply, weight_wpi, discontinued, grams, machine_washable, yarn_name,
             yarn_notes, organic, permalink, rating_avg, rating_ct, rating_tot, texture,
             wpi, yardage, gauge_divisor, 
             max_gauge, min_gauge, company_id, weight_id) = [None for dummy in range(32)]
        
        '''fiber stuff .. need to acct for more than 1 fiber type'''
        all_fibers = yarn["yarn_fibers"]
        
        num_fibers = len(all_fibers)
        
        animal_fiber_list = [all_fibers[i]["fiber_type"]["animal_fiber"] for i in range(num_fibers)]
        fiber_type_id_list = [all_fibers[i]["fiber_type"]["id"] for i in range(num_fibers)]
        fiber_type_name_list = [all_fibers[i]["fiber_type"]["name"] for i in range(num_fibers)]
        synthetic_list = [all_fibers[i]["fiber_type"]["synthetic"] for i in range(num_fibers)]
        vegetable_list = [all_fibers[i]["fiber_type"]["vegetable_fiber"] for i in range(num_fibers)]
        fiber_pct_list = [all_fibers[i]["percentage"]  for i in range(num_fibers)]
        fiber_id_list = [all_fibers[i]["id"] for i in range(num_fibers)]
        
        company_permalink = yarn["yarn_company"]["permalink"]
        company_name = yarn["yarn_company"]["name"]
        company_id = yarn["yarn_company"]["id"]
    
        try:
            weight_id = yarn["yarn_weight"]["id"] 	
            weight_name = yarn["yarn_weight"]["name"]
            weight_knit_gauge = yarn["yarn_weight"]["knit_gauge"]
            weight_ply = yarn["yarn_weight"]["ply"]
            weight_wpi = yarn["yarn_weight"]["wpi"]
            
        except KeyError:
            pass
        
        
        discontinued = yarn["discontinued"] #BOOLEAN
        grams = yarn["grams"]
        machine_washable = yarn["machine_washable"]	#BOOLEAN
        yarn_name = yarn["name"]
        yarn_notes = yarn["notes_html"]		#BLOB
        organic = yarn["organic"]   #BOOLEAN
        permalink = yarn["permalink"]		#NEEDED TO SCRAPE COMMENTS
        rating_avg = yarn["rating_average"]
        rating_ct = yarn["rating_count"]
        rating_tot = yarn["rating_total"]
        texture = yarn["texture"]
        wpi = yarn["wpi"]
        yardage = yarn["yardage"]
        
        gauge_divisor = yarn["gauge_divisor"] 	
        max_gauge = yarn["max_gauge"]  		
        min_gauge = yarn["min_gauge"]		    
            
        row_from_api = [num_fibers, animal_fiber_list, fiber_type_id_list, 
                        fiber_type_name_list, synthetic_list, vegetable_list, 
                        fiber_pct_list, fiber_id_list, company_permalink, company_name, 
                        weight_name, weight_knit_gauge, weight_ply, weight_wpi, 
                        discontinued, grams, machine_washable, yarn_name, yarn_notes,
                        organic, permalink, rating_avg, rating_ct, rating_tot, texture,
                        wpi, yardage, gauge_divisor, max_gauge, min_gauge, company_id, 
                        weight_id]
    	
        return np.array(row_from_api, dtype=object)

    except ValueError:
        pass

"""SCRAPE WEB, PARSE RESPONSE, SAVE YARN SUMMARY STATS"""
def getWebColumns():
	return ("common_price", "num_stashes", "num_projects", "num_comments", "last_updated")

def getYarnSumStats(permalink, br):
    yarn_url = 'http://www.ravelry.com/yarns/library/' + permalink
    
    br.open(yarn_url) #open url
    mainSoup = BeautifulSoup(br.response().read().decode('utf-8', 'ignore'))  #get, read and parse response

    #initialize empty row
    (commonPrice, numStashes, numProjects, numComments, lastUpdated) = [None for dummy in range(5)]
   
    lastUpdated = mainSoup.find("ul", class_="page_date_sidebar").get_text(strip=True) #NEED TO PARSE..
    check_commonPrice = mainSoup.find("div", class_="downloadable")
    if check_commonPrice is not None:
        commonPrice = (float(re.sub("\D", "", check_commonPrice.get_text())))/100 # in USD
    numStashes = int(re.sub("\D", "", mainSoup.find(id="stashes_tab").get_text())) #get total number of stashes
    numProjects = int(re.sub("\D", "", mainSoup.find(id="projects_tab").get_text())) #get total number of projects
    check_numComments = re.sub("\D", "", mainSoup.find(id="comments_tab").get_text()) #get total number of comments
    if check_numComments !='':
        numComments = int(check_numComments)
    else:
        numComments = 0
    row_from_web = [commonPrice, numStashes, numProjects, numComments, lastUpdated]
    	
    return np.array(row_from_web, dtype=object) 

"""GET COMMENTS, WRITE THEM TO CSV"""
def commentsHelper(soup):
    someComms = []    
    for comment in soup.find_all("div", class_="body markdown"):
        comm = comment.find_next('p')
        try:
            someComms.append(comm.get_text(strip=True))
        except AttributeError: #if comment is empty
            pass
    return someComms

def writeManyYarnComments(yarn_index, yarn_permalink, numComments, br): 
	#initialize stuff
    comments = []
    
    #initialize page iter
    numPages = (numComments / 25) + 1 #get total number of pages when using default of 25 comments
    
    # PER PAGE OF (UP TO 99) COMMENTS:
    while numPages > 0:
        #GET YARN COMMENTS URL
        yarn_comments_url = 'http://www.ravelry.com/yarns/library/' + yarn_permalink + '/comments?page=' + str(numPages)

        #DECREASE PAGE ITER
        numPages -= 1
        
        #GET RESPONSE -- YARN COMMENT PAGE
        try:
            br.open(yarn_comments_url) #open url
        except HTTPError:   #except if 404 (there are some errors on the website!)
            pass
            
        #MAKE SOUP
        soup = BeautifulSoup(br.response().read().decode('utf-8', 'ignore'))  #get, read and parse response
        
        #GET COMMENTS -- ONCE PER PAGE OF RESULTS
        comments.extend(commentsHelper(soup))
    
    comments = [comm.encode('utf-8') for comm in comments]
    comments.insert(0, yarn_index)    
    writer.writerows([comments])        
    
def writeFewYarnComments(yarn_index, yarn_permalink, br):
    yarn_comments_url = 'http://www.ravelry.com/yarns/library/' + yarn_permalink + '/comments?page_size=99&page=1'
    try:
        br.open(yarn_comments_url) #open url
    except HTTPError:    #except if 404 (there are some errors on the website!)
        pass
    soup = BeautifulSoup(br.response().read().decode('utf-8', 'ignore'))  #get, read and parse response

    #parse comments
    comments = [comm.encode('utf-8') for comm in commentsHelper(soup)]

    #add yarn index to beginning of list of comments    
    comments.insert(0, yarn_index)

    #append full row (index + all comments) to csv
    writer.writerows([comments]) 