from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

#Mac Users
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
# !which chromedriver

#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = mars_news(browser)
    
    results = {
        "title": news_title,
        "paragraph": news_p,
        "image_URL": jpl_image(browser),
        "weather": mars_weather_tweet(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemis(browser)
    }

    browser.quit()
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    news_title = mars_news_soup.find('div', class_='content_title').text
    news_p = mars_news_soup.find('div', class_='article_teaser_body').text
 
    return news_title, news_p

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(3)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    featured_image_route = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image_route}'

    return featured_image_url

def mars_weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url) 
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    
    mars_weather = tweet_soup.find('p', class_='TweetTextSize').text
    return mars_weather
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(url)[1]
    mars_df.columns = ['Property', 'Value']
    mars_df.set_index('Property', inplace = True)

    return mars_df.to_html(classes = 'table table-striped')
    
def mars_hemis(browser):
    #The website listed was down at the time of the assignment. An archive link was used as an alternative. 
    # url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    url = 'https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    
    for item in range(len(links)):
        hemi_dict = {}
        
        browser.find_by_css("a.product-item h3")[item].click()
        hemi_dict["title"] = browser.find_by_css("h2.title").text
        hemi_dict["img_url"] = browser.find_link_by_text("Sample").first["href"]
        hemisphere_image_urls.append(hemi_dict)
        browser.back()
    
    return hemisphere_image_urls