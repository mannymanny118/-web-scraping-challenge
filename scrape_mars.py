#imports dependancies

from splinter import Browser
from bs4 import BeautifulSoup
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__))) # sets current directory

def scrape():
    # starts browser 
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # loads first website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # waits 
    time.sleep(1)
    # creates a soup variable for scraping 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # scrapes first article name and description 
    news_titles = soup.find_all('div', class_='content_title')
    news_t = news_titles[1].text
    news_p = soup.find('div', class_='article_teaser_body').text
    # loads next website 
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    # waits 
    time.sleep(1)
    # creates a soup variable for scraping 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # scrapes img url
    featured_img_path = soup.find_all('img')[3]['src']
    # creates full img url 
    featured_img_url = 'https://www.jpl.nasa.gov' + featured_img_path
    # loads next website
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    # waits 
    time.sleep(1)
    # creates a soup variable for scraping 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # selects table with desired info
    info= soup.find(class_= 'widget widget_text clearfix')
    # stores table info 
    col1 = info.find_all(class_="column-1")
    col2 = info.find_all(class_="column-2")
    info_dict = {}
    # combines columns into one dict 
    for x in range(0, len(col1)):
        info_dict[col1[x].text] = col2[x].text
   
    # loads last website
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    # waits 
    time.sleep(1)
    # creates a soup variable for scraping 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # selects list of images 
    results = soup.find(class_="result-list")
    # stores image  title
    img_t = results.find_all("h3")
    # stores img page urls
    img_h = results.find_all("a")
    url_list = []
    # iterates through img pages to find img url 
    for y in range(0, len(img_h)):
        # creates url 
        url = "https://astrogeology.usgs.gov/"
        urly = url + img_h[y]['href']

        if (img_h[y]['href'] == img_h[y - 1]['href']) :
            continue 
        # opens sub page    
        browser.visit(urly)
        # scrapes img url 
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_link = results.find(class_="thumb")["src"]
        # stores img url 
        url_list.append(url + img_link)

    img_list = []
    # creates a list of dictionaries that contains the img title and url 
    for x in range(0, len(img_t)):
        img_dict = {"title":  img_t[x].text, "img_url": url_list[x]}
        img_list.append(img_dict)
    # stores all information into a dictionary 
    mars_dict = {
        "title": news_t,
        "para": news_p,
        "featured": featured_img_url,
        "info": info_dict,
        "imgs": img_list
    }
    
    return mars_dict




