
# coding: utf-8

# This exercise will require you to pull some data from the Qunadl API. Qaundl is currently the most widely used aggregator of financial market data.

# As a first step, you will need to register a free account on the http://www.quandl.com website.

# After you register, you will be provided with a unique API key, that you should store:

# In[37]:


# Store the API key as a string - according to PEP8, constants are always named in all upper case
API_KEY = 'PgKsKb5szSy4wVnrmFZ6'


# Qaundl has a large number of data sources, but, unfortunately, most of them require a Premium subscription. Still, there are also a good number of free datasets.

# For this mini project, we will focus on equities data from the Frankfurt Stock Exhange (FSE), which is available for free. We'll try and analyze the stock prices of a company called Carl Zeiss Meditec, which manufactures tools for eye examinations, as well as medical lasers for laser eye surgery: https://www.zeiss.com/meditec/int/home.html. The company is listed under the stock ticker AFX_X.

# You can find the detailed Quandl API instructions here: https://docs.quandl.com/docs/time-series

# While there is a dedicated Python package for connecting to the Quandl API, we would prefer that you use the *requests* package, which can be easily downloaded using *pip* or *conda*. You can find the documentation for the package here: http://docs.python-requests.org/en/master/ 

# Finally, apart from the *requests* package, you are encouraged to not use any third party Python packages, such as *pandas*, and instead focus on what's available in the Python Standard Library (the *collections* module might come in handy: https://pymotw.com/3/collections/).
# Also, since you won't have access to DataFrames, you are encouraged to us Python's native data structures - preferably dictionaries, though some questions can also be answered using lists.
# You can read more on these data structures here: https://docs.python.org/3/tutorial/datastructures.html

# Keep in mind that the JSON responses you will be getting from the API map almost one-to-one to Python's dictionaries. Unfortunately, they can be very nested, so make sure you read up on indexing dictionaries in the documentation provided above.

# In[12]:


# First, import the relevant modules
import requests
import json


# In[39]:


# Now, call the Quandl API and pull out a small sample of the data (only one day) to get a glimpse
# into the JSON structure that will be returned
r = requests.get('https://www.quandl.com/api/v3/datasets/FSE/AFX_X/data.json?start_date=2018-08-21&end_date=2018-08-21&api_key'+ API_KEY)


# In[40]:


# Inspect the JSON structure of the object you created, and take note of how nested it is,
# as well as the overall structure
print(r.text)


# These are your tasks for this mini project:
# 
# 1. Collect data from the Franfurt Stock Exchange, for the ticker AFX_X, for the whole year 2017 (keep in mind that the date format is YYYY-MM-DD).
# 2. Convert the returned JSON object into a Python dictionary.
# 3. Calculate what the highest and lowest opening prices were for the stock in this period.
# 4. What was the largest change in any one day (based on High and Low price)?
# 5. What was the largest change between any two days (based on Closing Price)?
# 6. What was the average daily trading volume during this year?
# 7. (Optional) What was the median trading volume during this year. (Note: you may need to implement your own function for calculating the median.)

# In[41]:


print ('1.Collect data from Frankfurt Stock Exchange');


# In[43]:


r = requests.get('https://www.quandl.com/api/v3/datasets/FSE/AFX_X/data.json?start_date=2017-01-01&end_date=2017-12-31&api_key' + API_KEY)


# In[46]:


print ('2. Convert JSON to DICTIONARY')
type(r.text)
r_dict = json.loads(r.text)
type(r_dict)


# In[47]:


r_dict_col = r_dict['dataset_data']['column_names']
print(r_dict_col)


# In[49]:


r_dict_data = r_dict['dataset_data']['data']
print(r_dict_data)


# In[53]:


#for loop on the data
price_r_d_min= (price[1] for price in r_dict_data if price[1] is not None)
price_r_d_max= (price[1] for price in r_dict_data if price[1] is not None)
print('3. Calculate what were the highest and lowest opening prices')
print(min(price_r_d_min), max(price_r_d_max))


# In[54]:


print(r_dict_data[1])


# In[56]:


#for loop on the data
price_r_d_diff= (price[2]-price[3] for price in r_dict_data if price[2] is not None and price[3] is not None)
print('4. Largest change in any one day (based on High and Low price)')
print(max(price_r_d_diff))


# In[92]:


#for loop to get the closing price
#create a list which will store all the prices
close_price = [] 
i=0
for price in r_dict_data:
    if close_price is None:
        close_price=price[4]
    else:
        close_price.append(price[4])


# In[101]:


print(close_price[1])


# In[118]:


# find the difference between the closing prices
diff=0
diff_list = []
for index,item in enumerate(close_price):
    if index == 0:
        diff=0
        #print(index,item,diff)
        diff_list.append(diff)
        diff=item
    else:
        diff= item-diff
        #print(index,item,diff)
        diff_list.append(diff)
        diff=item

print('5. Largest change between any two days')
max(diff_list)


# In[134]:


print('6. Average daily trading volume during this year')
price_r_sum= (price[6] for price in r_dict_data if price[6] is not None)

#total len
len1=0
for index in enumerate(r_dict_data):
    len1+=1
#price_r_len=len(price_r_sum)
price_avg = sum(price_r_sum) / len1
print(price_avg)

