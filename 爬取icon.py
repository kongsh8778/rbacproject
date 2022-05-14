# @Time : 2022/5/8 21:04 
# @Author : kongsh
# @File : 爬取icon.py

import requests
from bs4 import BeautifulSoup


response = requests.get(
    url='http://fontawesome.dashgame.com/',
)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')
web = soup.find(attrs={'id': 'web-application'})

icon_list = []

for item in web.find_all(attrs={'class': 'fa-hover'}):
    tag = item.find('i')
    class_name = tag.get('class')[1]
    icon_list.append([class_name, str(tag)])

print(icon_list)
