# importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("weatherAUS.csv")
df.head()

df.shape

df.info()

numerical_feature = [feature for feature in df.columns if df[feature].dtypes != 'O']
discrete_feature=[feature for feature in numerical_feature if len(df[feature].unique())<70]
continuous_feature = [feature for feature in numerical_feature if feature not in discrete_feature]
categorical_feature = [feature for feature in df.columns if feature not in numerical_feature]
print("Numerical Features Count {}".format(len(numerical_feature)))
print("Discrete feature Count {}".format(len(discrete_feature)))
print("Continuous feature Count {}".format(len(continuous_feature)))
print("Categorical feature Count {}".format(len(categorical_feature)))

"""### Exploring Locations"""

len(df['Location'].unique())

df['Location'].unique()

"""### Filtering Locations"""

filtered_locations = ['Adelaide', 'GoldCoast']
df = df[df['Location'].isin(filtered_locations)]

"""### Splitting the dataset location wise

"""

locations = df['Location'].unique()
dfs = {}
for location in locations:
    location_df = df[df['Location'] == location].copy()
    df_name = location + "_df"
    dfs[df_name] = location_df


for location, location_df in dfs.items():
    globals()[location] = location_df

"""#### Identifying columns with high % of missing values"""

city_dfs = ['Adelaide_df', 'GoldCoast_df']

col_names = df.columns

null_dict = {}

for city in city_dfs:
    df_city = globals()[city]
    null_ = (df_city[col_names].isnull().mean() * 100).round(2)
    null_dict[city] = null_

null_table = pd.DataFrame(null_dict)
print(null_table.T)

drop_columns = ['Sunshine', 'Evaporation', 'Cloud3pm', 'Cloud9am']

for city in city_dfs:
    df = globals()[city]
    df.drop(columns=drop_columns, inplace=True)

numerical_feature = [feature for feature in df.columns if df[feature].dtypes != 'O']
discrete_feature=[feature for feature in numerical_feature if len(df[feature].unique())<50]
continuous_feature = [feature for feature in numerical_feature if feature not in discrete_feature]
categorical_feature = [feature for feature in df.columns if feature not in numerical_feature]
print("Numerical Features Count {}".format(len(numerical_feature)))
print("Discrete feature Count {}".format(len(discrete_feature)))
print("Continuous feature Count {}".format(len(continuous_feature)))
print("Categorical feature Count {}".format(len(categorical_feature)))

"""### Data Cleaning

#### 1. Adelaide
"""

Adelaide_df.head()

Adelaide_df.isnull().sum()*100/len(Adelaide_df)

"""#### Continuous features"""

num_rows = 4
num_cols = 3

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 15))
axes = axes.flatten()

for i, feature in enumerate(continuous_feature):
    sns.distplot(Adelaide_df[feature], ax=axes[i])
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("Count")
    axes[i].set_title(feature)

if len(continuous_feature) < num_rows * num_cols:
    for j in range(len(continuous_feature), num_rows * num_cols):
        fig.delaxes(axes[j])

fig.tight_layout()
plt.show()

for var in continuous_feature:
            if Adelaide_df[var].isnull().sum()*100/len(df) > 0:
                   Adelaide_df[var].fillna(df[var].median(), inplace=True)

"""#### Discrete features"""

for var in discrete_feature:
    Adelaide_df[var].fillna(Adelaide_df[var].mode().iloc[0], inplace=True)

"""#### Categorical features"""

for var in categorical_feature:
    Adelaide_df[var].fillna(Adelaide_df[var].mode().iloc[0], inplace=True)

Adelaide_df.isnull().sum()*100/len(Adelaide_df)

Adelaide_df.describe().T

"""### Outlier Handling"""

num_cols = 4
num_rows = 3

plt.figure(figsize=(20, 20))
for i, feature in enumerate(continuous_feature):
    plt.subplot(num_rows, num_cols, i+1)
    sns.boxplot(data=Adelaide_df, y=feature)
    plt.title(feature)

plt.tight_layout()
plt.show()

variables = continuous_feature.copy()
if 'Rainfall' in variables:
    variables.remove('Rainfall')

for variable in variables:
    IQR = Adelaide_df[variable].quantile(0.75) - Adelaide_df[variable].quantile(0.25)
    lower_bridge = Adelaide_df[variable].quantile(0.25) - (IQR * 1.5)
    upper_bridge = Adelaide_df[variable].quantile(0.75) + (IQR * 1.5)

    Adelaide_df = Adelaide_df[(Adelaide_df[variable] >= lower_bridge) & (Adelaide_df[variable] <= upper_bridge)]

num_cols = 4
num_rows = 3

plt.figure(figsize=(20, 20))
for i, feature in enumerate(continuous_feature):
    plt.subplot(num_rows, num_cols, i+1)
    sns.boxplot(data=Adelaide_df, y=feature)
    plt.title(feature)

plt.tight_layout()
plt.show()

sns.boxplot(data=Adelaide_df, y='Rainfall', showfliers=False, color='skyblue')
plt.xlabel('Rainfall')
plt.ylabel('Value')
plt.title('Distribution of Rainfall')

plt.tight_layout()
plt.show()

pct_5 = np.percentile(Adelaide_df['Rainfall'], 5)
pct_95 = np.percentile(Adelaide_df['Rainfall'], 95)

print(pct_5, pct_95)

Adelaide_df['Rainfall'] = np.where(Adelaide_df['Rainfall'] > pct_95, pct_95,np.where(Adelaide_df['Rainfall'] < pct_5, pct_5, Adelaide_df['Rainfall']))

plt.figure(figsize=(8, 6))
sns.boxplot(data=Adelaide_df, y='Rainfall')
plt.title('Boxplot of Rainfall')
plt.xlabel('Rainfall')
plt.show()

"""### Feature Engineering"""

Adelaide_df["RainToday"] = pd.get_dummies(Adelaide_df["RainToday"], drop_first = True)
Adelaide_df["RainTomorrow"] = pd.get_dummies(Adelaide_df["RainTomorrow"], drop_first = True)

for feature in categorical_feature:
    print(feature, (Adelaide_df.groupby([feature])["RainTomorrow"].mean().sort_values(ascending = False)).index)

windgustdir = {'NNW':0, 'NW':1, 'WNW':2, 'N':3, 'W':4, 'WSW':5, 'NNE':6, 'S':7, 'SSW':8, 'SW':9, 'SSE':10,
       'NE':11, 'SE':12, 'ESE':13, 'ENE':14, 'E':15}
winddir9am = {'NNW':0, 'N':1, 'NW':2, 'NNE':3, 'WNW':4, 'W':5, 'WSW':6, 'SW':7, 'SSW':8, 'NE':9, 'S':10,
       'SSE':11, 'ENE':12, 'SE':13, 'ESE':14, 'E':15}
winddir3pm = {'NW':0, 'NNW':1, 'N':2, 'WNW':3, 'W':4, 'NNE':5, 'WSW':6, 'SSW':7, 'S':8, 'SW':9, 'SE':10,
       'NE':11, 'SSE':12, 'ENE':13, 'E':14, 'ESE':15}
Adelaide_df["WindGustDir"] = Adelaide_df["WindGustDir"].map(windgustdir)
Adelaide_df["WindDir9am"] = Adelaide_df["WindDir9am"].map(winddir9am)
Adelaide_df["WindDir3pm"] = Adelaide_df["WindDir3pm"].map(winddir3pm)

corrmat = Adelaide_df.corr()
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(corrmat,annot=True)

"""# GoldCoast"""

GoldCoast_df.head()

GoldCoast_df.isnull().sum()*100/len(GoldCoast_df)

"""#### Continuous features"""

num_rows = 4
num_cols = 3

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 15))
axes = axes.flatten()

for i, feature in enumerate(continuous_feature):
    sns.distplot(GoldCoast_df[feature], ax=axes[i])
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("Count")
    axes[i].set_title(feature)

if len(continuous_feature) < num_rows * num_cols:
    for j in range(len(continuous_feature), num_rows * num_cols):
        fig.delaxes(axes[j])

fig.tight_layout()
plt.show()

for var in continuous_feature:
            if GoldCoast_df[var].isnull().sum()*100/len(df) > 0:
                   GoldCoast_df[var].fillna(df[var].median(), inplace=True)

"""#### Categorical features"""

for var in categorical_feature:
    GoldCoast_df[var].fillna(GoldCoast_df[var].mode().iloc[0], inplace=True)

"""#### Discrete features"""

for var in discrete_feature:
    GoldCoast_df[var].fillna(GoldCoast_df[var].mode().iloc[0], inplace=True)

GoldCoast_df.isnull().sum()*100/len(GoldCoast_df)

GoldCoast_df.describe().T

"""#### Outlier Handling"""

num_cols = 4
num_rows = 3

plt.figure(figsize=(20, 20))
for i, feature in enumerate(continuous_feature):
    plt.subplot(num_rows, num_cols, i+1)
    sns.boxplot(data=GoldCoast_df, y=feature)
    plt.title(feature)

plt.tight_layout()
plt.show()

variables = continuous_feature.copy()
if 'Rainfall' in variables:
    variables.remove('Rainfall')

for variable in variables:
    IQR = GoldCoast_df[variable].quantile(0.75) - GoldCoast_df[variable].quantile(0.25)
    lower_bridge = GoldCoast_df[variable].quantile(0.25) - (IQR * 1.5)
    upper_bridge = GoldCoast_df[variable].quantile(0.75) + (IQR * 1.5)

    GoldCoast_df =GoldCoast_df[(GoldCoast_df[variable] >= lower_bridge) & (GoldCoast_df[variable] <= upper_bridge)]

sns.boxplot(data=GoldCoast_df, y='Rainfall', showfliers=True, color='skyblue')
plt.xlabel('Rainfall')
plt.ylabel('Value')
plt.title('Distribution of Rainfall')

plt.tight_layout()
plt.show()

num_cols = 4
num_rows = 3

plt.figure(figsize=(20, 20))
for i, feature in enumerate(continuous_feature):
    plt.subplot(num_rows, num_cols, i+1)
    sns.boxplot(data=GoldCoast_df, y=feature)
    plt.title(feature)

plt.tight_layout()
plt.show()

pct_5 = np.percentile(GoldCoast_df['Rainfall'], 5)
pct_95 = np.percentile(GoldCoast_df['Rainfall'], 95)
print(pct_5, pct_95)

GoldCoast_df['Rainfall'] = np.where(GoldCoast_df['Rainfall'] > pct_95, pct_95,np.where(GoldCoast_df['Rainfall'] < pct_5, pct_5, GoldCoast_df['Rainfall']))

sns.boxplot(data=GoldCoast_df, y='Rainfall', showfliers=True, color='skyblue')
plt.xlabel('Rainfall')
plt.ylabel('Value')
plt.title('Distribution of Rainfall')

plt.tight_layout()
plt.show()

"""### Feature Engineering"""

GoldCoast_df["RainToday"] = pd.get_dummies(GoldCoast_df["RainToday"], drop_first = True)
GoldCoast_df["RainTomorrow"] = pd.get_dummies(GoldCoast_df["RainTomorrow"], drop_first = True)

for feature in categorical_feature:
    print(feature, (GoldCoast_df.groupby([feature])["RainTomorrow"].mean().sort_values(ascending = False)).index)

windgustdir = {'NNW':0, 'NW':1, 'WNW':2, 'N':3, 'W':4, 'WSW':5, 'NNE':6, 'S':7, 'SSW':8, 'SW':9, 'SSE':10,
       'NE':11, 'SE':12, 'ESE':13, 'ENE':14, 'E':15}
winddir3pm = {'NW':0, 'NNW':1, 'N':2, 'WNW':3, 'W':4, 'NNE':5, 'WSW':6, 'SSW':7, 'S':8, 'SW':9, 'SE':10,
       'NE':11, 'SSE':12, 'ENE':13, 'E':14, 'ESE':15}
GoldCoast_df["WindGustDir"] = GoldCoast_df["WindGustDir"].map(windgustdir)
GoldCoast_df["WindDir3pm"] = GoldCoast_df["WindDir3pm"].map(winddir3pm)

corrmat = GoldCoast_df.corr()
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(corrmat,annot=True)
