# -*- coding: utf-8 -*-
"""EDA-1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J9UNpAk8RsJ7VHp3O4MOE7CzUQ_10QMQ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("data_clean.csv")
data

from google.colab import drive
drive.mount('/content/drive')

data.info()

print(data)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

data = pd.read_csv("data_clean.csv")
data

print(type(data))
print(data.shape)
print(data.size)

data1 = data.drop(['Unnamed: 0',"Temp C"], axis =1)
data1

data1.info()

#Convert the month column data type to float data type
data1['Month']=pd.to_numeric(data['Month'],errors='coerce')
data1.info()

data1[data1.duplicated()]

data1[data1.duplicated(keep=False)]

#Drop duplicates rows
data1.drop_duplicates(keep='first',inplace=True)
data1

#Change column names (Rename the columns)
data1.rename({'Solar.R': 'Solar'},axis=1, inplace = True)
data1

#display data1 missing values count in each column using isnull().sum()
data1.isnull().sum()

#visualize data1 missing values using graph
cols = data1.columns
colors = ['yellow', 'blue']
sns.heatmap(data1[cols].isnull(),cmap=sns.color_palette(colors),cbar = True)

from google.colab import files
uploaded = files.upload()

#Find the mean and median values of each numeric column
#Imputation of missing values with median
median_ozone = data1['Ozone'].median()
mean_ozone = data1['Ozone'].mean()
print("Median od Ozone: ", median_ozone)
print("Mean of Ozone: ", mean_ozone)

#replace the Ozone missing values with median value
data1['Ozone'] = data1['Ozone'].fillna(median_ozone)
data1.isnull().sum()

#replace Na values for solar column
#replace the Ozone missing values with median value
data1['Solar'] = data1['Solar'].fillna(median_ozone)
data1.isnull().sum()

median_Solar = data1['Solar'].median()
mean_Solar = data1['Solar'].mean()
print("Median od Solar: ", median_Solar)
print("Mean of Soalr: ", mean_Solar)

#replace Na values for solar column
#replace the solar missing values with median value
data1['Solar'] = data1['Solar'].fillna(median_Solar)
data1.isnull().sum()

#PRINT THE DATA1 5 ROWS
data1.head()

#Find the mode values of categorical columns
print(data1["Weather"].value_counts(()))
mode_weather = data1["Weather"].mode()[0]
print(mode_weather)

#impute missing values (replace NaN with mode etc.) using fillna()
data1["Weather"] = data1["Weather"].fillna(mode_weather)
data1.isnull().sum()

#Impute the missing values (Replace NaN with mode etc.) of "Weather" using fillna
mode_month=data1["Month"].mode()[0]
data1["Month"]=data1["Month"].fillna(mode_month)
data1.isnull().sum()

#Replace the NaN valuee in month column by its mode category
mode_month = data1["Month"].mode()[0]
data1["Month"] = data1["Month"].fillna(mode_month)
data1.isnull().sum()

data.tail()

#Reset the index column
data1.reset_index(drop =True)

Detection of Outliers in the columns

method-1 using histograms and boxplot

#Detection of outliers
#Create a figure with two subplots, stacked vertically
fig, axes = plt.subplots (2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [1, 3]})
#Plot the boxplot in the first (top) subplot
sns.boxplot(data=data1 ["Ozone"], ax=axes[0], color='skyblue', width=0.5, orient='h')
axes[0].set_title("Boxplot")
axes[0].set_xlabel("Ozone Levels")
# Plot the histogram with KDE curve in the second (bottom) subplot
sns.histplot(data1 ["Ozone"], kde=True, ax=axes [1], color='purple', bins=30)
axes[1].set_title("Histogram with KDE")
axes[1].set_xlabel("Ozone Levels")
axes[1].set_ylabel("Frequency")
#Adjust Layout for better spacing
plt.tight_layout()
# Show the plot
plt.show()

'''### observations
-the ozone column has extreme values beyond 81 as seen from box Plot
-The same is confirmed from the below right = skewed histogram.'''

#Create a figure with two subplots,stacked vertically
sns.violinplot(data=data1["Ozone"],color='skyblue')
plt.title("Violin Plot")

#Show the plot
plt.show()

#Detection of outliers
#Create a figure with two subplots, stacked vertically
fig, axes = plt.subplots (2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [1, 3]})
#Plot the boxplot in the first (top) subplot
sns.boxplot(data=data1 ["Solar"], ax=axes[0], color='skyblue', width=0.5, orient='h')
axes[0].set_title("Boxplot")
axes[0].set_xlabel("Solar Levels")
# Plot the histogram with KDE curve in the second (bottom) subplot
sns.histplot(data1 ["Solar"], kde=True, ax=axes [1], color='purple', bins=30)
axes[1].set_title("Histogram with KDE")
axes[1].set_xlabel("Ozone Levels")
axes[1].set_ylabel("Frequency")
#Adjust Layout for better spacing
plt.tight_layout()
# Show the plot
plt.show()

#Extract outliers from boxplot for Ozone column
plt.figure(figsize=(6,2))
boxplot_data = plt.boxplot(data1["Ozone"],vert=False)
[item.get_xdata() for item in boxplot_data ['fliers']]#fliers are outliers#Method-2

#Extract outliers from boxplot for Ozone column
plt.figure(figsize=(6,2))
boxplot_data = plt.boxplot(data1["Ozone"],vert=False)
[item.get_xdata() for item in boxplot_data ['fliers']]#fliers are outliers#Method-2

mu = data1["Ozone"].describe()[1]
sigma = data1["Ozone"].describe()[2]
for x in data1["Ozone"]:
    if ((x < (mu - 3*sigma)) or ( x > (mu + 3*sigma))):
      print(x)

import scipy.stats as stats
#Create Q-Q plot
plt.figure(figsize=(8,6))
stats.probplot(data1["Ozone"],dist="norm",plot=plt)
plt.title("Q-Q plot for Outliers Detection",fontsize=14)
plt.xlabel("Therotical Quantiles",fontsize=12)

import scipy.stats as stats
#Create Q-Q plot
plt.figure(figsize=(8,6))
stats.probplot(data1["Solar"],dist="norm",plot=plt)
plt.title("Q-Q plot for Outliers Detection",fontsize=14)
plt.xlabel("Therotical Quantiles",fontsize=12)

'''Observations from Q-Q plot
-the data does not follow normal distribution as the data points are deviating significantli away from re line
-the data shows a right -skewed distribution and possible outliers

#Create a figure for voilin plot

sns.violinplot(data=data1["Ozone"], color='lightgreen')
plt.title("Violin Plot")
plt.show()

sns.violinplot(data=data1, x="Weather", y="Ozone", palette="Set2")

sns.violinplot(data=data1, x="Weather", y="Ozone", palette="Set3")

sns.violinplot(data=data1, x="Weather", y="Solar", palette="Set2")

sns.violinplot(data=data1, x="Ozone", y="Solar", palette="Set2")

sns.swarmplot(data=data1, x="Weather", y = "Ozone", color="orange",palette="Set2",size=6)

sns.stripplot(data=data1, x="Weather",y="Ozone",color="orange",palette="Set1", size=6, jitter=True)

sns.kdeplot(data=data1["Ozone"], fill=True, color="blue")
sns.rugplot(data=data1["Ozone"], color="black")

plt.scatter(data1["Wind"], data1["Temp"])

#Compute pearson corelation coefficient
#between wind speed and temperature
data["Wind"].corr(data1["Temp"])

#read all numeric cpolumns into a new table
data1_numeric = data1.iloc[:,[0,1,2,6]]
data1_numeric

data1.info()

#Read all numeric (continuous) columns into a new table data1_numeric
data1_numeric = data1.iloc[:,[0,1,2,6]]
data1_numeric

data1.head()

#print correlation coefficients for all the aove columns
data1_numeric.corr()

"""***bservations
*the highest correlation strength is observed between Ozone and temperature (0.597087)
*the next higher correlation is observed between Ozone and wind(-0.523738)
*the next higher correlation strength is observed between wind and temp(-0.441228)
*the least correlation strength is observed between solar and wind(-0.055874)***

"""

#Plot a pair plot between all numeric columns using seaborn
sns.pairplot(data1_numeric)

"""TRANSFORMATIONS

"""

#CREATING DUMMY VARIABLE FOR WEATHER COLUMN
data2=pd.get_dummies(data1,columns=['Month','Weather'])
data2

"""# New Section"""