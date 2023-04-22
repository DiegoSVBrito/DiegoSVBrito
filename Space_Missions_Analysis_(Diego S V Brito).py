#!/usr/bin/env python
# coding: utf-8

# # Introduction

# <center><img src="https://i.imgur.com/9hLRsjZ.jpg" height=400></center>
# 
# This dataset was scraped from [nextspaceflight.com](https://nextspaceflight.com/launches/past/?page=1) and includes all the space missions since the beginning of Space Race between the USA and the Soviet Union in 1957!

# ### Install Package with Country Codes

# In[172]:


get_ipython().run_line_magic('pip', 'install iso3166')


# ### Upgrade Plotly
# 
# Run the cell below if you are working with Google Colab.

# In[173]:


get_ipython().run_line_magic('pip', 'install --upgrade plotly')


# ### Import Statements

# In[174]:


import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# These might be helpful:
from iso3166 import countries
from datetime import datetime, timedelta


# ### Notebook Presentation

# In[175]:


pd.options.display.float_format = '{:,.2f}'.format


# ### Load the Data

# In[176]:


df_data = pd.read_csv('mission_launches.csv')
display(df_data)


# # Preliminary Data Exploration
# 
# * What is the shape of `df_data`? 
# * How many rows and columns does it have?
# * What are the column names?
# * Are there any NaN values or duplicates?

# In[177]:


df_data.drop_duplicates()


# In[178]:


df_data.fillna(value=0)


# ## Data Cleaning - Check for Missing Values and Duplicates
# 
# Consider removing columns containing junk data. 

# In[179]:



df_data.drop(df_data.columns[[1]], axis=1, inplace=True)


# In[180]:


df_data.describe()


# ## Descriptive Statistics

# In[181]:



print(df_data.shape)
display(df_data)


# In[182]:


grouped = df_data.groupby(df_data.columns[-1])
launches_per_country = grouped[df_data.columns[0]].count()

launches_per_country = launches_per_country.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 10))

ax = launches_per_company.plot(kind='bar', legend=False)
ax.set_xlabel(df_data.columns[2])
ax.set_ylabel('Number of Launches')
ax.set_title('Number of Launches per Country')
plt.show()


# # Number of Launches per Company
# 
# Create a chart that shows the number of space mission launches by organisation.

# In[183]:


grouped = df_data.groupby(df_data.columns[1])
launches_per_company = grouped[df_data.columns[0]].count()

launches_per_company = launches_per_company.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 10))

ax = launches_per_company.plot(kind='bar', legend=False)
ax.set_xlabel(df_data.columns[2])
ax.set_ylabel('Number of Launches')
ax.set_title('Number of Launches per Company')
plt.show()


# In[ ]:





# # Number of Active versus Retired Rockets
# 
# How many rockets are active compared to those that are decomissioned? 

# In[184]:


def check_rocket_status(df_data):
    StatusActive = df_data['Rocket_Status'] == 'StatusActive'
    StatusRetired = df_data['Rocket_Status'] == 'StatusRetired'

    active_count = sum(StatusActive)
    retired_count = sum(StatusRetired)

    return active_count, retired_count

result = check_rocket_status(df_data)

labels = ['StatusActive', 'StatusRetired']
counts = [result[0], result[1]]

plt.bar(labels, counts)
plt.title('Rocket Status')
plt.xlabel('Status')
plt.ylabel('Count')
plt.show()


# In[ ]:





# # Distribution of Mission Status
# 
# How many missions were successful?
# How many missions failed?

# In[185]:


def check_Mission_Status(df_data):
    Success = df_data['Mission_Status'] == 'Success'
    Failure = df_data['Mission_Status'] == 'Failure'

    success_count = sum(Success)
    failure_count = sum(Failure)

    return success_count, failure_count

result = check_Mission_Status(df_data)

labels = ['Success', 'Failure']
counts = [result[0], result[1]]

plt.bar(labels, counts)
plt.title('Mission Status')
plt.xlabel('Status')
plt.ylabel('Count')
plt.show()


# In[186]:


df_data['Price'] = df_data['Price'].fillna(0)

df_data['Country'] = df_data['Location'].str.split(',').str[-1].str.strip()

# Drop Location column
df_data.drop(columns=['Location'], inplace=True)





display(df_data)



# # How Expensive are the Launches? 
# 
# Create a histogram and visualise the distribution. The price column is given in USD millions (careful of missing values). 

# In[187]:


grouped_expensive = df_data.groupby(df_data.columns[0])
lauch_expensive = grouped[df_data.columns[6]].count()
plt.hist(lauch_expensive, bins=20)

plt.title('How expensive is going to space')
plt.xlabel('date')
plt.ylabel('Price')
plt.show()


# In[188]:



get_ipython().system('pip install pycountry')
import plotly.express as px


import pycountry
import re


# Define a regular expression pattern to match country names
pattern = r'(\b{}\b)'.format('|'.join(pycountry.countries))

# Extract country names from the 'Location' column using the pattern
df_data['Country'] = df_data['Location'].str.extract(pattern, expand=False)

# Replace country names with their ISO codes
df_data['Country'] = df_data['Country'].apply(lambda x: pycountry.countries.get(name=x).alpha_3 if x else None)

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my-app")

def get_country(location):
    try:
        country = geolocator.geocode(location, exactly_one=True).raw['display_name'].split(",")[-1].strip()
    except:
        country = None
    return country

df['country'] = df['Location'].apply(get_country)


# # Use a Choropleth Map to Show the Number of Launches by Country
# 
# * Create a choropleth map using [the plotly documentation](https://plotly.com/python/choropleth-maps/)
# * Experiment with [plotly's available colours](https://plotly.com/python/builtin-colorscales/). I quite like the sequential colour `matter` on this map. 
# * You'll need to extract a `country` feature as well as change the country names that no longer exist.
# 
# Wrangle the Country Names
# 
# You'll need to use a 3 letter country code for each country. You might have to change some country names.
# 
# * Russia is the Russian Federation
# * New Mexico should be USA
# * Yellow Sea refers to China
# * Shahrud Missile Test Site should be Iran
# * Pacific Missile Range Facility should be USA
# * Barents Sea should be Russian Federation
# * Gran Canaria should be USA
# 
# 
# You can use the iso3166 package to convert the country names to Alpha3 format.

# In[ ]:


# Replace country names that need to be modified
df_data.loc[df_data['Country'] == 'Russia', 'Country'] = 'Russian Federation'
df_data.loc[df_data['Country'] == 'New Mexico', 'Country'] = 'USA'
df_data.loc[df_data['Country'] == 'Yellow Sea', 'Country'] = 'China'
df_data.loc[df_data['Country'] == 'Shahrud Missile Test Site', 'Country'] = 'Iran'
df_data.loc[df_data['Country'] == 'Pacific Missile Range Facility', 'Country'] = 'USA'
df_data.loc[df_data['Country'] == 'Barents Sea', 'Country'] = 'Russian Federation'
df_data.loc[df_data['Country'] == 'Gran Canaria', 'Country'] = 'Spain'

def get_country_code(name):
    country = pycountry.countries.get(name=name)
    return country.alpha_3 if country is not None and name != 'Russian Federation' else 'RUS'

df_data['Country_Code'] = df_data['Country'].apply(get_country_code)
df_data.loc[df_data['Country'] == 'USA', 'Country_Code'] = 'USA'
df_data.loc[df_data['Country'] == 'China', 'Country_Code'] = 'CHN'
df_data.loc[df_data['Country'] == 'Iran', 'Country_Code'] = 'IRN'
df_data.loc[df_data['Country'] == 'Russian Federation', 'Country_Code'] = 'RUS'
df_data.loc[df_data['Country'] == 'Spain', 'Country_Code'] = 'ESP'

import geopandas as gpd
import matplotlib.pyplot as plt


# In[196]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load GeoJSON file
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Group data by country and count the number of launches
grouped_per_country = df_data.groupby('Country')['Mission_Status'].count().reset_index(name='Launches')

# Merge data with GeoJSON file
merged = world.merge(grouped_per_country, left_on='name', right_on='Country', how='left')
merged['Launches'].fillna(0, inplace=True)

# Plot choropleth map
fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
ax.set_title('Number of Launches by Country')

merged.plot(column='Launches', cmap='Blues', linewidth=0.8, edgecolor='0.8', ax=ax, legend=True)

plt.show()









# # Use a Choropleth Map to Show the Number of Failures by Country
# 

# In[193]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load GeoJSON file
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Group data by country and count the number of failures
grouped_per_country = df_data[df_data['Mission_Status'] == 'Failure'].groupby('Country').count()['Mission_Status']
grouped_per_country = grouped_per_country.reset_index(name='count')

# Merge data with GeoJSON file
merged = world.merge(grouped_per_country, left_on='name', right_on='Country', how='left')
merged['count'].fillna(0, inplace=True)

# Plot choropleth map
fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
ax.set_title('Number of Launch Failures by Country')

merged.plot(column='count', cmap='Reds', linewidth=0.8, edgecolor='0.8', ax=ax, legend=True)

plt.show()


# In[ ]:





# # Create a Plotly Sunburst Chart of the countries, organisations, and mission status. 

# In[197]:


grouped_data = df_data.groupby(['Country', 'Organisation', 'Mission_Status'])['Mission_Status'].count().reset_index(name='count')
grouped_data = df_data.groupby(['Country', 'Organisation', 'Mission_Status'])['Mission_Status'].count().reset_index(name='count')
grouped_data['labels'] = grouped_data['Country'] + ' > ' + grouped_data['Organisation'] + ' > ' + grouped_data['Mission_Status']
grouped_data = grouped_data.sort_values('count', ascending=False)


# In[198]:


fig = px.sunburst(grouped_data, path=['Country', 'Organisation', 'Mission_Status'], values='count', color='Mission_Status',
                  color_discrete_sequence=px.colors.qualitative.Dark2, maxdepth=2, hover_data={'labels': True, 'count': True})
fig.update_layout(title='Launches by Country, Organisation, and Mission Status')
fig.show()


# In[200]:


df_data['Price'] = pd.to_numeric(df_data['Price'], errors='coerce')


# # Analyse the Total Amount of Money Spent by Organisation on Space Missions

# In[201]:


grouped_by_org = df_data.groupby('Organisation')['Price'].sum().reset_index(name='Total_Price')
grouped_by_org = grouped_by_org.sort_values('Total_Price', ascending=False)

import plotly.express as px
fig = px.bar(grouped_by_org, x='Organisation', y='Total_Price')
fig.show()


# In[ ]:





# In[ ]:





# # Analyse the Amount of Money Spent by Organisation per Launch

# In[202]:


# Group by organization and count the number of launches
grouped_by_org = df_data.groupby('Organisation')['Price'].agg(['sum', 'count']).reset_index()
# Calculate the cost per launch for each organization
grouped_by_org['Cost_per_Launch'] = grouped_by_org['sum'] / grouped_by_org['count']

grouped_by_org = grouped_by_org.sort_values('Cost_per_Launch', ascending=False)

# Create a bar chart to visualize the results
import plotly.express as px

fig = px.bar(grouped_by_org, x='Organisation', y='Cost_per_Launch',
             labels={'Organisation': 'Organization', 'Cost_per_Launch': 'Cost per Launch'})
fig.show()


# In[ ]:





# In[ ]:





# # Chart the Number of Launches per Year

# In[214]:


# convert the Date column to datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'], utc=True)

# extract the year from the date
df_data['Year'] = df_data['Date'].dt.year

# count the number of launches per year
launches_per_year = df_data.groupby('Year').size().reset_index(name='Count')


# In[218]:


# count the number of launches per year
launches_per_year = df_data.groupby(df_data['Date'].dt.year).size().reset_index(name='Num_Launches')

# Create a bar chart
fig = px.bar(launches_per_year, x='Date', y='Num_Launches', labels={'Date': 'Year', 'Num_Launches': 'Number of Launches'})

# Set title and axis labels
fig.update_layout(title='Number of Launches per Year', xaxis_title='Year', yaxis_title='Number of Launches')

# Show the plot
fig.show()


# # Chart the Number of Launches Month-on-Month until the Present
# 
# Which month has seen the highest number of launches in all time? Superimpose a rolling average on the month on month time series chart. 

# In[221]:



# Convert the Launch Date column to datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'], utc=True)

# Create a new column with the year and month of each launch
df_data['Year-Month'] = df_data['Date'].dt.strftime('%Y-%m')

# Group by year and month and count the number of launches
launches_per_month = df_data.groupby('Year-Month')['Unnamed: 0.1'].count().reset_index()
launches_per_month.columns = ['Year-Month', 'Num_Launches']

# Filter the data to only include launches until the present month
present_month = datetime.now().strftime('%Y-%m')
launches_per_month = launches_per_month[launches_per_month['Year-Month'] <= present_month]


# In[222]:



# Create a line chart
fig = px.line(launches_per_month, x='Year-Month', y='Num_Launches', labels={'Year-Month': 'Year-Month', 'Num_Launches': 'Number of Launches'})

# Set title and axis labels
fig.update_layout(title='Number of Launches Month-on-Month', xaxis_title='Year-Month', yaxis_title='Number of Launches')

# Show the chart
fig.show()


# # Launches per Month: Which months are most popular and least popular for launches?
# 
# Some months have better weather than others. Which time of year seems to be best for space missions?

# In[229]:


# Sort the list in ascending order
launches_per_month_sorted = sorted(launches_per_month, key=lambda x: x[1])

# Most popular month
most_popular_month = launches_per_month_sorted[-1][0]

# Least popular month
least_popular_month = launches_per_month_sorted[0][0]

# Rename the column in launches_per_month
launches_per_month = launches_per_month.rename(columns={'Year-Month': 'Month_Year', 'Num_Launches': 'Count'})


# In[230]:


# Most popular month
most_popular_month = max(launches_per_month, key=lambda x: x[1])[0]

# Least popular month
least_popular_month = min(launches_per_month, key=lambda x: x[1])[0]
# Create a scatter plot
fig = px.scatter(launches_per_month, x='Month_Year', y='Count', labels={'Month_Year': 'Month', 'Count': 'Number of Launches'})

# Set title and axis labels
fig.update_layout(title='Number of Launches per Month', xaxis_title='Month', yaxis_title='Number of Launches')

# Show the plot
fig.show()


# # How has the Launch Price varied Over Time? 
# 
# Create a line chart that shows the average price of rocket launches over time. 

# In[232]:


# Extract Date and Price columns
launch_prices = df_data[['Date', 'Price']]

# Create a histogram
fig = px.histogram(launch_prices, x='Date', y='Price', nbins=50, title='Launch Prices over Time')
fig = px.histogram(df_data, x="Price", nbins=50)

# Update layout
fig.update_layout(
    title_text="Distribution of Launch Prices",
    xaxis_title_text="Price (USD)",
    yaxis_title_text="Number of Launches",
    showlegend=False,
    bargap=0.1,
    xaxis=dict(gridcolor='rgb(225, 225, 225)'),
    yaxis=dict(gridcolor='rgb(225, 225, 225)')
)
# Set axis labels
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Price')

# Show the plot
fig.show()


# In[ ]:





# # Chart the Number of Launches over Time by the Top 10 Organisations. 
# 
# How has the dominance of launches changed over time between the different players? 

# In[233]:


# Get the top 10 organizations by number of launches
top_organizations = df_data['Organisation'].value_counts().nlargest(10)


# In[237]:


# Create a new dataframe with the number of launches by year for each of the top 10 organizations
df_top_organizations = df_data[df_data['Organisation'].isin(top_organizations.index)]
df_top_organizations = df_top_organizations.pivot_table(index=pd.to_datetime(df_top_organizations['Date']).dt.year,
                                                        columns='Organisation',
                                                        values='Mission_Status',
                                                        aggfunc='count',
                                                        fill_value=0)


# In[241]:


# create a new DataFrame with the number of launches by year
df_launches_by_year = df_data.groupby('Year').size().reset_index(name='Count')

# create a line plot
fig = px.line(df_launches_by_year, x='Year', y='Count', title='Number of Launches over Time')
fig.show()


# # Cold War Space Race: USA vs USSR
# 
# The cold war lasted from the start of the dataset up until 1991. 

# In[264]:


# convert 'Date' column to datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'], format='%Y-%m-%d')
# filter data for Cold War period
cold_war_data = df_data[(df_data['Date'] >= '1957-01-01') & (df_data['Date'] <= '1991-12-31')]

# group data by year and country, and calculate total number of launches
cw_launches = cold_war_data.groupby(['Country', pd.Grouper(key='Date', freq='Y')])[['Unnamed: 0.1']].count()
cw_launches.reset_index(inplace=True)

# filter data for Cold War period
cold_war_data = df_data[(df_data['Date'].dt.year >= 1957) & (df_data['Date'].dt.year <= 1991)]

# extract year and month from Date column
cold_war_data['Year'] = cold_war_data['Date'].dt.strftime('%Y')
cold_war_data['Month'] = cold_war_data['Date'].dt.strftime('%m')

# group data by year and country, and calculate total number of launches


# create a pivot table to display the data as a heatmap
cw_pivot = cw_launches.pivot_table(index='Country', columns=['Date'], values="Unnamed: 0.1", fill_value=0)


# In[266]:


# create histogram of launches per year
plt.hist(cw_launches[cw_launches['Country'] == 'USA']['Unnamed: 0.1'], bins=10, alpha=0.5, label='USA')
plt.hist(cw_launches[cw_launches['Country'] == 'USSR/Russia']['Unnamed: 0.1'], bins=10, alpha=0.5, label='USSR/Russia')

# add labels and title
plt.xlabel('Number of launches')
plt.ylabel('Frequency')
plt.title('Histogram of launches during the Cold War period (1957-1991)')

# add legend
plt.legend()

# display plot
plt.show()


# ## Create a Plotly Pie Chart comparing the total number of launches of the USSR and the USA
# 
# Hint: Remember to include former Soviet Republics like Kazakhstan when analysing the total number of launches. 

# In[277]:


import plotly.graph_objs as go
from plotly.subplots import make_subplots

# create pie chart for USSR
labels1 = ['USSR', 'Other Countries']
values1 = [ussr_total_launches, total_launches - ussr_total_launches]
fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1)])
fig1.update_layout(title='Total Number of Launches for the USSR')

# create pie chart for USA
labels2 = ['USA', 'Other Countries']
values2 = [usa_total_launches, total_launches - usa_total_launches]
fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2)])
fig2.update_layout(title='Total Number of Launches for the USA')

# display pie charts side-by-side
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)
fig.show()


# In[302]:


get_ipython().system('pip install --upgrade matplotlib')
import matplotlib.animation as animation
anim = animation.FuncAnimation(fig, update, frames=df_data['Year'].unique(), interval=1000, repeat=True)


# ## Create a Chart that Shows the Total Number of Launches Year-On-Year by the Two Superpowers

# In[316]:


import pandas as pd
import matplotlib.pyplot as plt

# group data by year and country and count the number of missions
grouped_data = df_data.groupby([df_data['Date'].dt.year, 'Country']).size().reset_index(name='count')

# get unique years and countries
years = grouped_data[df_data['Country'].isin(['USA', 'USSR', 'Russia'])]['Date'].unique()

# filter data to include only USA and USSR/Russia
usa_data = grouped_data[(grouped_data['Country'] == 'USA') & (grouped_data['Date'].isin(years))]
ussr_data = grouped_data[(grouped_data['Country'].isin(['USSR', 'Russia'])) & (grouped_data['Date'].isin(years))]

# create subplots for each country
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# plot line charts for USA and USSR/Russia launches
axs[0].plot(usa_data['Date'], usa_data['count'], marker='o', label='USA')
axs[0].plot(ussr_data['Date'], ussr_data['count'], marker='o', label='USSR/Russia')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Number of launches')
axs[0].set_title('Launches Year-On-Year by the Two Superpowers')
axs[0].legend()

# plot bar chart showing the difference in launches between USA and USSR/Russia
launch_diff = usa_data.set_index('Date')['count'] - ussr_data.set_index('Date')['count']
axs[1].bar(launch_diff.index, launch_diff.values)
axs[1].axhline(y=0, color='grey', linestyle='--')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Difference in launches (USA - USSR/Russia)')
axs[1].set_title('Difference in Launches Year-On-Year between USA and USSR/Russia')

# adjust spacing between subplots
fig.subplots_adjust(hspace=0.5)

# display plot
plt.show()






# In[ ]:





# ## Chart the Total Number of Mission Failures Year on Year.

# In[324]:


import pandas as pd
import matplotlib.pyplot as plt

# filter data to include only missions that failed
failed_missions = df_data[df_data['Mission_Status'] == 'Failure']

# group data by year and country and count the number of mission failures
grouped_data = failed_missions.groupby(['Date', 'Country']).size().reset_index(name='count')

# create subplots for USA and USSR/Russia data
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# plot data for USA
usa_data = grouped_data[grouped_data['Country'] == 'USA']
axs[0].plot(usa_data['Date'], usa_data['count'], label='USA', marker='o')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Total Number of Mission Failures')
axs[0].set_title('Total Number of Mission Failures Year On Year - USA')
axs[0].legend()

# plot data for USSR/Russia
ussr_data = grouped_data[grouped_data['Country'].isin(['USSR', 'Russia'])]
axs[1].plot(ussr_data['Date'], ussr_data['count'], label='USSR/Russia', marker='o')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Total Number of Mission Failures')
axs[1].set_title('Total Number of Mission Failures Year On Year - USSR/Russia')
axs[1].legend()

# adjust spacing between subplots
plt.subplots_adjust(wspace=0.3)

# display plot
plt.show()




# In[330]:


import pandas as pd
import matplotlib.pyplot as plt

# group data by year and count the number of failures
grouped_data = df_data.groupby(['Date']).agg(Mission_Status_failures=('Mission_Status', lambda x: sum(x == 'Failure')))

# reset index to make Date a regular column
grouped_data = grouped_data.reset_index()

# create line plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(grouped_data['Date'], grouped_data['Mission_Status_failures'], label='Total Failures', marker='o')

# set axis labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Total Number of Failures')
ax.set_title('Total Number of Mission Failures Year On Year')

# display plot
plt.show()


# ## Chart the Percentage of Failures over Time
# 
# Did failures go up or down over time? Did the countries get better at minimising risk and improving their chances of success over time? 

# In[328]:


import pandas as pd
import matplotlib.pyplot as plt

# group data by year and country and count the number of missions and failures
grouped_data = df_data.groupby(['Date', 'Country']).agg(Mission_Status_count=('Mission_Status', 'count'),
                                                         Mission_Status_failures=('Mission_Status', lambda x: sum(x == 'Failure')))

# calculate percentage of failures
grouped_data['Percentage of Failures'] = grouped_data['Mission_Status_failures'] / grouped_data['Mission_Status_count'] * 100

# reset index to make Date and Country columns regular columns
grouped_data = grouped_data.reset_index()

# filter data to include only data for the USA and USSR/Russia
grouped_data = grouped_data[grouped_data['Country'].isin(['USA', 'USSR', 'Russia'])]

# create subplots for USA and USSR/Russia data
fig, ax = plt.subplots(figsize=(10, 6))

# plot data for USA
usa_data = grouped_data[grouped_data['Country'] == 'USA']
ax.plot(usa_data['Date'], usa_data['Percentage of Failures'], label='USA')

# plot data for USSR/Russia
ussr_data = grouped_data[grouped_data['Country'].isin(['USSR', 'Russia'])]
ax.plot(ussr_data['Date'], ussr_data['Percentage of Failures'], label='USSR/Russia')

# set axis labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Percentage of Failures')
ax.set_title('Percentage of Mission Failures Year On Year')

# add legend
ax.legend()

# display plot
plt.show()



# In[ ]:





# In[ ]:





# # For Every Year Show which Country was in the Lead in terms of Total Number of Launches up to and including including 2020)
# 
# Do the results change if we only look at the number of successful launches? 

# In[331]:


import pandas as pd
import matplotlib.pyplot as plt

# filter data to include only launches up to and including 2020
df_data = df_data[df_data['Date'].dt.year <= 2020]

# group data by year and country and count the number of launches
grouped_data = df_data.groupby(['Date', 'Country']).size().reset_index(name='count')

# create a pivot table to aggregate the number of launches by year and country
pivoted_data = pd.pivot_table(grouped_data, values='count', index='Date', columns='Country', fill_value=0)

# create a new column for each country, with the cumulative sum of launches up to that year
for col in pivoted_data.columns:
    pivoted_data[f'{col}_cumsum'] = pivoted_data[col].cumsum()

# create a new column for each year, with the country that had the highest cumulative sum of launches up to that year
pivoted_data['leader'] = pivoted_data.iloc[:, -len(pivoted_data.columns)//2:-1].idxmax(axis=1)

# create stacked bar chart
fig, ax = plt.subplots(figsize=(12, 6))
pivoted_data.iloc[:, :-1].plot(kind='bar', stacked=True, ax=ax)

# iterate over each year and add a text label to show the country that was in the lead
for i, year in enumerate(pivoted_data.index):
    leader = pivoted_data.loc[year, 'leader']
    y_offset = pivoted_data.iloc[i, :-1].sum() * 0.05
    ax.text(i, y_offset, leader, ha='center', va='bottom', fontweight='bold')


# In[332]:


# set axis labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Total Number of Launches')
ax.set_title('Total Number of Launches by Country, with Leader Highlighted')

# display plot
plt.show()


# # Create a Year-on-Year Chart Showing the Organisation Doing the Most Number of Launches
# 
# Which organisation was dominant in the 1970s and 1980s? Which organisation was dominant in 2018, 2019 and 2020? 

# In[333]:



# Group data by year and organization and count the number of launches
grouped_data = df_data.groupby(['Year', 'Organisation']).size().reset_index(name='Count')

# Get unique years
years = grouped_data['Year'].unique()

# Create subplots for each organization
fig, axs = plt.subplots(len(grouped_data['Organisation'].unique()), figsize=(10, 25))




# In[337]:


# Iterate over organizations and plot line charts for the number of launches by year
for i, org in enumerate(grouped_data['Organisation'].unique()):
    org_data = grouped_data[grouped_data['Organisation'] == org]
    axs[i].plot(org_data['Year'], org_data['Count'])
    axs[i].set_xlabel('Year')
    axs[i].set_ylabel('Number of Launches')
    axs[i].set_title(org)


# In[338]:


# Adjust spacing between subplots
fig.subplots_adjust(hspace=0.5)

# Display plot
plt.show()


# In[ ]:




