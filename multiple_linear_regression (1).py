# -*- coding: utf-8 -*-
"""Multiple linear regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wxKOcFhIpY5X6GBtLlRVFn5YsidPJvge

ASSUMPTIONS IN MULTIPLELINEAR REGRESSION
- 1.LINEARITY: The relationship between the predictors and the response is linear.
- 2.INDEPENDENCE: Observations are independent of each other.
- 3.HOMOSCEDASTICITY: The residuals (differences blw observed and predicted values) exhibit constant variance at all levels of the predictor
- 4.NORMAL DISTRIBUTIONOF ERRORS: The residuals of the model are normally distributed
- 5.NO MULTICOLLINEARITY: The independent variables should not be too highly correlated with each other Violations of these assumptions may lead to in efficeincy in the regression parameters and unreliable predictors
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.graphics.regressionplots import influence_plot

cars=pd.read_csv("Cars.csv")
cars.head()

#rEARRANGE THE COLUMNS
cars = pd.DataFrame(cars, columns=["HP","VOL","SP","WT","MPG"])
cars.head()

"""DESCRIPTION OF COLUMNS
- HP: Horse power of car
- MPG: milege of the car
- VOL: volume of the cars(size)
- SP: Top speed of the car(Mlies per hour)
- WT: Weight of the car(ponds)
-

EDA
"""

cars.info()

#CHECK FOR MISSING VALUES
cars.isna().sum()

"""- There are no missing values
- There are 81 observations
- the data types of the columns are relevant and valid
"""

#Create a figure with two subplots (one above the other)
fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
#Creating a boxplot
sns.boxplot(data=cars, x='HP', ax=ax_box, orient='h')
ax_box.set(xlabel='') # Remove x Label for the boxplot
#Creating a histogram in the same x-axis
sns.histplot(data=cars, x='HP', ax=ax_hist, bins=30, kde=True, stat="density")
ax_hist.set(ylabel='Density')
#Adjust Layout
plt.tight_layout()
plt.show()

#Create a figure with two subplots (one above the other)
fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
#Creating a boxplot
sns.boxplot(data=cars, x='SP', ax=ax_box, orient='h')
ax_box.set(xlabel='') # Remove x Label for the boxplot
#Creating a histogram in the same x-axis
sns.histplot(data=cars, x='SP', ax=ax_hist, bins=30, kde=True, stat="density")
ax_hist.set(ylabel='Density')
#Adjust Layout
plt.tight_layout()
plt.show()

#Create a figure with two subplots (one above the other)
fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
#Creating a boxplot
sns.boxplot(data=cars, x='VOL', ax=ax_box, orient='h')
ax_box.set(xlabel='') # Remove x Label for the boxplot
#Creating a histogram in the same x-axis
sns.histplot(data=cars, x='VOL', ax=ax_hist, bins=30, kde=True, stat="density")
ax_hist.set(ylabel='Density')
#Adjust Layout
plt.tight_layout()
plt.show()

#Create a figure with two subplots (one above the other)
fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})
#Creating a boxplot
sns.boxplot(data=cars, x='WT', ax=ax_box, orient='h')
ax_box.set(xlabel='') # Remove x Label for the boxplot
#Creating a histogram in the same x-axis
sns.histplot(data=cars, x='WT', ax=ax_hist, bins=30, kde=True, stat="density")
ax_hist.set(ylabel='Density')
#Adjust Layout
plt.tight_layout()
plt.show()

"""Observations from box plot
- There are some extreme values (outliers) observed in towards the right tail of SP and HP distributions.
- In VOL and wT columns,  a few outliers are observed in both tails of their distributions.
- The extreme values of cars data may have come from the specially designed nAature of cars.
- As this is multi-dimensional data, the outliers with respect to spatial dimensions may have to be consideered while building the regression model
- As this is multi-dimensional data, the outliers with respect to spatiaasl dimensions may have to be considered while building the regression model

Checking for
"""

cars[cars.duplicated()]

# Pair plot
sns.set_style(style='darkgrid')
sns.pairplot(cars)

cars.corr()

"""Observations
- high corelation values are present in HP than SP
- negative values are present in MPG.
-b/w x and y,  all the x variable are showing moderate to high corellation strength , highest being between HP and MPG.
- Therefore this dataset qualifies for building multiple linear regression model to predict MPG
- Among x columns (X1,X2,X3 and X4), , some very high coreelation strengths are observed between SP vs HP, vOL vs WT
- The high corellation among x columns is not desirable as it might lead to multicollinearity problem.

Preparing a preliminary model considering all x columns
"""

#Build model
#import statsmodels.formula.api as smf
model1 = smf.ols('MPG~WT+VOL+SP+HP', data=cars).fit()

model1.summary()

"""****R-Squared values tells about how much of variability in y is explained by X.****

OBSERVATIONS:
- The R-squared and adjusted R-Squared values are good and about 75% of variability in y is explained by X columns
- The probability value with respect to f-statistic is close to zero, indicating that all or some of x columns are significant
- The p-values for VOL and WT are higher that 5% indicating some interaction issue among themselves,  which need to be further explored

PERFORMANCE METRICS FOR MODEL1
"""

#fIND THE PERFORMNACE METRICS
#CREATE A DATA FRAME WITH ACTUAL Y AND PREDICTED Y COLUMNS

df1 = pd.DataFrame()
df1["actual_y1"]=cars["MPG"]
df1.head()

#predict for the given X data columns
pred_y1=model1.predict(cars.iloc[:,0:4])
df1["pred_y1"] = pred_y1
df1.head()

#compute the mean squared error(MSE) for model
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(df1["actual_y1"], df1["pred_y1"])
print("MSE :", mse)
print("RMSE :", np.sqrt(mse))

"""Checking for multicollinearity among X-columns using VIF method"""

cars.head()

# Compute VIF values
rsq_hp = smf.ols('HP~WT+VOL+SP',data=cars).fit().rsquared
vif_hp = 1/(1-rsq_hp)

rsq_wt = smf.ols('WT~HP+VOL+SP',data=cars).fit().rsquared
vif_wt = 1/(1-rsq_wt)

rsq_vol = smf.ols('VOL~WT+SP+HP',data=cars).fit().rsquared
vif_vol = 1/(1-rsq_vol)

rsq_sp = smf.ols('SP~WT+VOL+HP',data=cars).fit().rsquared
vif_sp = 1/(1-rsq_sp)

# Storing vif values in a data frame
d1 = {'Variables':['Hp','WT','VOL','SP'],'VIF':[vif_hp,vif_wt,vif_vol,vif_sp]}
Vif_frame = pd.DataFrame(d1)
Vif_frame

