
# coding: utf-8

# The first db

# In[2]:


import requests
from bs4 import BeautifulSoup


# In[3]:


best_place_url = 'https://livability.com/list/top-100-best-places-to-live/2019/10'
r = requests.get(best_place_url)
soup = BeautifulSoup(r.content, 'lxml')
main_table = soup.findAll('div',{"class" : "list"})[0]
main_body = main_table.find('ul')


# In[4]:


city_list = []
city_name_list = []
for city in main_body.findAll('li',{"class" : "list-item"}):
    for url in city.findAll('h3'):
        city_url = url.find('a').attrs['href']
        city_name = url.find('a').text
        city_list.append(city_url)
        city_name_list.append(city_name)


# In[5]:


for i in range(1,10):
    new_url = best_place_url+'?page='+str(i)
    r = requests.get(new_url)
    soup = BeautifulSoup(r.content, 'lxml')
    main_table = soup.findAll('div',{"class" : "list"})[0]
    main_body = main_table.find('ul')
    for city in main_body.findAll('li',{"class" : "list-item"}):
        for url in city.findAll('h3'):
            city_url = url.find('a').attrs['href']
            city_name = url.find('a').text
            city_list.append(city_url)
            city_name_list.append(city_name)


# In[6]:


city_url = []
for url in city_list:
    out = 'https://livability.com'+ url
    city_url.append(out)


# In[7]:


total = []
for i in range(len(city_url)):
    re = requests.get(city_url[i])
    soup = BeautifulSoup(re.content, 'lxml')
    main = soup.findAll('div',{'role':'main'})[0]
    main_result = main.find('table')
    result = main_result.findAll('td',{'class':'value'})
    single = []
    single.append(city_name_list[i])
    for item in result:
        single.append(item.text.replace('\n',''))
    total.append(single)


# In[10]:


import sqlite3
conn = sqlite3.connect('city_rates.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Rates')


# In[11]:


cur.execute('CREATE TABLE Rates (name VARCHAR(20) PRIMARY KEY, Civic INT, Demographics INT, Economy INT, Education INT, Health INT,Housing INT, Infrastructure INT)')
for city in total:
    cur.execute('INSERT INTO Rates(name,Civic,Demographics,Economy,Education,Health,Housing,Infrastructure) VALUES (?,?,?,?,?,?,?,?)',(city[0],int(city[1]),int(city[2]),int(city[3]),int(city[4]),int(city[5]),int(city[6]),int(city[7])))


# The second db

# In[34]:

try:
    rental_url = 'https://www.apartmentlist.com/rentonomics/national-rent-data/'
    res = requests.get(rental_url)
    soup = BeautifulSoup(res.content, 'lxml')
    all_info = soup.findAll('table',{'id':'tablepress-359'})[0]
    rental_info = all_info.find('tbody')


    # In[35]:


    rentals = []
    for rent in rental_info.findAll('tr'):
        type_loc = rent.find('td',{'class':'column-2'}).text
        if type_loc == 'City':
            city = []
            location = rent.find('td',{'class':'column-1'}).text
            one_br = rent.find('td',{'class':'column-3'}).text
            two_br = rent.find('td',{'class':'column-4'}).text
            city.append(location)
            city.append(one_br)
            city.append(two_br)
            rentals.append(city)


    # In[36]:


    cur.execute('DROP TABLE IF EXISTS Rentals')
    cur.execute('CREATE TABLE Rentals (name VARCHAR(20) PRIMARY KEY, one_br VARCHAR(20),two_br VARCHAR(20))')
    for rent in rentals:
        cur.execute('INSERT INTO Rentals(name,one_br,two_br) VALUES (?,?,?)',(rent[0],rent[1],rent[2]))
        


    # In[37]:


    result = []
    for city in total:
        for citys in rentals:
            if city[0] == citys[0]:
                out = []
                out.extend(city)
                out.extend(citys[1:])
                result.append(out)
except:
    print('please check the website')
    rental_url = 'https://www.apartmentlist.com/rentonomics/national-rent-data/'
    res = requests.get(rental_url)
    soup = BeautifulSoup(res.content, 'lxml')
    print(soup)

# In[38]:


api_key = '773fccf5d1628a20eed7fd7f8c8ac0e7'
import json
for city in result:
    name = city[0].split(',')[0]
    if name.find(' ') == -1:
        url ='http://api.weatherstack.com/current?access_key='+api_key+'&query='+name
    else:
        url ='http://api.weatherstack.com/current?access_key='+api_key+'&query='+str(name.split()[0])+'%20'+str(name.split()[1])
    
    inf = requests.get(url)
    try:
        current_w = json.loads(inf.text)['current']
        tem = current_w['temperature']
        wind_dg = current_w['wind_degree']
        pre = current_w['pressure']
        hum = current_w['humidity']
        uv = current_w['uv_index']
        vis = current_w['visibility']
        city.append(tem)
        city.append(wind_dg)
        city.append(pre)
        city.append(hum)
        city.append(uv)
        city.append(vis)
    except (IndexError,ValueError):
        continue


# In[39]:


file = open('city_rent.txt','w')
title = 'city,rank,housing,oneb,twob,temp,uv,vis'+'\n'
file.write(title)
towrite=''
for i in range(len(result)):
    towrite = str(result[i][0])+'%'+str(i+1)+'%'+str(result[i][6])+'%'+str(result[i][8])+'%'+str(result[i][9])+'%'+str(result[i][10])+'%'+str(result[i][14])+'%'+str(result[i][15])
    file.write(towrite)
    file.write('\n')


# In[40]:


file.close()


# final DB

# In[41]:


cur.execute('DROP TABLE IF EXISTS Citys')
cur.execute('CREATE TABLE Citys (name VARCHAR(20) PRIMARY KEY, Civic INT, Demographics INT, Economy INT, Education INT, Health INT,Housing INT, Infrastructure INT,one_br VARCHAR(20),two_br VARCHAR(20),tem INT,wind INT,pre INT,hum INT,uv INT,vis INT)')
for city in result:    
    cur.execute('INSERT INTO Citys(name,Civic,Demographics,Economy,Education,Health,Housing,Infrastructure,one_br,two_br,tem,wind,pre,hum,uv,vis) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(city[0],int(city[1]),int(city[2]),int(city[3]),int(city[4]),int(city[5]),int(city[6]),int(city[7]),city[8],city[9],int(city[10]),int(city[11]),int(city[12]),int(city[13]),int(city[14]),int(city[15])))
    


# In[42]:




