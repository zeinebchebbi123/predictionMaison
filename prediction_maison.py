# -*- coding: utf-8 -*-
"""prediction.maison.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RHw_i9sjzPwlI8JKsLWTl7XycCXKPGqt
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import pandas as pd
from google.colab import drive
drive.mount('/content/drive')

# Remplacez par le chemin correct des fichiers
sample_submission = pd.read_csv('/content/drive/My Drive/sample_submission.csv')
test = pd.read_csv('/content/drive/My Drive/test.csv')
train = pd.read_csv('/content/drive/My Drive/train.csv')


# Créer des copies
test_copy = test.copy()
train_copy = train.copy()

# Aperçu des données
print(train.head())
print(test.head())

test_copy.head()

train_copy.head()

len(train_copy.columns)
train_copy['train']  = 1
test_copy['train']  = 0
data_full = pd.concat([train_copy, test_copy], axis=0,sort=False)
data_full.describe()

data_full.info()

df_NULL = [(c, data_full[c].isna().mean()*100) for c in data_full]
df_NULL = pd.DataFrame(df_NULL, columns=["Colonne", "Taux de NULL"])
df_NULL.sort_values("Taux de NULL", ascending=False)

from matplotlib import pyplot as plt
_df_1['Taux de NULL'].plot(kind='line', figsize=(8, 4), title='Taux de NULL')
plt.gca().spines[['top', 'right']].set_visible(False)

from matplotlib import pyplot as plt
_df_0['Taux de NULL'].plot(kind='hist', bins=20, title='Taux de NULL')
plt.gca().spines[['top', 'right',]].set_visible(False)

# Variables avec plus de 50% de NULL
df_NULL = df_NULL[df_NULL["Taux de NULL"] > 80]
df_NULL.sort_values("Taux de NULL", ascending=False)

categorical_features = data_full.select_dtypes(include=['object'])
numerical_features = data_full.select_dtypes(exclude=['object'])
# Variables numériques :
print("Nombre de variables numériques :",numerical_features.shape[1])
print("\nNombre de valeurs nulles :\n",numerical_features.isnull().sum())

# Variables catégoriques :
print("Nombre de variables numériques :",categorical_features.shape[1])
print("\nNombre de valeurs nulles :\n",categorical_features.isnull().sum())

fill_None = ['BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2','GarageType','GarageFinish','GarageQual','FireplaceQu','GarageCond']
categorical_features[fill_None]= categorical_features[fill_None].fillna('None')

fill_other = ['MSZoning','Utilities','Exterior1st','Exterior2nd','MasVnrType','Electrical','KitchenQual','Functional','SaleType']
categorical_features[fill_other] = categorical_features[fill_other].fillna(categorical_features.mode().iloc[0])

categorical_features.info()

print("Médiane GarageYrBlt :",numerical_features['GarageYrBlt'].median())
print("LotFrontage :",numerical_features["LotFrontage"].median())

numerical_features['GarageYrBlt'] = numerical_features['GarageYrBlt'].fillna(numerical_features['GarageYrBlt'].median())
numerical_features['LotFrontage'] = numerical_features['LotFrontage'].fillna(numerical_features['LotFrontage'].median())

numerical_features = numerical_features.fillna(0)
numerical_features.info()

for col in categorical_features.columns:
    #Conversion du type de variable en variable catégorique
    categorical_features[col] = categorical_features[col].astype('category')
    categorical_features[col] = categorical_features[col].cat.codes
categorical_features.head()

df_final = pd.concat([numerical_features,categorical_features], axis=1,sort=False)
final_train = df_final[df_final['train'] == 1]
final_train = final_train.drop(['train',],axis=1)

final_test = df_final[df_final['train'] == 0]
final_test = final_test.drop(['SalePrice'],axis=1)
final_test = final_test.drop(['train',],axis=1)

final_train = final_train.drop(["Id"],axis=1)

corr_train = final_train.corr()

# Mask for the upper triangle
mask = np.triu(np.ones_like(corr_train, dtype=bool))

# Creating the heatmap with the chosen color scheme
fig, ax = plt.subplots(figsize=(20, 20))
sns.heatmap(
    corr_train,
    mask=mask,
    cmap="RdPu",  # Vibrant Red-Purple color scheme
    vmax=1,
    center=0,
    square=True,
    linewidths=.5,
    cbar_kws={"shrink": .5}
)
ax.set_title("Matrice des corrélations du jeu de données Train", fontsize=22)
plt.show()

nocorr_features = list(corr_train[corr_train['SalePrice']<0.2].index)
nocorr_features

final_train = final_train.drop(nocorr_features, axis=1)
final_train.head()

rl_features = list(corr_train[corr_train['SalePrice']>0.3].index)
rl_features.remove("SalePrice")
rl_features

Y_train = final_train["SalePrice"]
X_train = final_train.drop(["SalePrice"],axis=1)
X_train = X_train[rl_features]

from sklearn.model_selection import train_test_split
X_train_rl, X_test_rl, y_train_rl, y_test_rl = train_test_split(X_train, Y_train, test_size=0.3, random_state=1)

y_train_rl = y_train_rl.values.reshape(-1,1)
y_test_rl = y_test_rl.values.reshape(-1,1)

#STANDADISATION DES DONNEES
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_rl = sc.fit_transform(X_train_rl)
X_test_rl = sc.fit_transform(X_test_rl)
y_train_rl = sc.fit_transform(y_train_rl)
y_test_rl = sc.fit_transform(y_test_rl)

#regression lineaire
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train_rl,y_train_rl)

print("Intercept :",lm.intercept_)
print("Coefficients :",lm.coef_)
print("R² du modèle :",round(lm.score(X_train_rl,y_train_rl),2))

pred_rl = lm.predict(X_test_rl)
pred_rl = pred_rl.reshape(-1,1)

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(1, 1, 1)
ax.scatter(y_test_rl, pred_rl)
ax.plot([y_test_rl.min(), y_test_rl.max()], [y_test_rl.min(), y_test_rl.max()], color='r')
ax.set(xlabel='y_test', ylabel='y_pred')
plt.title("Projection des prédictions en fonction des valeurs réelles", fontsize=20)
plt.show()

#Fonction de calculs des metriques importantes MAE, MSE, MAPE, RMSE
def metrics_timeseries(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    diff = y_true - y_pred
    mae = np.mean(abs(diff))
    mse = np.mean(diff**2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs(diff / y_true)) * 100
    dict_metrics = {"Métrique":["MAE", "MSE", "RMSE", "MAPE"], "Résultats":[mae, mse, rmse, mape]}
    df_metrics = pd.DataFrame(dict_metrics)
    return df_metrics

metrics_rl = metrics_timeseries(y_test_rl, pred_rl)
metrics_rl

Y_rf = final_train["SalePrice"]
X_rf = final_train.drop(["SalePrice"],axis=1)

from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestRegressor
selector = RFECV(RandomForestRegressor(), min_features_to_select=5, step=1, cv=5)
selector.fit(X_rf,Y_rf)



from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestRegressor

# Create and fit the selector
selector = RFECV(RandomForestRegressor(), min_features_to_select=5, step=1, cv=5)
selector.fit(X_rf, Y_rf)

# Access cross-validation scores
grid_scores = selector.cv_results_['mean_test_score']

# Print the scores
print("Mean cross-validation scores for each feature subset:")
print(grid_scores)

# Access selected features
selected_features = X_rf.columns[selector.support_]
print("Selected features:")
print(selected_features)

selector.cv_results_['mean_test_score']

selector.ranking_

best_features_rf = list(np.array(X_rf.columns)[selector.support_])
best_features_rf

X_rf = X_rf[best_features_rf]

X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(X_rf, Y_rf, test_size=0.3, random_state=1)
y_train_rf = y_train_rf.values.reshape(-1,1)
y_test_rf = y_test_rf.values.reshape(-1,1)

from sklearn.model_selection import GridSearchCV
warnings.filterwarnings('ignore')

param_grid_rf = { 'n_estimators' : [10,50,100,150,200], 'max_features' : ['auto', 'sqrt']}
grid_search_rf = GridSearchCV(RandomForestRegressor(), param_grid_rf, cv=5)
grid_search_rf.fit(X_train_rf, y_train_rf)

print ("Score final : ", round(grid_search_rf.score(X_train_rf, y_train_rf) *100,4), " %")
print ("Meilleurs parametres: ", grid_search_rf.best_params_)
print ("Meilleure config: ", grid_search_rf.best_estimator_)

rf =  RandomForestRegressor(max_features='sqrt', n_estimators=150)
rf.fit(X_train_rf, y_train_rf)

pred_rf = rf.predict(X_test_rf)
pred_rf = pred_rf.reshape(-1,1)

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(1, 1, 1)
ax.scatter(y_test_rf, pred_rf)
ax.plot([y_test_rf.min(), y_test_rf.max()], [y_test_rf.min(), y_test_rf.max()], color='r')
ax.set(xlabel='y_test', ylabel='y_pred')
plt.title("Projection des prédictions en fonction des valeurs réelles", fontsize=20)
plt.show()

metrics_rf = metrics_timeseries(y_test_rf, pred_rf)
metrics_rf

id_test = final_test["Id"]
X_pred_test = final_test[best_features_rf]

pred_rf = rf.predict(X_pred_test)
pred_rf = pred_rf.reshape(-1,1)
pred_rf

df_submission = pd.concat([id_test,pd.Series(pred_rf[:,0])],axis=1).rename(columns={0:"SalePrice"})
df_submission

df_submission.to_csv('submission.csv', index=False)