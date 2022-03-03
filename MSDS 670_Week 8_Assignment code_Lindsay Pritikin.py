# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 20:37:30 2022

@author: linds
"""
#%% Import Libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import os
os.chdir('C:/Users/linds/OneDrive/Documents/MSDS/MSDS 670 - Data Visualization/Week 8')

#%% Import Dataset
df = pd.read_csv('SampleSuperstoreSubset.csv', encoding = 'unicode_escape')
df = df.drop(columns=['Unnamed: 21'])
df['Salesperson'] = df['Region']

#add in salespeople
for d in df['Salesperson']:
    if d == 'West':
        df['Salesperson'] = df['Salesperson'].replace('West','Anna Andreadi')
    elif d == 'East':
        df['Salesperson'] = df['Salesperson'].replace('East', 'Chuck Magee')
    elif d == 'Central':
        df['Salesperson'] = df['Salesperson'].replace('Central', 'Kelly Williams')
    else:
        df['Salesperson'] = df['Salesperson'].replace('South', 'Cassandra Brandow')
        
df['Order Date Year'] = pd.DatetimeIndex(df['Order Date']).year
df['Order Date Month'] = pd.DatetimeIndex(df['Order Date']).month  
df['Order Date Quarter'] = pd.DatetimeIndex(df['Order Date']).quarter

#change naming for quarters
for d in df['Order Date Quarter']:
    if d == 1:
        df['Order Date Quarter'] = df['Order Date Quarter'].replace(1,'Q1')
    if d == 2:
        df['Order Date Quarter'] = df['Order Date Quarter'].replace(2,'Q2')
    if d == 3:
        df['Order Date Quarter'] = df['Order Date Quarter'].replace(3,'Q3')
    if d == 4:
        df['Order Date Quarter'] = df['Order Date Quarter'].replace(4,'Q4')

#%% Performance by Year and Salesperson vs. Average

#sales by year and salesperson
year_df = pd.DataFrame(df.groupby(['Order Date Year', 'Salesperson'])['Sales'].sum().reset_index())

#average sales by year
average_df = year_df.groupby(['Order Date Year']).mean().reset_index()

#plot
fig, ax = plt.subplots(figsize=(12,8), facecolor='white')
fig = (80,80)
plt.rcParams['font.size'] = '12'
year_df.groupby('Salesperson').plot(x='Order Date Year', y='Sales', ax=ax, legend=False)
average_df.plot(x='Order Date Year', y='Sales', ax=ax, legend=False, color='lightgrey', linestyle='--')
ax.xaxis.set_ticks([2013, 2014, 2015, 2016])
ax.set_title('Sales by Year and Salesperson', fontsize=18)
ax.set_xlabel('')
def thousands(x, pos):
    return '${:1.0f}K'.format(x*1e-3)
ax.yaxis.set_major_formatter(thousands)

ax.text(2016.03, 146000, 'Kelly Williams', color='tab:red')
ax.text(2016.03, 139000, '(Central)', color='tab:red')
ax.text(2016.03, 212000, 'Chuck Magee', color='tab:green')
ax.text(2016.03, 205000, '(East)', color='tab:green')
ax.text(2016.03, 122000, 'Cassandra Brandow', color='tab:orange')
ax.text(2016.03, 115000, '(South)', color='tab:orange')
ax.text(2016.03, 249500, 'Anna Andreadi', color='tab:blue', fontweight='bold')
ax.text(2016.03, 242500, '(West)', color='tab:blue')
ax.text(2016.03, 183000, 'Average', color='tab:grey')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#%% Performance by Segment YOY

#sales by segment
segsales = df.groupby(['Order Date Year','Segment'])['Sales'].sum().reset_index()
segsales_2016 = segsales[segsales['Order Date Year']==2016].reset_index()
segsales_2015 = segsales[segsales['Order Date Year']==2015].reset_index()

#plot
fig, ax = plt.subplots(figsize=(12,8), facecolor='white')
plt.rcParams['font.size'] = '12'

labels = ['Consumer', 'Corporate', 'Home Office']
x = np.arange(len(labels)) 
y1 = segsales_2016['Sales'].values
y2 = segsales_2015['Sales'].values
width = 0.25

ax.set_title('2016 vs. 2015 Sales by Segment', fontsize=18)
ax.bar(x - (width/2), y1, width, label='2016', color='tab:blue')
ax.bar(x + (width/2), y2, width, label='2015', color='skyblue')
ax.legend()
ax.set_xticklabels(['','Consumer','','Corporate','', 'Home Office'], fontsize=13)
ax.tick_params(bottom=False)

def thousands(x, pos):
    return '${:1.0f}K'.format(x*1e-3)
ax.yaxis.set_major_formatter(thousands)

ax.text(-0.27, 335000, '+12% YOY', fontweight='bold')
ax.text(.725, 245000, '+17% YOY', fontweight='bold')
ax.text(1.73, 163000, '+52% YOY', fontweight='bold')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#%% +/- Horizontal bar chart

#2016 profits
profit = df.groupby(['Order Date Year','Sub-Category'])['Profit'].sum().reset_index()
profit2016 = profit[profit['Order Date Year']==2016].sort_values(['Profit'], ascending=False)
profit2016['Profit'] = profit2016['Profit'] / 1000
profit2016['Profit'] = pd.Series(["{0:.1f}".format(val) for val in profit2016['Profit']], index = profit2016.index)
profit2016['Profit'] = pd.to_numeric(profit2016['Profit'])

#plot
fig, ax = plt.subplots(figsize=(19,10), facecolor='white')
plt.rcParams['font.size'] = '14'
colors = ["green" if i > 0 else "firebrick" for i in profit2016['Profit']]
negatives = ['$-8.1K', '$-2.9K', '$-1.0K', '$-0.6K']

ax.barh(profit2016['Sub-Category'], profit2016['Profit'], color=colors)
ax.set_title('2016 Profit by Sub-Category', fontsize=18)
ax.set_xlabel('Profit')
def thousands(x, pos):
    return '${:.0f}K'.format(x)
ax.xaxis.set_major_formatter(thousands)

rects = ax.patches
for rect in rects:
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2
    x = "{0:.1f}".format(float(x_value))
    label = '$' + str(x) + 'K'
        
    if label in negatives:
        ax.annotate(
        label,                  
        (x_value, y_value),         
        xytext=(-42, -5),
        fontsize=12,
        textcoords="offset points")
    else:
        ax.annotate(
            label,                     
            (x_value, y_value),        
            xytext=(3, -5),   
            fontsize=12,
            textcoords="offset points") 
        
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#%% Seasonality by Product and by Quarter throughout the years

#2016 sales by quarter and subcategory
quartercat = df[df['Order Date Year']==2016].groupby(['Order Date Year', 'Order Date Quarter','Sub-Category'])['Sales'].sum().reset_index()

#pivot for heatmap
quartercatp = quartercat.pivot(index='Sub-Category', columns='Order Date Quarter', values='Sales')

#plot
fig, ax = plt.subplots(figsize=(10,10), facecolor='white')

df_formatted = quartercatp.applymap(
    lambda val: f'${val / 1000:,.0f}K')

sns.heatmap(quartercatp, annot=df_formatted, fmt='', cmap='Blues', ax=ax, cbar=False)

ax.set_title('Sub-Category Sales by Quarter\n2016\n')
ax.set_xlabel('')
ax.set_ylabel('')
ax.xaxis.tick_top()

#https://stackoverflow.com/questions/35003011/seaborn-heatmap-currency-format











