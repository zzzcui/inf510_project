
# coding: utf-8

# In[20]:


file = open('city_rent.txt')
towrite = open('city_rent.csv','w')


# In[21]:


towrite.write('rank,city,housing,oneb,twob,temp,uv,vis\n')
data = []
for item in file:
    data.append(item)
for item in data[1:]:
    re = item.strip().replace(',','.').split('%')
    towrite.write('{},{},{},{},{},{},{},{}\n'.format(re[1],re[0],re[2],re[3],re[4],re[5],re[6],re[7]))
towrite.close()
file.close()

