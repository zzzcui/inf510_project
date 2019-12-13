
# coding: utf-8

# In[ ]:





# In[10]:


def analysis(filename):
    file = open(filename)

    result = []
    for item in file:
        result.append(item.replace('\n','').split('%'))

    ##Create db from inputfile

    import sqlite3
    conn = sqlite3.connect('cities.db')
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Citys')

    cur.execute('DROP TABLE IF EXISTS Citys')
    cur.execute('CREATE TABLE Citys (name VARCHAR(20) PRIMARY KEY, Housing INT, one_br VARCHAR(20),two_br VARCHAR(20),tem INT,uv INT,vis INT)')
    for city in result[1:]:
        cur.execute('INSERT INTO Citys(name,Housing,one_br,two_br,tem,uv,vis) VALUES (?,?,?,?,?,?,?)',(city[0],int(city[2]),city[3],city[4],int(city[5]),int(city[6]),int(city[7])))

    t = cur.execute('select two_br from Citys')
    sum = 0
    two_br = []
    for i in t:
        r = i[0].replace('$','').replace(',','')
        sum +=int(r)
        two_br.append(int(r))
    c = cur.execute('select count(*) from Citys')
    for item in c:
        count = item[0]
    avg_two_b = sum/int(count)
    median_two = sorted(two_br)[35]
    print('2b data')
    print('median',median_two)
    print('avg',avg_two_b)
    IQR_2b = 1.5*(sorted(two_br)[53]-sorted(two_br)[18])

    ranking = range(1,len(two_br)+1)
    import matplotlib.pyplot as plt
    plt.scatter(ranking,two_br,label= "stars", color= "green",  marker= "*",s =30)
    plt.xlabel('ranking')
    plt.ylabel('rental 2b rate')
    plt.title('ranking vs 2b rate,p1')
    plt.hlines(y = avg_two_b,xmin=0,xmax=70)
    plt.show()
    ##The mean rental fee for two bedroom apartment in these best living cities is 1026.2 and median is 958. This point out the data distribution is right-skewed. And from the plot, we could easier find out that there is no linear relationship between ranking and rent. Most of the rent is from 800 to 1200 in these cities.

    one = cur.execute('select one_br from Citys')
    sum_one = 0
    one_br = []
    for i in t:
        r = i[0].replace('$','').replace(',','')
        sum_one +=int(r)
        one_br.append(int(r))
    avg_one_b = sum_one/int(count)
    median_one = sorted(one_br)[35]
    print('1b data')
    print('median',median_one)
    print('avg',avg_one_b)
    plt.figure()
    plt.scatter(ranking,one_br,label= "stars", color= "blue",  marker= "s")
    plt.xlabel('ranking')
    plt.ylabel('rental 1b rate')
    plt.title('ranking vs 1b rate,p2')
    plt.hlines(y = avg_one_b,xmin=0,xmax=70)
    plt.show()
    
    ##Mean greater than median ==> right-skewed distribution. Most of the rent is from 600 to 800 in these cities. Compare with the previous graph, the shape is similar and the difference is about 200 between one bedroom and two bedrooms.

    diff = []
    for i in range(len(two_br)):
        sub = two_br[i]-one_br[i]
        diff.append(sub)
    plt.figure()
    plt.plot(ranking,diff,label= "diff", color= "purple",  marker= "8")
    plt.xlabel('ranking')
    plt.ylabel('diff')
    plt.title('ranking vs diff,p3')
    plt.show()

    tem = cur.execute('select tem from Citys')
    sum_tem = 0
    tem_list = []
    for i in tem:
        sum_tem += int(i[0])
        tem_list.append(int(i[0]))
    avg_tem = round(sum_tem/int(count),2)
    median_tem = sorted(tem_list)[35]
    print('temprature data')
    print('median',median_tem)
    print('avg',avg_tem)
    plt.figure()
    plt.scatter(ranking,tem_list,label= "stars", color= "yellow",  marker= "o")
    plt.xlabel('ranking')
    plt.ylabel('temp')
    plt.title('ranking vs temp,p4')
    plt.hlines(y = avg_tem,xmin=0,xmax=70)
    plt.show()
    ##From the graph, we could find out the temperature for the best living city is in the range from 0 to 20. It points out that people would like to live in the city that not too hot and not too cold.

    h = cur.execute('select Housing from Citys')
    sum_house = 0
    house = []
    for i in h:
        sum_house += int(i[0])
        house.append(int(i[0]))
    avg_housing = round(sum_house/int(count),2)
    
    median_housing = sorted(house)[35]
    print('house score')
    print('median',median_housing)
    print('avg',avg_housing)
    plt.figure()
    plt.plot(ranking,house)
    plt.xlabel('ranking')
    plt.ylabel('house score')
    plt.title('ranking vs house score,p5')
    plt.hlines(y = avg_housing,xmin=0,xmax=70)
    plt.show()
    ##There is no clear relationship between house score and ranking for the city. Housing is not a dominate varialbe in deciding the city is good for living or not.

    uv = cur.execute('select uv from Citys')
    sum_uv = 0
    uv_list = []
    for i in uv:
        sum_uv += int(i[0])
        uv_list.append(int(i[0]))
    avg_uv = round(sum_uv/int(count),2)
    median_uv = sorted(uv_list)[35]
    print('UV index')
    print('median',median_uv)
    print('avg',avg_uv)
    plt.figure()
    range1 = (1,10)
    bins = 8
    plt.hist(uv_list, bins, range1, color = 'brown', histtype = 'bar', rwidth = 0.5)
    plt.xlabel('uv')
    plt.ylabel('count')
    plt.title('uv histogram,p6')
    plt.show()

    plt.figure()
    plt.scatter(tem_list,uv_list)
    plt.xlabel('temp')
    plt.ylabel('uv')
    plt.title('temp vs uv,p7')
    plt.show()
    ##From the picture we could have a conclusion, the most comfortable uv for living is between 0 to 2. And there may have a relationship between uv and temp. The uv is increasing may cause the temp increased too.

    vis = cur.execute('select vis from Citys')
    sum_vis = 0
    vis_list = []
    for i in vis:
        sum_vis += int(i[0])
        vis_list.append(int(i[0]))
    avg_vis = round(sum_vis/int(count),2)

    median_vis = sorted(vis_list)[35]
    print('visibility')
    print('median',median_vis)
    print('avg',avg_vis)
    plt.figure()
    plt.scatter(ranking,vis_list)
    plt.xlabel('ranking')
    plt.ylabel('vis')
    plt.title('scatter ranking vs vis,p8')
    plt.show()
    ranges = (0,30)
    bins = 10
    plt.figure()
    
    plt.hist(vis_list, bins, ranges, color = 'yellow', histtype = 'bar', rwidth = 0.8)
    plt.xlabel('vis')
    plt.title('histgram distributionfor visibility,p9')
    plt.show()
    ##The change of visibility doesn't effect the rating for the city a lot. But we can see most of the high rating cities have a visibiblity within the range(15,20).

    from sklearn import linear_model
    import statsmodels.api as sm

    Temp = tem_list
    Vis = vis_list

    # Note the difference in argument order
    model = sm.OLS(Vis, Temp).fit()
    predictions = model.predict(Temp) # make the predictions by the model

    # Print out the statistics
    print(model.summary())
    # Because the r^2 is small, and we would like to consider there is no linear relationship between temp and visiiblity.

    Temp = tem_list
    UV = uv_list

    # Note the difference in argument order
    model = sm.OLS(UV, Temp).fit()
    predictions = model.predict(Temp) # make the predictions by the model

    # Print out the statistics
    print(model.summary())
    # There is a moderate relationship between temp and uv level.

    H_score = house
    one_bed = one_br

    # Note the difference in argument order
    model = sm.OLS(one_bed, H_score).fit()
    predictions = model.predict(H_score) # make the predictions by the model

    # Print out the statistics
    print(model.summary())
    #Using the value for house as x in the y = .2196*x+ constant to estimate the rent for one bedroom.



    #Find the relationship between house and ranking is strong. So house is an important part for ranking.
    # And comparing with temp and uv, the visibility is highly related to the rankin


# In[12]:





# In[ ]:




