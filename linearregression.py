# -*- coding: utf-8 -*-
"""CA_LinearRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15jMw_r1mEPoZD5Lya7kbNwfWPtJ7IB8o

Importing all the necessary libraries required to run the python code.
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE  
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.datasets as dataz
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE
# %matplotlib inline
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

"""Importing the dataset and examining it.
*  The Pandas library imported as pd offers data manipulation,cleaning and analysis
*   pd.read_csv helps to import and read the file in colab


"""

# Importing dataset and examining it
df = pd.read_csv("/content/telecom_customer_churn.csv")
pd.set_option('display.max_columns',None) #Will ensure that all columns are displayed

""".head() displays the top 5 rows of the dataset"""

#Display the top 5 rows
df.head()

"""Dataset.tail() displays the bottom 5 rows of the dataset"""

#Display the bottom 5 rows
df.tail()

df.describe() # Quick Description of the data

df.describe(include='all') # will include all variables

"""Data cleaning and preparation

Using df.drop() dropping ['Zip Code','Latitude','Longitude','Customer ID','Churn Category','City'] these variables from the dataset for optimal performance.
"""

df=df.drop(columns=['Zip Code','Latitude','Longitude','Customer ID','Churn Category','City'])

df.info()  # general information about the dataset, including data type and missing values.

"""Data Exploration

Using the seaborn library's  pairplot function a pairwise relationship in the dataset is plotted. .
"""

#Using Seaborn library 
sns.pairplot(df)

"""From the scatter plot, It is clear that age and total revenue has a weak correlation similarly age with total long distance charge also has very weak correlation. Number od dependents vs average monthly gb download has a weak correlation.Tenure in Months vs total revenue has a strong correlation. Similarly total charges has a strong correlation with total revenue."""

sns.heatmap(df.corr(), annot= True)

# Increase the size of the heatmap.
plt.figure(figsize=(16, 6))
# Store heatmap object in a variable to easily access it when you want to include more features (such as title).
# Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True)
# Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);

"""From the heatmap above, I observe that age is negatively correlated with average monthly gb download which means that an increase in one variable lead to a decrease in the other variable and a strong correlation between total charges vs total revenue which explains that as charges increase the total revenue increases too."""

#Heatmap with cluster information
sns.clustermap(df.corr(), method="complete",cmap='RdBu',annot=True,annot_kws={"size":5}, vmin=1,figsize=(10,7))

"""From the cluster map above, it is observed that there are two large groups, which again can be divided into three sub groups. Total extra data charges and total refunds fall in a group which together fall into another group with age and all these together combined fall into another group with longitude. Similarly total revenue and total charges are closely related, total revenue and total charges combined together form a group with tenure in months. All these combined in the cluster form a group with total long distance charges which again clubs with the prevoius groups form a group with monthly charges.

##Data manipulation and modelling

Since the machine learning models cannot work on strings or categorical variables, the categorical variable needs to be converted to numerical.The dataset has few categorical variables, they needs to be converted to numerical values. pd.get_dummies() is used to convert categorical data into dummy variables.
"""

df = pd.get_dummies(df, prefix = None)
df.head()

"""Using df.info() to print information about the dataFrame"""

df.info()

"""From the above observation it is noted that there are missing values for variables 'Avg Monthly Long Distance Charges' and 'Avg Monthly GB Download' .Filling the null values with mean."""

df['Avg Monthly Long Distance Charges'].fillna(df['Avg Monthly Long Distance Charges'].mean(),inplace = True)
df['Avg Monthly GB Download'].fillna(df['Avg Monthly GB Download'].mean(),inplace = True)

"""For the linear regression model, set a lable for prediction. Here the target or dependant variable is 'Total Revenue' denoted by Y and the independant variables denoted by x.
df.drop() method drops the dependant variable from x.
"""

#Linear Regression Model

X=df.drop(columns=['Total Revenue'])
Y=df.loc[:,'Total Revenue']

"""Splitting the data into train and test set by using train_test_split() function.
Here the data is divided into 70:30 ratio and random_state parameter gives same train and test sets accross different executions.
"""

X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size =0.3, random_state = 7)

"""Using .shape() function checking the size of the test and train sets."""

#print to check size of test and train
print(f'X_train: {X_train.shape}')
print(f'x_test: {X_test.shape}')
print(f'y_train: {Y_train.shape}')
print(f'y_test: {Y_test.shape}')

"""Normalizing the data using the standardscaler() function. By Observing the data its noted that the variables in the datasets are in different ranges, which might lead to a biased model. In order to avoid a biased model we scale the data."""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.values)
X_test_scaled = scaler.fit_transform(X_test.values)

"""# <font color='green'> Linear Regression

Linear regression analysis is used to predict the value of a variable based on the value of another variable. It attempts to model the relationship between two variables by fitting a linear equation to observed data.

Fit the linear regression model to get the predictions.
"""

from sklearn.linear_model import LinearRegression
lm = LinearRegression()

lm.fit(X_train_scaled, Y_train)
lm_pred = lm.predict(X_test_scaled)

Y_pred = lm.predict(X_test_scaled)
print(Y_pred)

print(lm.intercept_)

coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
coeff_df

"""Using evalution metrics to validate the results."""

from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(Y_test, Y_pred))
print('MSE:', metrics.mean_squared_error(Y_test, Y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))
print('R2 for train:', lm.score(X_train_scaled, Y_train))
print('R2 for test(cross validation):', lm.score(X_test_scaled, Y_test))

"""Replacing the null values with median to see if it alters the performance."""

# Importing dataset and examining it
df2 = pd.read_csv("/content/telecom_customer_churn.csv")
pd.set_option('display.max_columns',None) #Will ensure that all columns are displayed
df2=df2.drop(columns=['Zip Code','Latitude','Longitude','Customer ID','Churn Category','City'])
df2 = pd.get_dummies(df, prefix = None)
df2.head()

df2['Avg Monthly Long Distance Charges'].fillna(df2['Avg Monthly Long Distance Charges'].median(),inplace = True)
df2['Avg Monthly GB Download'].fillna(df2['Avg Monthly GB Download'].median(),inplace = True)

#Linear Regression Model with missing values replaced by median

X=df2.drop(columns=['Total Revenue'])
Y=df2.loc[:,'Total Revenue']
X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size =0.3, random_state = 7)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.values)
X_test_scaled = scaler.fit_transform(X_test.values)
from sklearn.linear_model import LinearRegression
lm = LinearRegression()

lm.fit(X_train_scaled, Y_train)
lm_pred = lm.predict(X_test_scaled)
Y_pred = lm.predict(X_test_scaled)
print(lm.intercept_)
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
coeff_df
from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(Y_test, Y_pred))
print('MSE:', metrics.mean_squared_error(Y_test, Y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))
print('R2 for train:', lm.score(X_train_scaled, Y_train))
print('R2 for test(cross validation):', lm.score(X_test_scaled, Y_test))

"""The RMSE SCORE is lower when the null values replaced by mean and also R2 score for training and testing data sets indicate that the data perfectly fits the linear regression model. hence the first linear regression model is a better fit.

## Evaluation Metrics when the null values are replaced by mean.

MAE: 91.39351431925819\
MSE: 8411.69338854378\
RMSE: 91.71528437803472\
R2 for train: 1.0\
R2 for test(cross validation): 0.9989725032836634


---------------------------------------------------------------------------
## Evaluation Metrics when the null values are replaced by median.

3006.9597038539555\
MAE: 652.4389550370421\
MSE: 729770.2210726149\
RMSE: 854.2658960023015\
R2 for train: 1.0\
R2 for test(cross validation): 0.9108578414361149

---------------------------------------------------------------------------

The RMSE SCORE is lower when the null values replaced by mean and also R-Squared for training and testing data sets indicate that the data perfectly fits the linear regression model. Hence the first linear regression model is a better fit.
"""

Y_pred = lm.predict(X_test_scaled)
print(Y_pred)

y_pred = pd.DataFrame( { "actual": Y_test, 
"predicted_prob": lm.predict( 
( X_test_scaled ) ) } ) 
y_pred