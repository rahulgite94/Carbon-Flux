#!/usr/bin/env python
# coding: utf-8

#                                             Data-601 Project-1 Proposal
# Description: One of the biggest problems this world is facing now is the emission of carbon dioxide. Since 1958 humans have added 200 gigatons of Carbon dioxide in the atmosphere. In order to measure the CO2 fluxes (in and out of the gas) many organizations has setup flux tower all over United States which measure the amount of CO2 exchanged between atmosphere and ecosystem.<br>
# My dataset contains 4 year (2015-2018) records of measurement from these flux towers. The data was gathered from Ameriflux (https://ameriflux.lbl.gov/).<br>
# My work is to clean this data and plot the visualization of it and then compare it with the visualization of similar data which is gathered from satellites. <br>
# 
# Dataset Description: <br>
# •	Column : 9<br>
# •	Rows : 324994<br>
# •	Size : 8 MB<br>
# •	Column Name :<br>
# 	Start: Timestamp when the reading started<br>
# 	Stop: Timestamp when the reading stopped<br>
# 	Dtime: Timestamp of the day of reading<br>
# 	Latitude: Latitude of the tower<br>
# 	Longitude: Longitude of the tower<br>
# 	Xco2: measurement taken by the tower device<br>
# 	Dstype: source of the data<br>
# 	StationId: This represent that from which station the data was taken<br>
# 

# In[1]:


##conda install -c anaconda basemap


# In[2]:


#conda install -c conda-forge proj4


# #### Importing necessary Libraries

# In[1]:


import pandas as pd
import datetime as dt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


data= pd.read_csv('FINAL_CO2_Values_ALL_Sites_3.csv')


# In[3]:


data.shape


# #### lets check few of the data

# In[4]:


data.head()


# In[5]:


data.tail()


# #### Lets see the data describe

# In[6]:


data.describe()


# In[7]:


data.describe(include='all')


# #### lets see the data types

# In[8]:


data.dtypes


# #### yeepiiee, No null values

# In[9]:


data.isnull().values.any()


# ### We got some overview lets start the cleaning
# #### I have no use of that unknown column so droping it.

# In[12]:


#data=data.drop(data.columns[0], axis=1)


# In[10]:


data.head()


# ### Now we will start with a Date

# In[14]:


data['start'].head()


# #### Unique values are 48

# In[15]:


data['start'].nunique()


# #### Value Count is also not telling much things

# In[11]:


data['start'].value_counts()


# #### We will be converting Date into its format

# data['start'] = data['start'].astype('str')
# data['start']=data['start'].str[0:6]

# In[18]:


data.head()


# data['start']=pd.to_datetime(data['start'], format='%Y%m')

# #### So we got date in proper format
# we got the date in YYYYMM format we didn't have day or time

# In[20]:


data.head()


# #### Similarly converting stop and dtime column

# data['stop'] = data['stop'].astype('str')
# data['stop']=data['stop'].str[0:6]
# data['stop']=pd.to_datetime(data['stop'], format='%Y%m')
# 
# data['dtime'] = data['dtime'].astype('str')
# data['dtime']=data['dtime'].str[0:6]
# data['dtime']=pd.to_datetime(data['dtime'], format='%Y%m')

# In[22]:


data.dtypes


# In[14]:


stationID=data.stationID.unique()
len(stationID)


# In[24]:


include=['datetime64[ns]'] 
for sid in stationID:
    print('Data describe for station:'+sid)
    print(data[data.stationID==sid].describe(include = include))
    print('---------------------------------------------------------------------------')


# #### Let's see what we got more to clean

# In[25]:


data.head()


# #### Lets jump to stationID

# In[26]:


data['stationID'].nunique()


# #### Taking all the station values in a list

# In[27]:


stationID=data.stationID.unique()
stationID


# #### We can change StationID type as category

# In[28]:


data['stationID']=data['stationID'].astype('category')


# In[29]:


data.dtypes


# In[30]:


data.head()


# #### Its time for oue main Column ie xco2

# In[31]:


data.describe()


# #### As we have different station and values associated with them, we should check for describe based on each station

# In[15]:


for sid in stationID:
    print('Data describe for station:'+sid)
    print(data[data.stationID==sid].describe())
    print('---------------------------------------------------------------------------')


# Let's check the count by plotting

# In[16]:


xco2CountBeforeClean=[]
for sid in stationID:
    df=data[data.stationID==sid].xco2
    xco2CountBeforeClean.append(df.count())


# In[17]:


f, ax = plt.subplots(figsize=(18,5)) 
ax.bar(stationID,xco2CountBeforeClean, width=0.2, color='b', align='center', label='Before cleaning')
plt.xlabel('Stations')
plt.ylabel('xco2')
ax.legend()
plt.show()


# #### The measurement of xco2 value depends on many factor like temperature, weather etc 
# #### The minimum and maximum range of the xco2 value is between (380 to 420)*
# 
# *(Comapred with other station values and suggestion of the expert)

# In[18]:


min_val=380
max_val=420
data=data[data['xco2']>min_val]
data=data[data['xco2']<max_val]


# In[19]:


data.describe()


# #### Refining  data which is lower than 3 times standard deviation minus its mean
# #### Refining  data which is greater than 3 times standard deviation plus its mean

# In[20]:


tower_mean=data['xco2'].mean()
tower_std=data['xco2'].std()
data=data[data['xco2']> (tower_mean - 3*tower_std)]
data=data[data['xco2']< (tower_mean + 3*tower_std)]


# #### Lets see the station wise describe

# In[21]:


for sid in stationID:
    print('Data describe for station:'+sid)
    print(data[data.stationID==sid].xco2.describe())
    print('--------------------------------------------')


# #### It would be more clear to see the plot of data before and after cleaning

# In[22]:


xco2CountAfterClean=[]
for sid in stationID:
    df=data[data.stationID==sid].xco2
    xco2CountAfterClean.append(df.count())


# In[23]:


f, ax = plt.subplots(figsize=(18,5))
ax.bar(stationID,xco2CountBeforeClean, width=0.2, color='b', align='center', label='before')
ax.bar(stationID,xco2CountAfterClean, width=0.4, color='g', align='center', label='after')
plt.xlabel('Station')
plt.ylabel('xco2(GtC)')
ax.legend()
plt.show()


# Ohhh we have removed lots of data from US-ADR, US_CF1 <br>
# may be these measuring towers has some error.<br>
# As we dont have much data from these station, it can affect our analysis.<br>
# 

# #### Now let us see the count of each data we have now

# In[25]:


sns.set(rc={'figure.figsize':(20,9)})
tips = sns.load_dataset("tips")
sns.set(style="whitegrid")
ax1=sns.barplot(x=stationID,y=xco2CountAfterClean, data=tips)
ax1.set(xlabel='Station', ylabel='xco2(GtC)')


# #### Bar plot mostly show us the count, lets see some better plots

# In[26]:


ax = sns.stripplot( x=data['stationID'],y=data['xco2'],data=tips, size=.6)


# 

# In[27]:


xco2_USA10=data[data.stationID=='US-A10'].xco2


# In[44]:


plt.hist(xco2_USA10, bins=100)
plt.xlabel('US-A10 xco2(GtC)')
plt.ylabel('Frequency')
plt.title('US-A10 Histogram')
plt.show()


# 

# 

# In[45]:


sns.set(style="whitegrid")
ax1=sns.scatterplot(x=data['stationID'],y=data['xco2'], data=tips)


# #### Plotting the heatmap for xco2 values based on latitude and longitude

# In[46]:


latitude=data.latitude.unique()
latitude=data.longitude.unique()
xco2=xco2CountAfterClean
df=pd.DataFrame({'longitude': data['longitude'], 'latitude': data['latitude'], 'value': data['xco2'] })

df_wide=df.pivot_table( index='longitude', columns='latitude', values='value' )
p2=sns.heatmap( df_wide )


# #### Conclusion: As we can see by cleaning and visulatization this show how much carbon Dioxide was released from these stations. And in the future scope will include much more complex basemap and the comparision with the visualtization of the satellites.

# In[ ]:




