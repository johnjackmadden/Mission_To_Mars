#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
# searching for elements with a specific combination of tag (div) and attribute (list_text)
# wait one second before searching for components; dynamic pg can take a while to load
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[ ]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[ ]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[ ]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[ ]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[ ]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[ ]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[ ]:


img_soup


# In[ ]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') # tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
img_url_rel


# In[ ]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[ ]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df.to_html()


# ### Hemisphere images

# In[9]:


# 1. Use browser to visit the URL 
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
item_url = "https://astrogeology.usgs.gov"
browser.visit(hemi_url)


# In[10]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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
    
    img_data=dict({'title':title, 'img_url':jpg_url})
    hemisphere_image_urls.append(img_data)


# In[11]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


browser.quit()


# In[ ]:




