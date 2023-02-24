<html><head></head><body>#!/usr/bin/env python
# coding: utf-8

# # Analyze Traffic Safety Data with Python
# 
# ### Try some of these resources for extra help as you work:
# 
# * [View the Analyze Traffic Safety Data with Python cheatsheet](https://www.codecademy.com/learn/case-study-analyze-traffic-safety/modules/traffic-safety-case-study/cheatsheet)
# * [View the solution notebook](./solution.html)
# * [Learn more about analyzing traffic safety data in this introductory article](https://www.codecademy.com/courses/case-study-analyze-traffic-safety/articles/analyze-traffic-safety-data-with-python-article)

# In[1]:


import pandas as pd
import datetime as dt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt


get_ipython().run_line_magic(&#39;matplotlib&#39;, &#39;inline&#39;)
# set plot theme and palette
sns.set_theme()
sns.set_palette(&#39;colorblind&#39;)


# ## Traffic data exploration

# ### 1. Inspect the traffic safety dataset
# 
# After running the first cell to load all necessary libraries, we need to load our dataset. Using pandas, load the dataset `traffic.csv` and save it as `traffic`. Inspect the first few rows.

# In[2]:


# load dataset
## YOUR CODE HERE ##
traffic = pd.read_csv(&#39;traffic.csv&#39;)

# inspect first few rows
## YOUR CODE HERE ##
traffic.head()


# ### 2. Inspect and format data types
# 
# The `traffic` data frame contains three columns: `Date`, `Crashes_per_100k`, and `Season`. In order to plot the `Crashes_per_100k` column as a time series, we need to make sure that the `Date` column is in date format. Inspect the data types in the data frame, convert the `Date` column to date format, and inspect the data types a second time.

# In[3]:


# inspect data types
## YOUR CODE HERE ##
traffic.info()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# The `traffic` dataframe consists of 3 columns and 180 rows. Luckily, there are no missing data to contend with. The number of crashes is normalized to the annual population per 100,000 people. We will also need to format the `Date` variable since Python does not yet recognize it as a datetime variable.
# 
# 
# </details>

# Convert the `Date` column to the date datatype using the `pd.to_datatime(column)` function.

# In[4]:


# convert Date to date format
## YOUR CODE HERE ##
traffic[&#39;Date&#39;] = pd.to_datetime(traffic[&#39;Date&#39;])

# inspect data types
## YOUR CODE HERE ##
traffic.info()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# By using the `pd.to_datetime()` function, we converted a character string object to the `datetime64[ns]` datatype. This will allow us to plot a time series of data points.
# 
# </details>

# ### 3. Visualize traffic safety data
# To get a sense of trends that may exist in the data, use seaborn&#39;s `sns.lineplot()` function to create a line plot of the `traffic` data with `Date` on the x-axis and `Crashes_per_100k` on the y-axis.

# In[5]:


# create line plot
## YOUR CODE HERE ##
sns.lineplot(x = &#39;Date&#39;, y=&#39;Crashes_per_100k&#39;, data = traffic)
plt.show()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# Looking at the line plot of our collision data, we can see the decreasing trend in crash rates from 2006 continuing until 2010 or 2011, and then crash rates begin increasing. The data for 2020 is very different from the preceding years.
#     
# There also appear to be cyclical patterns, which may indicate differing crash rates by season.
# 
# </details>

# ### 4. Visualize seasonal rates
# 
# Since we saw a fair amount of variance in the number of collisions occurring throughout the year, we might hypothesize that the number of collisions increases or decreases during different seasons. We can visually explore this with a box plot. 
# 
# Use `sns.boxplot()` with crash rate on the x-axis and season on the y-axis. Remove the anomolous 2020 data by adjusting the `data` parameter to `traffic[traffic.Date.dt.year != 2020]`.

# In[6]:


# create box plot by season
## YOUR CODE HERE ##
sns.boxplot(x = &#39;Date&#39;, y=&#39;Crashes_per_100k&#39;, data = traffic[traffic.Date.dt.year != 2020])
plt.show()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# Winter and Fall appear to have generally higher crash rates than Spring and Summer. Seasons may be the reason for the pattern in crash rates.
# 
# </details>

# ## Smartphone data exploration

# ### 5. Inspect the smartphone use dataset
# 
# The dataset `crashes_smartphones.csv` contains smartphone data from Pew Research Center matched to normalized crash rates from the `traffic` data frame for the years 2011 to 2019.
# 
# <details>
#     <summary style="display:list-item;"><b>Toggle for an overview of the variables in this dataset.</b></summary>
# 
# * `Month_Year`: a shortened date with only the month and year of the survey
# * `Crashes_per_100k`: the normalized crash rate matching the month and year of the smartphone usage survey
# * `Season`: Winter, Spring, Summer, or Fall
# * `Smartphone_Survey_Date`: the actual date the smartphone usage survey was conducted
# * `Smartphone_usage`: the percent of survey participants that owned and used a smartphone
# 
# </details>
# 
# Load the dataset as `smartphones` and inspect the first few rows.

# In[7]:


# import dataset
## YOUR CODE HERE ##
smartphones = pd.read_csv(&#39;crashes_smartphones.csv&#39;)

# inspect first few rows
## YOUR CODE HERE ##
smartphones.head()


# ### 6. Format date data type
# Similar to the  `traffic` data frame, the `smartphones` data frame has a date column that is not properly formatted. Convert the `Smartphone_Survey_Date` column to the date data type using the `pd.to_datetime()` function and then inspect the data types in the data frame.

# In[8]:


# convert Date to date format
## YOUR CODE HERE ##
smartphones[&#39;Smartphone_Survey_Date&#39;] = pd.to_datetime(smartphones[&#39;Smartphone_Survey_Date&#39;])

# inspect data types
## YOUR CODE HERE ##
smartphones.info()


# # change to datetime object
# ## YOUR CODE HERE ##
# smartphones[&#39;Smartphone_Survey_Date&#39;] = pd.to_datetime(smartphones[&#39;Smartphone_Survey_Date&#39;])
# 
# # inspect data types
# ## YOUR CODE HERE ##
# smartphones.info()

# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# There is a lot less data available for smartphone usage rates than there was for crash rates. The `smartphones` dataframe consists of 5 columns and 28 rows. Luckily, there are no missing data to contend with.
# 
# 
# </details>

# ### 7. Visualize smartphone use data
# Now let&#39;s take a look at smartphone use over time. Create a line plot of the `smartphones` data with `Smartphone_Survey_Date` on the x-axis and `Smartphone_usage` on the y-axis.

# In[9]:


# create line plot
## YOUR CODE HERE ##
sns.lineplot(x = &#39;Smartphone_Survey_Date&#39;, y=&#39;Smartphone_usage&#39;, data = smartphones)
plt.show()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# We can see a trend of smartphone usage increasing over time.
# 
# </details>

# ## Relationship exploration

# ### 8. Visualize crash rate by smartphone use
# A scatter plot with smartphone usage on one axis and crash rates on the other axis will give us an idea of whether there is a relationship between these two variables. 
# 
# Create a scatter plot with a regression line using seaborn&#39;s `sns.regplot()` with `Smartphone_usage` on the x-axis and `Crashes_per_100k` on the y-axis.

# In[10]:


# create scatter plot with regression line
## YOUR CODE HERE ##
sns.regplot(x = &#39;Smartphone_usage&#39;, y = &#39;Crashes_per_100k&#39;, data = smartphones)
plt.show()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# There appears to be a positive linear relationship between the rate of car crashes and the rate of adult smartphone usage in the U.S.
# 
# </details>

# ### 9. Check the correlation coefficient
# 
# To test whether the correlation between `Smartphone_usage` and `Crashes_per_100k` is statistically significant, we can calculate the Pearson&#39;s _r_ correlation coefficient and the associated _p_-value. 
# 
# Use `corr, p = pearsonr(column1, column2)` on the `Smartphone_usage` and `Crashes_per_100k` columns in the `smartphones` dataframe. Then use the provided code to print `corr` and `p` to see the results.

# In[11]:


# find Pearson&#39;s r and p-value
corr, p = pearsonr(smartphones.Smartphone_usage, smartphones.Crashes_per_100k)
## YOUR CODE HERE ## pearsonr(df.column1, df.column2)

# print corr and p
print(&#34;Pearson&#39;s r =&#34;,  round(corr,3))
print(&#34;p = &#34;, round(p,3))


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# The Pearson&#39;s r correlation coefficient is greater than 0.5, which indicates a moderately strong positive relationship. The p-value is less than 0.05. Together, this tells us that there is a statistically significant correlation between adult smartphone usage rates and car crash rates in the U.S. We have to be careful though: correlation does not mean causation, as the saying goes. Many other factors may be contributing to the rise in car crash rates from 2011 to 2019. 
# 
# </details>

# ## Analysis

# ### 10. Run a linear regression
# We can use a linear regression to predict crash rates based on smart phone usage. Let&#39;s regress crash rates on smartphone usage. Then we can predict the crash rate in 2020 and see if it matches the actual crash rate in 2020!
# 
# We have provided the code to convert the variables to NumPy arrays that will work with the modeling function. The `Smartphone_usage` array is saved as `X`, and the `Crashes_per_100k` array is saved as `y`.
# 
# Initiate the model by saving `LinearRegression()` to the variable `lm`. Then fit the model and run the regression with `.fit()`.

# In[20]:


# convert columns to arrays
X = smartphones[&#39;Smartphone_usage&#39;].to_numpy().reshape(-1, 1)
y = smartphones[&#39;Crashes_per_100k&#39;].to_numpy().reshape(-1, 1)
lm = LinearRegression()
lm.fit(X,y)


# # initiate the linear regression model
# ## YOUR CODE HERE ##
# lm = LinearRegression()
# 
# # fit the model
# ## YOUR CODE HERE ##
# 
# lm.fit(X, y)

# ### 11. Print and interpret regression coefficients
# 
# Let&#39;s see the values our model produced. Print the coefficients from our `lm` model. Then think about which parts of the regression line equation these values represent.

# In[21]:


# print the coefficients 
## YOUR CODE HERE ##
print(&#34;Coefficients: \n&#34;,lm.intercept_, lm.coef_)


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# The generic equation for a line is `y = b + (m * x)`, where `b` is the value where the the line intercepts the y-axis and `m` is the slope of the line. In this step, we learned the two coefficients of our linear model, `b = 120.6637` and `m = 0.6610`. So the equation for our linear model is `y = 120.6637 + (0.6610 * x)` and we can use this equation to predict new values of y from any new value of x.
#     
# We can also interpret the slope of 0.6610: every additional percentage point of smartphone usage is associated with an additional 0.6610 crashes per 100,000 people.
# </details>

# ### 12. Make a prediction
# 
# Let&#39;s assume smartphone usage was the same for 2020 as it was for 2019. This is a reasonable asssumption since the increase in smartphone usage that we observed in our plot started to plateau at the end of the time series. Let&#39;s use this approximation and our regression model to predict the crash rate in 2020.
# 
# From our model output, the regression line equation is `Crashes_per_100k = 120.6637 + (0.6610 * Smartphone_usage)`. Run the provided code to view the smartphone usage rate for 2019. Then substitute this value into the equation, using Python as a calculator to predict the crash rate for 2020.

# In[24]:


# get the smartphone usage rate from 2019
smartphones[smartphones[&#39;Month_Year&#39;] == &#34;Feb-19&#34;].Smartphone_usage


# In[29]:


# predict the crash rate in 2020 using the regression equation
## YOUR CODE HERE ##
Crashes_per_100k = 120.6637 + (0.6610 * smartphones.Smartphone_usage)


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# If the smartphone usage rate was the same in 2020 as in 2019 (81%), our model predicts that the crash rate in 2020 would be 174.205 crashes per 100,000 people.  
# 
# </details>

# ### 13. Compare to the actual rate
# 
# How good was our prediction? Get the actual crash rate for February of 2020 from the `traffic` dataframe using `pd.to_datetime(&#34;2020-02-01&#34;)` as the value for `Date`.

# In[32]:


# get the actual crash rate in Feb 2020
## YOUR CODE HERE ##
traffic[traffic[&#39;Date&#39;] == pd.to_datetime(&#34;2020-02-01&#34;)].Crashes_per_100k


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# The actual crash rate in Februrary of 2020 was only 157.8895, which was a fair bit lower than our prediction. 
# 
# </details>

# ### 14. Visualize the prediction
# 
# Let&#39;s plot our regression plot again, but let&#39;s add two new points on top:
# 
# * The predicted 2020 crash rate
# * The actual 2020 crash rate
# 
# Code has been provided for the original regression plot and a legend title. 
# 
# Add a scatter plot layer to add the 2020 predicted and actual crash rates that both used the 2019 smartphone usage rate. Use different colors and marker shapes for the predicted and actual 2020 crash rates.

# In[42]:


# recreate the regression plot we made earlier
sns.regplot(x = &#39;Smartphone_usage&#39;, y = &#39;Crashes_per_100k&#39;, data = smartphones)


# add a scatter plot layer to show the actual and predicted 2020 values
## YOUR CODE HERE ##
##sns.scatterplot(x = [x1,x2], y = [y1,y2], 
##hue = [&#39;predicted&#39;,&#39;actual&#39;] , style = ##[&#39;predicted&#39;,&#39;actual&#39;], 
##markers = [&#39;X&#39;,&#39;o&#39;], palette=[&#39;navy&#39;,&#39;orange&#39;], s=200)

# add legend title
#plt.legend(title=&#39;2020&#39;)
plt.show()


# <details>
#     <summary style="display:list-item; font-size:16px; color:blue;"><i>What did we discover in this step? Toggle to check!</i></summary>
# 
# By adding another layer to our regression plot, we can see the difference between the predicted and real crash rates in February 2020. This allows us to see how these values compare to the rest of the dataset. 
# 
# </details>
<script type="text/javascript" src="https://external-production.codecademy.com/assets/relay.js"></script></body></html>