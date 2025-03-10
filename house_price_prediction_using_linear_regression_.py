# -*- coding: utf-8 -*-
"""House Price Prediction using Linear Regression .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tC4VVvCp2R1jig6uLNvv1Ia79mgIcJrP

[CLICK HERE TO DOWNLOAD DATASET](https://drive.google.com/drive/folders/1PcDhHnl4AbKQaqpjLDIV52gh1wI6St3D)

# **House Price Prediction Regression Model**

**Project Goal : **Predict the price of a house by its features. If you are a buyer or seller of the house but you don’t know the exact price of the house, so supervised machine learning regression algorithms can help you to predict the price of the house just providing features of the target house.
"""

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load dataset
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

print("Shape of train: ", train.shape)
print("Shape of test: ", test.shape)

train.head(10)

test.head(10)

## concat train and test
df = pd.concat((train, test))
# temp_df = df
print("Shape of df: ", df.shape)

df.head(6)

df.tail(6)

"""# Exploratory Data Analysis (EDA)"""

# To show the all columns
pd.set_option("display.max_columns", 2000)
pd.set_option("display.max_rows", 85)

df.head(6)

df.tail(6)

df.info()

df.describe()

df.select_dtypes(include=['int64', 'float64']).columns

df.select_dtypes(include=['object']).columns

# Set index as Id column
df = df.set_index("Id")

df.head(6)

# Show the null values using heatmap
plt.figure(figsize=(16,9))
sns.heatmap(df.isnull())

# Get the percentages of null value
null_percent = df.isnull().sum()/df.shape[0]*100
null_percent

# drop columns
df = df.drop(columns=col_for_drop)
df.shape

print(df.columns)

# find the unique value count
for i in df.columns:
    print(i + "\t" + str(len(df[i].unique())))

# find unique values of each column
for i in df.columns:
    print("Unique value of:>>> {} ({})\n{}\n".format(i, len(df[i].unique()), df[i].unique()))

# Describe the target
train["SalePrice"].describe()

# Plot the distplot of target
plt.figure(figsize=(10,8))
bar = sns.distplot(train["SalePrice"])
bar.legend(["Skewness: {:.2f}".format(train['SalePrice'].skew())])

# correlation heatmap
plt.figure(figsize=(25,25))
# Select only numerical features for correlation calculation
numerical_train = train.select_dtypes(include=['number'])
ax = sns.heatmap(numerical_train.corr(), cmap = "coolwarm", annot=True, linewidth=2)

# to fix the bug "first and last row cut in half of heatmap plot"
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

# correlation heatmap of higly correlated features with SalePrice
# Convert 'SalePrice' to numeric if it's not already
train['SalePrice'] = pd.to_numeric(train['SalePrice'], errors='coerce')
#Now calculate the correlation matrix on numerical features only:
hig_corr = train.select_dtypes(include=np.number).corr()
hig_corr_features = hig_corr.index[abs(hig_corr["SalePrice"]) >= 0.5]
hig_corr_features

plt.figure(figsize=(10,8))
ax = sns.heatmap(train[hig_corr_features].corr(), cmap = "coolwarm", annot=True, linewidth=3)
# to fix the bug "first and last row cut in half of heatmap plot"
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

plt.figure(figsize=(10,8))
ax = sns.heatmap(train[hig_corr_features].corr(), cmap = "coolwarm", annot=True, linewidth=3)
# to fix the bug "first and last row cut in half of heatmap plot"
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

# Plot regplot to get the nature of highly correlated data
plt.figure(figsize=(16,9))
for i in range(len(hig_corr_features)):
    if i <= 9:
        plt.subplot(3,4,i+1)
        plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
        sns.regplot(data=train, x = hig_corr_features[i], y = 'SalePrice')

"""# **Handling Missing Value**"""

missing_col = df.columns[df.isnull().any()]
missing_col

"""Handling missing value of Bsmt feature"""

bsmt_col = ['BsmtCond', 'BsmtExposure', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtFinType1',
       'BsmtFinType2', 'BsmtFullBath', 'BsmtHalfBath', 'BsmtQual', 'BsmtUnfSF', 'TotalBsmtSF']
bsmt_feat = df[bsmt_col]
bsmt_feat

bsmt_feat.info()

bsmt_feat.isnull().sum()

bsmt_feat = bsmt_feat[bsmt_feat.isnull().any(axis=1)]
bsmt_feat

bsmt_feat_all_nan = bsmt_feat[(bsmt_feat.isnull() | bsmt_feat.isin([0])).all(1)]
bsmt_feat_all_nan

bsmt_feat_all_nan.shape

qual = list(df.loc[:, df.dtypes == 'object'].columns.values)
qual

# Fillinf the mising value in bsmt features
for i in bsmt_col:
    if i in qual:
        bsmt_feat_all_nan[i] = bsmt_feat_all_nan[i].replace(np.nan, 'NA') # replace the NAN value by 'NA'
    else:
        bsmt_feat_all_nan[i] = bsmt_feat_all_nan[i].replace(np.nan, 0) # replace the NAN value inplace of 0

bsmt_feat.update(bsmt_feat_all_nan) # update bsmt_feat df by bsmt_feat_all_nan
df.update(bsmt_feat_all_nan) # update df by bsmt_feat_all_nan
"""
>>> df = pd.DataFrame({'A': [1, 2, 3],
...                    'B': [400, 500, 600]})
>>> new_df = pd.DataFrame({'B': [4, 5, 6],
...                        'C': [7, 8, 9]})
>>> df.update(new_df)
>>> df
   A  B
0  1  4
1  2  5
2  3  6
"""

bsmt_feat = bsmt_feat[bsmt_feat.isin([np.nan]).any(axis=1)]
bsmt_feat

bsmt_feat.shape

print(df['BsmtFinSF2'].max())
print(df['BsmtFinSF2'].min())

pd.cut(range(0,1526),5) # create a bucket

df_slice = df[(df['BsmtFinSF2'] >= 305) & (df['BsmtFinSF2'] <= 610)]
df_slice

bsmt_feat.at[333,'BsmtFinType2'] = df_slice['BsmtFinType2'].mode()[0] # replace NAN value of BsmtFinType2 by mode of buet ((305.0, 610.0)

bsmt_feat

bsmt_feat['BsmtExposure'] = bsmt_feat['BsmtExposure'].replace(np.nan, df[df['BsmtQual'] =='Gd']['BsmtExposure'].mode()[0])

bsmt_feat['BsmtCond'] = bsmt_feat['BsmtCond'].replace(np.nan, df['BsmtCond'].mode()[0])
bsmt_feat['BsmtQual'] = bsmt_feat['BsmtQual'].replace(np.nan, df['BsmtQual'].mode()[0])

df.update(bsmt_feat)

bsmt_feat.isnull().sum()

"""# Handling missing value of Garage feature"""

df.columns[df.isnull().any()]

garage_col = ['GarageArea', 'GarageCars', 'GarageCond', 'GarageFinish', 'GarageQual', 'GarageType', 'GarageYrBlt',]
garage_feat = df[garage_col]
garage_feat = garage_feat[garage_feat.isnull().any(axis=1)]
garage_feat

garage_feat.shape

garage_feat_all_nan = garage_feat[(garage_feat.isnull() | garage_feat.isin([0])).all(1)]
garage_feat_all_nan.shape

for i in garage_feat:
    if i in qual:
        garage_feat_all_nan[i] = garage_feat_all_nan[i].replace(np.nan, 'NA')
    else:
        garage_feat_all_nan[i] = garage_feat_all_nan[i].replace(np.nan, 0)

garage_feat.update(garage_feat_all_nan)
df.update(garage_feat_all_nan)

garage_feat = garage_feat[garage_feat.isnull().any(axis=1)]
garage_feat

for i in garage_col:
    garage_feat[i] = garage_feat[i].replace(np.nan, df[df['GarageType'] == 'Detchd'][i].mode()[0])

garage_feat.isnull().any()

df.update(garage_feat)

"""# Handling missing value of remaining feature"""

df.columns

df.columns[df.isnull().any()]

df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode()[0])
df['Exterior1st'] = df['Exterior1st'].fillna(df['Exterior1st'].mode()[0])
df['Exterior2nd'] = df['Exterior2nd'].fillna(df['Exterior2nd'].mode()[0])
df['Functional'] = df['Functional'].fillna(df['Functional'].mode()[0])
df['KitchenQual'] = df['KitchenQual'].fillna(df['KitchenQual'].mode()[0])
df['MSZoning'] = df['MSZoning'].fillna(df['MSZoning'].mode()[0])
df['SaleType'] = df['SaleType'].fillna(df['SaleType'].mode()[0])
df['Utilities'] = df['Utilities'].fillna(df['Utilities'].mode()[0])
# Check if 'MasVnrType' is in the DataFrame columns
if 'MasVnrType' in df.columns:
    df['MasVnrType'] = df['MasVnrType'].fillna(df['MasVnrType'].mode()[0])
else:
    print("Column 'MasVnrType' not found in DataFrame.")
    # Investigate why the column is missing and take appropriate action

df.columns[df.isnull().any()]

# Check if 'MasVnrType' is in the DataFrame columns
if 'MasVnrType' in df.columns:
    # Proceed with your code if the column exists
    unique_values = df[df['MasVnrArea'].isnull() == True]['MasVnrType'].unique()
    print(unique_values)
else:
    print("Column 'MasVnrType' not found in DataFrame.")
    # Investigate why the column is missing and take appropriate action,
    # such as checking if it was dropped or renamed earlier.

# df.loc[(df['MasVnrType'] == 'None') & (df['MasVnrArea'].isnull() == True), 'MasVnrArea'] = 0

df.isnull().sum()/df.shape[0] * 100

"""# Handling missing value of LotFrontage feature"""

import numpy as np

lotconfig = ['Corner', 'Inside', 'CulDSac', 'FR2', 'FR3']

for i in lotconfig:
    # Compute mean LotFrontage for the specific LotConfig
    mean_value = df.loc[df['LotConfig'] == i, 'LotFrontage'].mean()

    # Fill missing values with the computed mean
    df.loc[(df['LotFrontage'].isnull()) & (df['LotConfig'] == i), 'LotFrontage'] = mean_value

df.isnull().sum()

"""# Feature Transformation"""

df.columns

# converting columns in str which have categorical nature but in int64
feat_dtype_convert = ['MSSubClass', 'YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold']
for i in feat_dtype_convert:
    df[i] = df[i].astype(str)

df['MoSold'].unique() # MoSold = Month of sold

# conver in month abbrevation
import calendar
df['MoSold'] = df['MoSold'].apply(lambda x : calendar.month_abbr[x])

df['MoSold'].unique()

quan = list(df.loc[:, df.dtypes != 'object'].columns.values)

quan

len(quan)

obj_feat = list(df.loc[:, df.dtypes == 'object'].columns.values)
obj_feat

"""# Conver categorical code into order"""

from pandas.api.types import CategoricalDtype
df['BsmtCond'] = df['BsmtCond'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes

df['BsmtCond'].unique()

df['BsmtExposure'] = df['BsmtExposure'].astype(CategoricalDtype(categories=['NA', 'Mn', 'Av', 'Gd'], ordered = True)).cat.codes

df['BsmtExposure'].unique()

df['BsmtFinType1'] = df['BsmtFinType1'].astype(CategoricalDtype(categories=['NA', 'Unf', 'LwQ', 'Rec', 'BLQ','ALQ', 'GLQ'], ordered = True)).cat.codes
df['BsmtFinType2'] = df['BsmtFinType2'].astype(CategoricalDtype(categories=['NA', 'Unf', 'LwQ', 'Rec', 'BLQ','ALQ', 'GLQ'], ordered = True)).cat.codes
df['BsmtQual'] = df['BsmtQual'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['ExterQual'] = df['ExterQual'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['ExterCond'] = df['ExterCond'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['Functional'] = df['Functional'].astype(CategoricalDtype(categories=['Sal', 'Sev', 'Maj2', 'Maj1', 'Mod','Min2','Min1', 'Typ'], ordered = True)).cat.codes
df['GarageCond'] = df['GarageCond'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['GarageQual'] = df['GarageQual'].astype(CategoricalDtype(categories=['NA', 'Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['GarageFinish'] = df['GarageFinish'].astype(CategoricalDtype(categories=['NA', 'Unf', 'RFn', 'Fin'], ordered = True)).cat.codes
df['HeatingQC'] = df['HeatingQC'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['KitchenQual'] = df['KitchenQual'].astype(CategoricalDtype(categories=['Po', 'Fa', 'TA', 'Gd', 'Ex'], ordered = True)).cat.codes
df['PavedDrive'] = df['PavedDrive'].astype(CategoricalDtype(categories=['N', 'P', 'Y'], ordered = True)).cat.codes
df['Utilities'] = df['Utilities'].astype(CategoricalDtype(categories=['ELO', 'NASeWa', 'NASeWr', 'AllPub'], ordered = True)).cat.codes

df['Utilities'].unique()

"""# Show skewness of feature with distplot"""

skewed_features = ['1stFlrSF',
 '2ndFlrSF',
 '3SsnPorch',
 'BedroomAbvGr',
 'BsmtFinSF1',
 'BsmtFinSF2',
 'BsmtFullBath',
 'BsmtHalfBath',
 'BsmtUnfSF',
 'EnclosedPorch',
 'Fireplaces',
 'FullBath',
 'GarageArea',
 'GarageCars',
 'GrLivArea',
 'HalfBath',
 'KitchenAbvGr',
 'LotArea',
 'LotFrontage',
 'LowQualFinSF',
 'MasVnrArea',
 'MiscVal',
 'OpenPorchSF',
 'PoolArea',
 'ScreenPorch',
 'TotRmsAbvGrd',
 'TotalBsmtSF',
 'WoodDeckSF']

quan == skewed_features

plt.figure(figsize=(25,20))
for i in range(len(skewed_features)):
    if i <= 28:
        plt.subplot(7,4,i+1)
        plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
        ax = sns.distplot(df[skewed_features[i]])
        ax.legend(["Skewness: {:.2f}".format(df[skewed_features[i]].skew())], fontsize = 'xx-large')

df_back = df

# decrease the skewnwnes of the data
for i in skewed_features:
    df[i] = np.log(df[i] + 1)

plt.figure(figsize=(25,20))
for i in range(len(skewed_features)):
    if i <= 28:
        plt.subplot(7,4,i+1)
        plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
        ax = sns.distplot(df[skewed_features[i]])
        ax.legend(["Skewness: {:.2f}".format(df[skewed_features[i]].skew())], fontsize = 'xx-large')

SalePrice = np.log(train['SalePrice'] + 1)

# get object feature to conver in numeric using dummy variable
obj_feat = list(df.loc[:,df.dtypes == 'object'].columns.values)
len(obj_feat)

# dummy varaibale
dummy_drop = []
clean_df = df
for i in obj_feat:
    dummy_drop += [i + '_' + str(df[i].unique()[-1])]

df = pd.get_dummies(df, columns = obj_feat)
df = df.drop(dummy_drop, axis = 1)

df.shape

import seaborn as sns
import pandas as pd

# Drop non-numeric columns (pairplot only works with numeric data)
numeric_df = df.select_dtypes(include=['number'])

# Drop rows with missing values (optional but helps avoid errors)
numeric_df = numeric_df.dropna()

# Generate pairplot
sns.pairplot(numeric_df)

# scaling dataset with robust scaler
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()

# Select only numerical features for scaling
numerical_features = df.select_dtypes(include=['number']).columns
df_numerical = df[numerical_features]

# Fit and transform the scaler on numerical features only
scaler.fit(df_numerical)
df_scaled = scaler.transform(df_numerical)

# Replace the original numerical columns with scaled values in the original DataFrame
df[numerical_features] = df_scaled

"""# Machine Learning Model Building"""

train_len = len(train)

# Splitting the data
X_train = df[:train_len]  # First part for training
X_test = df[train_len:]   # Remaining part for testing
y_train = df['SalePrice']  # Extracting target variable

# Checking dimensions
print(X_train.shape)
print(X_test.shape)
print(len(y_train))

"""# Cross Validation"""

from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import make_scorer, r2_score

def test_model(model, X_train=X_train, y_train=y_train):
    cv = KFold(n_splits = 3, shuffle=True, random_state = 45)
    r2 = make_scorer(r2_score)
    r2_val_score = cross_val_score(model, X_train, y_train, cv=cv, scoring = r2)
    score = [r2_val_score.mean()]
    return score

"""# Linear Regression"""

df.dtypes

# import sklearn.linear_model as linear_model
# LR = linear_model.LinearRegression()
# test_model(LR)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 1️⃣ Fill missing values
df.fillna(df.median(), inplace=True)  # Fill numerical columns with median
df.fillna(df.mode().iloc[0], inplace=True)  # Fill categorical columns with mode

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)  # Drop Id column if present

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Independent variables
y = df['SalePrice']  # Target variable

# 4️⃣ Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Train the model
LR = LinearRegression()
LR.fit(X_train, y_train)

# 6️⃣ Check model performance
print("Model trained successfully!")
print("Train Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

import pandas as pd
import sklearn.linear_model as linear_model
from sklearn.model_selection import train_test_split

# 1️⃣ Handle missing values
df.fillna(df.median(), inplace=True)  # Median for numerical
df.fillna(df.mode().iloc[0], inplace=True)  # Mode for categorical

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Features
y = df['SalePrice']  # Target

# 4️⃣ Ensure correct train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Train Linear Regression model
LR = linear_model.LinearRegression()
LR.fit(X_train, y_train)

# 6️⃣ Predict and check the model
y_pred = LR.predict(X_test)

print("Model trained successfully! ✅")

# Cross validation
cross_validation = cross_val_score(estimator = LR, X = X_train, y = y_train, cv = 10)
print("Cross validation accuracy of LR model = ", cross_validation)
print("\nCross validation mean accuracy of LR model = ", cross_validation.mean())

import pandas as pd
import sklearn.linear_model as linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1️⃣ Handle missing values (avoid NaN errors)
df.fillna(df.median(), inplace=True)  # Median for numerical
df.fillna(df.mode().iloc[0], inplace=True)  # Mode for categorical

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Features
y = df['SalePrice']  # Target

# 4️⃣ Ensure correct train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Train Ridge Regression model
rdg = linear_model.Ridge(alpha=1.0)
rdg.fit(X_train, y_train)

# 6️⃣ Predict and calculate error
y_pred = rdg.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("Ridge Regression Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

import pandas as pd
import sklearn.linear_model as linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1️⃣ Handle missing values (avoid NaN errors)
df.fillna(df.median(), inplace=True)  # Median for numerical
df.fillna(df.mode().iloc[0], inplace=True)  # Mode for categorical

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Features
y = df['SalePrice']  # Target

# 4️⃣ Ensure correct train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Train Lasso Regression model
lasso = linear_model.Lasso(alpha=1e-4)
lasso.fit(X_train, y_train)

# 6️⃣ Predict and calculate error
y_pred = lasso.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("Lasso Regression Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

"""# Fitting Polynomial Regression to the dataset"""

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1️⃣ Handle missing values (avoid NaN errors)
df.fillna(df.median(), inplace=True)  # Median for numerical
df.fillna(df.mode().iloc[0], inplace=True)  # Mode for categorical

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Features
y = df['SalePrice']  # Target

# 4️⃣ Ensure correct train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Apply Polynomial Features
poly_reg = PolynomialFeatures(degree=2)
X_train_poly = poly_reg.fit_transform(X_train)
X_test_poly = poly_reg.transform(X_test)  # Use transform, not fit_transform

# 6️⃣ Train Polynomial Regression Model
lin_reg_2 = LinearRegression()
lin_reg_2.fit(X_train_poly, y_train)

# 7️⃣ Predict and calculate error
y_pred = lin_reg_2.predict(X_test_poly)
mse = mean_squared_error(y_test, y_pred)

print("Polynomial Regression Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

import pandas as pd
import sklearn.linear_model as linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 1️⃣ Handle missing values (avoid NaN errors)
df.fillna(df.median(), inplace=True)  # Median for numerical
df.fillna(df.mode().iloc[0], inplace=True)  # Mode for categorical

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Features
y = df['SalePrice']  # Target

# 4️⃣ Ensure correct train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Apply Polynomial Features
poly_reg = PolynomialFeatures(degree=2)
X_train_poly = poly_reg.fit_transform(X_train)
X_test_poly = poly_reg.transform(X_test)  # Use transform, not fit_transform

# 6️⃣ Train Linear Regression Model
lin_reg_2 = linear_model.LinearRegression()
lin_reg_2.fit(X_train_poly, y_train)

# 7️⃣ Predict and calculate error
y_pred = lin_reg_2.predict(X_test_poly)
mse = mean_squared_error(y_test, y_pred)

print("Polynomial Regression Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

"""# Support Vector Machine"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# 1️⃣ Handle missing values
df.fillna(df.median(), inplace=True)  # Fill numeric NaNs with median
df.fillna(df.mode().iloc[0], inplace=True)  # Fill categorical NaNs with mode

# 2️⃣ Drop unnecessary columns
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)

# 3️⃣ Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])  # Features
y = df['SalePrice']  # Target

# 4️⃣ Ensure correct train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# 5️⃣ Scale the data (SVR is sensitive to feature scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6️⃣ Train SVR Model
svr_reg = SVR(kernel='rbf')
svr_reg.fit(X_train_scaled, y_train)

# 7️⃣ Predict and calculate error
y_pred = svr_reg.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)

print("SVR Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

"""# Decision Tree Regressor"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Handle missing values
df.fillna(df.median(), inplace=True)

# Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])
y = df['SalePrice']

# Train-test split (Ensure consistency)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# Train the Decision Tree Regressor
dt_reg = DecisionTreeRegressor(random_state=21)
dt_reg.fit(X_train, y_train)

# Predict and calculate error
y_pred = dt_reg.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Decision Tree Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

"""**Random Forest Regressor**"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Handle missing values
df.fillna(df.median(), inplace=True)

# Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])
y = df['SalePrice']

# Train-test split (Ensure consistency)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# Train the Random Forest Regressor
rf_reg = RandomForestRegressor(n_estimators=1000, random_state=51)
rf_reg.fit(X_train, y_train)

# Predict and calculate error
y_pred = rf_reg.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Random Forest Model Trained Successfully! ✅")
print(f"Mean Squared Error: {mse:.4f}")

"""# Bagging & boosting"""

from sklearn.ensemble import BaggingRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Handle missing values
df.fillna(df.median(), inplace=True)

# Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])
y = df['SalePrice']

# Train-test split (Ensure consistency)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# Bagging Regressor
br_reg = BaggingRegressor(n_estimators=1000, random_state=51)
br_reg.fit(X_train, y_train)
y_pred_br = br_reg.predict(X_test)
mse_br = mean_squared_error(y_test, y_pred_br)

# Gradient Boosting Regressor
gbr_reg = GradientBoostingRegressor(n_estimators=1000, learning_rate=0.1, loss='squared_error', random_state=51)
# The loss parameter is updated to 'squared_error', which is the new default and a valid option.
gbr_reg.fit(X_train, y_train)
y_pred_gbr = gbr_reg.predict(X_test)
mse_gbr = mean_squared_error(y_test, y_pred_gbr)

print(f"Bagging Regressor MSE: {mse_br:.4f}")
print(f"Gradient Boosting Regressor MSE: {mse_gbr:.4f}")

from sklearn.ensemble import BaggingRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Handle missing values
df.fillna(df.median(), inplace=True)

# Define features (X) and target (y)
X = df.drop(columns=['SalePrice'])
y = df['SalePrice']

# Train-test split (Ensures consistency)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1460, shuffle=False)

# Function to test models
def test_model(model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{model.__class__.__name__} - MSE: {mse:.4f}, R² Score: {r2:.4f}")

# Bagging Regressor
br_reg = BaggingRegressor(n_estimators=1000, random_state=51)
test_model(br_reg)

# Gradient Boosting Regressor
# gbr_reg = GradientBoostingRegressor(n_estimators=1000, learning_rate=0.1, loss='ls', random_state=51)
# test_model(gbr_reg)
# Gradient Boosting Regressor with correct loss parameter
gbr_reg = GradientBoostingRegressor(n_estimators=1000, learning_rate=0.1, loss='squared_error', random_state=51)
test_model(gbr_reg)

"""# XGBoost"""

import xgboost
#xgb_reg=xgboost.XGBRegressor()
xgb_reg = xgboost.XGBRegressor(bbooster='gbtree', random_state=51)
test_model(xgb_reg)

"""# SVM Model Bulding"""

svr_reg.fit(X_train,y_train)
y_pred = np.exp(svr_reg.predict(X_test)).round(2)

y_pred

submit_test1 = pd.concat([test['Id'],pd.DataFrame(y_pred)], axis=1)
submit_test1.columns=['Id', 'SalePrice']

submit_test1

submit_test1.to_csv('sample_submission.csv', index=False )

"""# SVM Model Bulding Hyperparameter Tuning

**Hyperparameter Tuning**
"""

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

params = {
    'kernel': ['linear', 'rbf', 'sigmoid'],
    'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
    'C': [0.1, 1, 10, 100, 1000],
    'epsilon': [1, 0.2, 0.1, 0.01, 0.001, 0.0001]
}
rand_search = RandomizedSearchCV(svr_reg, param_distributions=params, n_jobs=-1, cv=11)
rand_search.fit(X_train, y_train)
rand_search.best_score_

svr_reg= SVR(C=100, cache_size=200, coef0=0.0, degree=3, epsilon=0.01, gamma=0.0001,
    kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
test_model(svr_reg)

svr_reg.fit(X_train,y_train)
y_pred = np.exp(svr_reg.predict(X_test)).round(2)

y_pred

submit_test3 = pd.concat([test['Id'],pd.DataFrame(y_pred)], axis=1)
submit_test3.columns=['Id', 'SalePrice']

submit_test3.to_csv('sample_submission.csv', index=False)
submit_test3

"""# XGBoost parameter tuning"""

import xgboost
from sklearn.model_selection import RandomizedSearchCV

xgb2_reg = xgboost.XGBRegressor()

params_xgb = {
    'max_depth': range(2, 20, 2),
    'n_estimators': range(99, 2001, 80),
    'learning_rate': [0.2, 0.1, 0.01, 0.05],
    'booster': ['gbtree'],
    'min_child_weight': range(1, 8, 1)
}

rand_search_xgb = RandomizedSearchCV(
    estimator=xgb2_reg,
    param_distributions=params_xgb,
    n_iter=100,
    n_jobs=-1,
    cv=11,
    verbose=11,
    random_state=51,
    return_train_score=True,
    scoring='neg_mean_absolute_error'
)

rand_search_xgb.fit(X_train, y_train)

rand_search_xgb.bestscore

rand_search_xgb.bestparams

xgb2_reg=xgboost.XGBRegressor(n_estimators= 899,
 mon_child_weight= 2,
 max_depth= 4,
 learning_rate= 0.05,
 booster= 'gbtree')

test_model(xgb2_reg)

xgb2_reg.fit(X_train,y_train)
y_pred_xgb_rs=xgb2_reg.predict(X_test)

np.exp(y_pred_xgb_rs).round(2)

y_pred_xgb_rs = np.exp(xgb2_reg.predict(X_test)).round(2)
xgb_rs_solution = pd.concat([test['Id'], pd.DataFrame(y_pred_xgb_rs)], axis=1)
xgb_rs_solution.columns=['Id', 'SalePrice']
xgb_rs_solution.to_csv('sample_submission.csv', index=False)

xgb_rs_solution

"""# Feature Engineering / Selection to improve accuracy"""

# correlation Barplot
plt.figure(figsize=(9,16))
corr_feat_series = pd.Series.sort_values(train.corrwith(train.SalePrice))
sns.barplot(x=corr_feat_series, y=corr_feat_series.index, orient='h')

df_back1 = df_back

df_back1.to_csv('df_for_feature_engineering.csv', index=False)

list(corr_feat_series.index)

"""# **House Prices: Advanced Regression Techniques**

# Feature Selection / Engineering
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df_for_feature_engineering.csv')
train = pd.read_csv('/content/train.csv')
test = pd.read_csv('/content/test.csv')
df

#df = df.set_index('Id')

"""# Drop feature"""

df = df.drop(['YrSold',
 'LowQualFinSF',
 'MiscVal',
 'BsmtHalfBath',
 'BsmtFinSF2',
 '3SsnPorch',
 'MoSold'],axis=1)

quan = list(df.loc[:,df.dtypes != 'object'].columns.values)
quan

skewd_feat = ['1stFlrSF',
 '2ndFlrSF',
 'BedroomAbvGr',
 'BsmtFinSF1',
 'BsmtFullBath',
 'BsmtUnfSF',
 'EnclosedPorch',
 'Fireplaces',
 'FullBath',
 'GarageArea',
 'GarageCars',
 'GrLivArea',
 'HalfBath',
 'KitchenAbvGr',
 'LotArea',
 'LotFrontage',
 'MasVnrArea',
 'OpenPorchSF',
 'PoolArea',
 'ScreenPorch',
 'TotRmsAbvGrd',
 'TotalBsmtSF',
 'WoodDeckSF']
#  '3SsnPorch',  'BsmtFinSF2',  'BsmtHalfBath',  'LowQualFinSF', 'MiscVal'

# Decrease the skewness of the data
for i in skewd_feat:
    df[i] = np.log(df[i] + 1)

SalePrice = np.log(train['SalePrice'] + 1)

"""# decrease the skewnwnes of the data"""

for i in skewed_features: df[i] = np.log(df[i] + 1)

df

obj_feat = list(df.loc[:, df.dtypes == 'object'].columns.values)
print(len(obj_feat))

obj_feat

# dummy varaibale
dummy_drop = []
for i in obj_feat:
    dummy_drop += [i + '_' + str(df[i].unique()[-1])]

df = pd.get_dummies(df, columns = obj_feat)
df = df.drop(dummy_drop, axis = 1)

df.shape

# scaling dataset with robust scaler
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
scaler.fit(df)
df = scaler.transform(df)

"""# Model Building"""

train_len = len(train)
X_train = df[:train_len]
X_test = df[train_len:]
y_train = SalePrice

print("Shape of X_train: ", len(X_train))
print("Shape of X_test: ", len(X_test))
print("Shape of y_train: ", len(y_train))

"""# Cross Validation"""

from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import make_scorer, r2_score

def test_model(model, X_train=X_train, y_train=y_train):
    cv = KFold(n_splits = 3, shuffle=True, random_state = 45)
    r2 = make_scorer(r2_score)
    r2_val_score = cross_val_score(model, X_train, y_train, cv=cv, scoring = r2)
    score = [r2_val_score.mean()]
    return score

# first cross validation with df with log second without log

"""# **Linear Model**"""

import sklearn.linear_model as linear_model
LR = linear_model.LinearRegression()
test_model(LR)

rdg = linear_model.Ridge()
test_model(rdg)

lasso = linear_model.Lasso(alpha=1e-4)
test_model(lasso)

"""# **Support vector machine**"""

from sklearn.svm import SVR
svr = SVR(kernel='rbf')
test_model(svr)

"""# **svm hyper parameter tuning**"""

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
params = {'kernel': ['rbf'],
         'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
         'C': [0.1, 1, 10, 100, 1000],
         'epsilon': [1, 0.2, 0.1, 0.01, 0.001, 0.0001]}
rand_search = RandomizedSearchCV(svr_reg, param_distributions=params, n_jobs=-1, cv=11)
rand_search.fit(X_train, y_train)
rand_search.best_score_

rand_search.best_estimator_

svr_reg1=SVR(C=10, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma=0.001,
    kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
test_model(svr_reg1)

svr_reg= SVR(C=100, cache_size=200, coef0=0.0, degree=3, epsilon=0.01, gamma=0.0001,
    kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
test_model(svr_reg)

"""# **XGBoost**"""

import xgboost
#xgb_reg=xgboost.XGBRegressor()
xgb_reg = xgboost.XGBRegressor(bbooster='gbtree', random_state=51)
test_model(xgb_reg)

xgb2_reg=xgboost.XGBRegressor(n_estimators= 899,
 mon_child_weight= 2,
 max_depth= 4,
 learning_rate= 0.05,
 booster= 'gbtree')

test_model(xgb2_reg)

xgb2_reg.fit(X_train,y_train)
y_pred = np.exp(xgb2_reg.predict(X_test)).round(2)
submit_test = pd.concat([test['Id'],pd.DataFrame(y_pred)], axis=1)
submit_test.columns=['Id', 'SalePrice']
submit_test.to_csv('sample_submission.csv', index=False)
submit_test

svr_reg.fit(X_train,y_train)
y_pred = np.exp(svr_reg.predict(X_test)).round(2)
submit_test = pd.concat([test['Id'],pd.DataFrame(y_pred)], axis=1)
submit_test.columns=['Id', 'SalePrice']
submit_test.to_csv('sample_submission.csv', index=False)
submit_test

"""# **Model Saving**"""

import pickle

pickle.dump(svr_reg, open('model_house_price_prediction.csv', 'wb'))
model_house_price_prediction = pickle.load(open('model_house_price_prediction.csv', 'rb'))
model_house_price_prediction.predict(X_test)

test_model(model_house_price_prediction)

"""SVM Accuracy = 90%"""