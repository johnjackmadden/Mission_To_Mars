import pandas as pd
import datetime as dt

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Extablish browser path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # Create an instance of the Browser class for Chrome and display actions
    # Initiate headless driver for deployment
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = mars_hemi(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls
    }

    # Stop webdriver and return data 
    browser.quit()
    return data

# Visit the mars nasa news site
def mars_news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    # searching for elements with a specific combination of tag (div) and attribute (list_text)
    # wait one second before searching for components; dynamic pg can take a while to load
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError: # Use AttributeError to return errors for bs/splinter
        return None,None

    return news_title,news_p

### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') # tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():    
    try:
        # Read grid into a data frame and cast it back to HTML
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException: #Use BaseException with Pandas
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    return df.to_html()

def mars_hemi(browser):
    # 1. Use browser to visit the URL 
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    hemisphere_image_urls = []

    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    items = hemi_soup.find_all('div', class_='description')

    for item in items:
        title = item.find_all('a', class_='itemLink product-item')[0].find("h3")
        
        item_url = "https://astrogeology.usgs.gov" + item.find_all('a', class_='itemLink product-item')[0]["href"]
        browser.visit(item_url)
        
        item_html = browser.html
        item_soup = soup(item_html, 'html.parser')
        
        jpg_url = item_soup.find("a", text="Sample").get("href")
        
        img_data=dict({'title':title.text, 'img_url':jpg_url})
        hemisphere_image_urls.append(img_data)

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())