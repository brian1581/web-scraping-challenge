# Dependencies
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import requests

    ## Mars News 

def mars_news_final():
    # dictionary to be filled
    headlines = {}
    # list to be filled
    pgs = []

    # homepage url
    home_url = 'https://mars.nasa.gov/'
    # scrape url
    nasa_url = 'https://mars.nasa.gov/news/'
    # url response
    response = requests.get(nasa_url)
    time.sleep(5)
    # puts response in BeautifulSoup
    soup_resp = bs(response.text, 'html.parser')
    time.sleep(5)

    # class finder
    class_soup = soup_resp.find('div', class_='slide')
    # anchor finder
    anchor_soup = class_soup.find_all('a')
    # title cleaner
    title = anchor_soup[1].get_text().strip()

    # paragraph finder
    pg_soup = class_soup.find('a')
    # url for paragraphs
    url_soup = pg_soup['href']
    # combiner
    url_pgh = home_url + url_soup 
    # 2nd response
    next_response = requests.get(url_pgh)
    time.sleep(5)
    # 2nd response to BeautifulSoup
    scnd_response = bs(next_response.text, "html.parser")
    time.sleep(5)
    # class finder
    find_class = scnd_response.find(class_='wysiwyg_content')
    # paragraph finder
    find_para = find_class.find_all('p')

    # iterate and clean up the paragraph results
    for para in find_para:                                                 
        para_clean = para.get_text().strip()   
        pgs.append(para_clean) 

    # dictionary title
    headlines["news_title"] = title
    # summary
    headlines["first_pg_text"] = pgs[0]
    # detail
    headlines["second_pg_text"] = pgs[1]

    return headlines


    ## Mars Images


def mars_pics():
    # splinter
    browser = Browser('chrome', headless=False) 
    # images
    images = 'https://photojournal.jpl.nasa.gov/jpeg/'
    # search
    url_search = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 

    # define browser
    browser.visit(url_search)
    # visit the search URL with automated browser
    html_search = browser.html
    time.sleep(5)
    # url response
    soup_url = bs(html_search, 'html.parser')
    time.sleep(5)

    # create an image list
    image_list = []
    # iterate to find images
    for image in soup_url.find_all('div',class_="img"):
        image_list.append(image.find('img').get('src')) 

    # finds first image
    first_image = image_list[0]
    # split
    first_list = first_image.split('-')   
    # 2nd split
    scnd_list = first_list[0].split('/')
    # concatenate
    featured_image_url = images + scnd_list[-1] + '.jpg'

    browser.quit()

    return featured_image_url


    ## Mars Twitter Feed
    

def mars_twitter():

    # initialize the browser
    browser = Browser('chrome', headless=False)   
    # define url
    weather_tweet = 'https://twitter.com/marswxreport?lang=en'
    # visit url
    browser.visit(weather_tweet)
    # url response
    html_tweet = browser.html 
    time.sleep(5)
    # acquire URL response via BeautifulSoup
    soup_tweet = bs(html_tweet, 'html.parser')
    time.sleep(5)

    # create list to be filled
    mars_weather = []
    # iterates tweets from bs and adds to list
    for weather in soup_tweet.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        mars_weather.append(weather.text.strip()) 

    # look and iterate back on weather tweets
    for tweet in reversed(mars_weather):
        if tweet[:3]=='Sol':
            mars_weather = tweet

    browser.quit() 

    return mars_weather
    
    
    ## Mars Facts
    

def mars_factoids():

    # id the url
    facts = 'https://space-facts.com/mars/'
    # browser
    browser = Browser('chrome', headless=False) 
    # visit the page
    browser.visit(facts)
    time.sleep(5)
    # declare the page
    facts_page = browser.html

    # read into pandas
    pd_facts = pd.read_html(facts)
    # index
    df_facts = pd_facts[0]
    # name columns and set index
    df_facts.columns = ['Fact', 'Measurement']
    df_facts.set_index('Fact', inplace=True)

    # df to html
    html_facts = df_facts.to_html(header=False, index=False)

    return html_facts

    
    ## Mars Hemispheres
    

def mars_hemispheres():

    # browser
    browser = Browser('chrome', headless=False)                               
    # search url
    hemi_search = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # visit url
    browser.visit(hemi_search)
    time.sleep(3)
    # get response
    hemi_response = browser.html
    time.sleep(3)
    # soup
    hemi_soup = bs(hemi_response, 'html.parser') 

    # list to be filled
    hemi_images = []
    # product finder
    pics = hemi_soup.find('div', class_='result-list') 
    time.sleep(5)
    # hemi finder
    hemis = pics.find_all('div', class_='item')
    # iterate the hemis
    for hemi in hemis:
    # get title
        hemi_title = hemi.find('h3')
        try:
            hemi_text = hemi_title.text.replace('Enhanced', '')
            # note the links
            img_link = hemi.find('a')['href']
            search_img = 'https://astrogeology.usgs.gov/' + img_link 
        # auto click
            browser.visit(search_img)
        # get response
            hemi_html = browser.html
            time.sleep(3)
        # bs response
            hemi_soup2 = bs(hemi_html, 'html.parser')
            time.sleep(3)
        # find image link
            hemi_pics = hemi_soup2.find('div', class_='downloads').find('ul').find('li') 
            time.sleep(3)
            hemi_url = hemi_pics.find('a')['href']
        # dictionary
            hemi_images.append({'title': hemi_text, 'img_url': hemi_url})
        except:
            print('Not found')

    browser.quit()

    return hemi_images

# last function to use all above functions for final result

def scrape():
    browser = Browser('chrome', headless=False) 
    time.sleep(5)
    """ Main scraping function which uses the rest of the function
        Creates a results dictionary """

    results = {}

    results['headlines'] = mars_news_final()

    results['featured_image_url'] = mars_pics()

    results['mars_weather'] = mars_twitter()

    results['html_facts'] = mars_factoids()

    results['hemi_images'] = mars_hemispheres()

    return results

if __name__ == '__main__':
    
    print(scrape())