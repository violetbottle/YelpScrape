# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 19:26:58 2017

@author: Sukanya
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import time
import re
import requests
import os

def getID(review):
    links_container = review.find("a",{"class":"biz-name js-analytics-click"})
    link = links_container.get('href',' ')
    urlName=re.findall('((?<=\/)[^\/?]*(?=[^\/]*$))',link)
    ID=urlName
 
    return ID
def reviewCount(review):
    count=0 # initialize critic and text 
    countChunk=review.find('span',{'class':re.compile('review-count.rating-qualifier')})
    if countChunk: count=countChunk.text#.encode('ascii','ignore')
    count=count.replace("reviews","")
    
    return count

def getHTML(ReviewID,Count):
    check=str(ReviewID).strip("['")
    check=check.strip("']")
    if not os.path.exists('F:/Fall 17/webAnalytics/Queens/' + check):
                os.makedirs('F:/Fall 17/webAnalytics/Queens/' + check)
    os.chdir('F:/Fall 17/webAnalytics/Queens/' + check)
    y=0
    p=0
    while y <= int(Count) or y <= 40:
        
        my_url = 'https://www.yelp.com/biz/' +check +'?start='+str(y)
        print(my_url)
        y = y + 20
            #Opening a connection and grabbing the page
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        
            #Parse the page as an HTML
        page_soup = BeautifulSoup(page_html.decode('ascii', 'ignore'),'lxml') 
            
        file = open('reviews_' + str(p) + ".html",'w')
        file.write(str(page_soup))
        p = p + 1  
        file.close
    return "success"

def run(url):

    pageNum=1# number of pages to collect

    
    
    for p in range(1,pageNum+1): # for each page 

        print ('page',p)
        html=None
        k=p*10
        if k==10: pageLink=url # url for page 1
        else: pageLink=url+'&start='+str(k) # make the page url
		
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
				
		
        if not html:continue # couldnt get the page, ignore
        
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
        reviews=soup.findAll('div',{'class':re.compile('search-result.natural-search-result')})
        sumReviews=0
        
        for review in reviews:  
            
        
            ReviewID=getID(review)
            Count = reviewCount(review)
            sumReviews=sumReviews+int(Count)
            getHTML(ReviewID,Count)
            
        print(sumReviews)
            
            

  

if __name__=='__main__':
    url='https://www.yelp.com/search?find_desc=Japanese+Korean+thai&find_loc=Queens'
    run(url)


