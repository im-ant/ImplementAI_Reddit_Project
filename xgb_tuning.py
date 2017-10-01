import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV   #Perforing grid search
import numpy as np

if __name__ == '__main__':
    train = pd.read_csv('train_modified.csv')
    train.drop('Unnamed: 0', axis=1, inplace=True)
    train.drop('date', axis=1, inplace=True)
    train.dropna(inplace=True)
    vals = train['company'].values
    train['company'], id = pd.factorize(vals)
    target = (train['target'] > 0).astype(int)


    train.drop('target', axis=1, inplace=True)

    param_search = {
        'num_leaves':[25, 50, 100, 250, 500],
        'n_estimators':[100, 200],
        'max_bin':[256, 5000, 20000],
        'reg_alpha': [0, 0.001],
        'reg_lambda': [0, 0.0001]
    }
    gsearch1 = GridSearchCV(estimator = LGBMClassifier(), param_grid = param_search, scoring='accuracy',n_jobs=-1, cv=5, verbose=5)
    gsearch1.fit(train.values,target.values)
    print('=============================================')
    print('=============================================')
    print('=============================================')
    print(gsearch1.best_params_, gsearch1.best_score_)
    print('=============================================')
    print('=============================================')
    print('=============================================')


    param_test1 = {
        'max_depth':[3, 4, 5, 6, 7],
        'min_child_weight':[3, 5, 7],
        'gamma': [i / 10.0 for i in range(0, 5, 2)],
        'subsample':[i / 10.0 for i in range(5, 10, 2)],
        'colsample_bytree':[i / 10.0 for i in range(5, 10, 2)],
        'objective': ['binary:logistic']
    }
    model = XGBClassifier()
    gsearch1 = GridSearchCV(estimator = XGBClassifier(), param_grid = param_test1, scoring='accuracy',n_jobs=-1, cv=5, verbose=1)

    gsearch1.fit(train,target)

    print('=============================================')
    print('=============================================')
    print('=============================================')
    print(gsearch1.best_params_, gsearch1.best_score_)
    print('=============================================')
    print('=============================================')
    print('=============================================')
