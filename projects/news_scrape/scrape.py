'''
Scrape the reuters site to get the title out and print.
Test Code for Docker
'''
import requests
from bs4 import BeautifulSoup

 


url = 'https://www.reuters.com/'
webdata = requests.get(url).text

 

soup = BeautifulSoup(webdata, 'html.parser')
print(soup.title.string)
