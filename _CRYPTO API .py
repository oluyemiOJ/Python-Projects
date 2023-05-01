#!/usr/bin/env python
# coding: utf-8

# # Automating Crypto Website API Pull

# In[7]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'500',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '052b2290-6f0d-412c-a5bf-c9495916c7e0',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[8]:


type(data)


# In[9]:


#This allows you to see all the columns, not just like 15

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[10]:


#This normalizes the data and makes it all pretty in a dataframe

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[11]:


def api_runner():


    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'500',
        'convert':'USD'
    }
    headers = { 
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '052b2290-6f0d-412c-a5bf-c9495916c7e0',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
     print(e)



    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')
    df
    
    if not os.path.isfile(r'C:\Users\USER\Documents\Python Scripts\API.csv'):
        df.to_csv(r'C:\Users\USER\Documents\Python Scripts\API.csv', header='column_names')
    else:
        df.to_csv(r'C:\Users\USER\Documents\Python Scripts\API.csv', mode='a', header=False)


# In[12]:


import os
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(60) #sleep for 1 minute
exit()    


# In[15]:


df72 = pd.read_csv(r'C:\Users\USER\Documents\Python Scripts\API.csv')
df72


# In[18]:


# One thing I noticed was the scientific notation. I want to be able to see the numbers in this case

pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[19]:


df


# In[20]:


# Taking look at the coin trends over time

df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3


# In[21]:


df4 = df3.stack()
df4


# In[22]:


type(df4)


# In[23]:


df5 = df4.to_frame(name='values')
df5


# In[24]:


type(df5)


# In[25]:


df5.count()


# In[28]:


#Because of how it's structured above we need to set an index. I don't want to pass a column as an index for this dataframe
#So I'm going to create a range and pass that as the dataframe. You can make this more dynamic, but I'm just going to hard code it


index = pd.Index(range(3000))

df6 = df5.reset_index()
df6



# In[29]:


# Changing the column name

df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[32]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['24h','7d','30d','60d','90d'])
df7


# In[30]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[33]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[40]:


# Now to do something much simpler
# creating a dataframe with the columns we want

df10 = df[['name','quote.USD.price','timestamp']]
df10 = df10.query("name == 'Ethereum'")
df10


# In[41]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df10)


# In[42]:


df11 = df[['name','quote.USD.price','timestamp']]
df11 = df11.query("name == 'Tether'")
df11


# In[43]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df11)


# In[ ]:





# In[44]:


df12 = df[['name','quote.USD.price','timestamp']]
df12 = df12.query("name == 'BNB'")
df12


# In[45]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df12)


# In[ ]:




