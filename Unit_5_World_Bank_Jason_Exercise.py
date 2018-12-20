
# coding: utf-8

# # JSON examples and exercise
# ****
# + get familiar with packages for dealing with JSON
# + study examples with JSON strings and files 
# + work on exercise to be completed and submitted 
# ****
# + reference: http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-reader
# + data source: http://jsonstudio.com/resources/
# ****

# In[3]:


import pandas as pd


# ## imports for Python, Pandas

# In[6]:


import json
from pandas.io.json import json_normalize


# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas.pydata.org/pandas-docs/stable/io.html#normalization

# In[4]:


# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': {'governor': 'Rick Scott'},
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': {'governor': 'John Kasich'},
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[7]:


# use normalization to create tables from nested element
json_normalize(data, 'counties')


# In[8]:


# further populate tables created from nested element
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])


# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 
# + data source: http://jsonstudio.com/resources/

# In[9]:


# load json as string
json.load((open('data/world_bank_projects_less.json')))


# In[10]:


# load as Pandas dataframe
sample_json_df = pd.read_json('data/world_bank_projects_less.json')
sample_json_df


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[1]:


import pandas as pd


# In[2]:


import json
from pandas.io.json import json_normalize


# In[30]:


world_bank = pd.read_json((open('data/world_bank_projects.json')))


# In[33]:


print(type(world_bank))


# In[39]:


world_bank_projects = world_bank[['countryshortname','id']]
#world_bank.groupby('countryshortname').count()


# In[41]:


df= world_bank_projects.groupby('countryshortname').count()
#df1 = df.sort_values('score',ascending = False).groupby('pidx').head(2)
#print (df1)


# In[54]:


df1=df.sort_values('id',ascending=False)


# In[78]:


print('Answer 1 - Top 10 countries by number of projects')
print(df1.head(10))
# Top ten countries by number of projects


# In[96]:


# Create a themes dataframe and display it
wb_themes = pd.DataFrame(columns=['code', 'name'])
for row in world_bank.mjtheme_namecode:
    wb_themes = wb_themes.append(json_normalize(row))
wb_themes.reset_index(drop=True, inplace=True)


# In[98]:


wb_themes.head()


# In[100]:


df_wb= wb_themes.groupby('name').count()
df_wb


# In[101]:


df1_wb=df_wb.sort_values('code',ascending=False)


# In[102]:


print('Answer 2 - Top 10 Themes')
print(df1_wb.head(10))
# Top ten themes


# In[104]:


#create a list with all the non-null values
wb_themes.head()


# In[157]:


wb_themes_nn= wb_themes[wb_themes['name'] != '']
#eliminate the duplicates
wb_themes_nn = wb_themes_nn.drop_duplicates()
#wb_themes_nn


# In[158]:


wb_themes_ans3 = pd.merge(wb_themes, wb_themes_nn, on='code')


# In[159]:


wb_themes_ans3 = wb_themes_ans3.drop('name_x' , axis=1)


# In[160]:


print ('Answer 3  -  Project Theme Names Populated')
wb_themes_ans3.rename(index=str, columns={"code": "Code", "name_y": "Project_Theme"})

