import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import numpy as np
import datetime
from sklearn.metrics import classification_report, accuracy_score
import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    try:
        file_name = sys.argv[1]
    except:
        file_name = 'dataset/jan2april_processed_trainingSet.csv'

    df = pd.read_csv(file_name)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    val = df['company']
    df['company'], id = pd.factorize(val)

    df['date'] = pd.to_datetime(df['date'])
    train = df[df['date'] < datetime.datetime(year=2017, month=4, day=15)]
    test = df[df['date'] >= datetime.datetime(year=2017, month=4, day=15)]

    test = test.sort_values('date')
    test.reset_index(drop=True, inplace=True)

    backtesting_df = test['target'].values
    # print(len(train), len(test))

    train = train.sample(frac=1)
    train.drop('date', axis=1, inplace=True)
    train.dropna(inplace=True)
    # train.drop('company', axis=1, inplace=True)
    train_y = (train['target'] > 0).astype(int)
    train_X = train.drop('target', axis=1)


    test = test.sample(frac=1)
    test.drop('date', axis=1, inplace=True)
    test.dropna(inplace=True)
    # test.drop('company', axis=1, inplace=True)
    test_y = (test['target'] > 0).astype(int)
    test_X = test.drop('target', axis=1)

    # model = LGBMClassifier(reg_lambda= 0, reg_alpha= 0.001, max_bin= 5000, n_estimators=500, num_leaves= 25)
    # model.fit(train_X.values,train_y.values)
    #
    # pred_proba_lgbm = model.predict_proba(test_X)
    # pred_proba_lgbm_train = model.predict_proba(train_X)
    # pred_lgbm = model.predict(test_X)
    # print(classification_report(pred_lgbm, test_y.values))
    # print(accuracy_score(pred_lgbm, test_y.values))
    #
    # model = XGBClassifier(objective='binary:logistic', subsample=0.5, max_depth=7, gamma=0.2, colsample_bytree=0.5,
    #                       min_child_weight=5, n_estimators=400)
    #
    # model.fit(train_X, train_y)
    # pred_proba_xgb = model.predict_proba(test_X)
    # pred_proba_xgb_train = model.predict_proba(train_X)
    # pred_xgb = model.predict(test_X)
    #
    #
    # print(classification_report(pred_xgb, test_y.values))
    # print(accuracy_score(pred_xgb, test_y.values))

    model = CatBoostClassifier()

    model.fit(train_X, train_y)
    pred_proba_cat = model.predict_proba(test_X)
    pred_proba_cat_train = model.predict_proba(train_X)
    pred_cat = model.predict(test_X)

    print(classification_report(pred_cat, test_y.values))
    print(accuracy_score(pred_cat, test_y.values))
    # stacked_train = np.swapaxes(np.vstack((pred_proba_lgbm_train[:, 1], pred_proba_xgb_train[:, 1], pred_proba_cat_train[:, 1],  np.swapaxes(train_X, 0, 1))), 0, 1)
    #
    # stacked_test = np.swapaxes(np.vstack((pred_proba_lgbm[:, 1], pred_proba_xgb[:, 1], pred_proba_cat[:, 1] , np.swapaxes(test_X, 0, 1))), 0, 1)
    #
    # # Stacked model
    # model = CatBoostClassifier()
    #
    # model.fit(stacked_train, train_y)
    # pred_stacked_cat = model.predict(stacked_test)
    # pred_stacked_cat_proba = model.predict_proba(stacked_test)
    # print(classification_report(pred_stacked_cat, test_y.values))
    # print(accuracy_score(pred_stacked_cat, test_y.values))
    #
    # boosted = (((pred_proba_lgbm[:, 1] + pred_proba_xgb[:, 1] + pred_proba_cat[:, 1] + pred_stacked_cat_proba[:, 1]) / 4) > .5).astype(int)
    # print(classification_report(boosted, test_y.values))
    # print(accuracy_score(boosted, test_y.values))


    # # this is a backtesting script
    # def exponential_average(old, new, beta=0.9):
    #     return old * beta + (1-beta) * new
    #
    backtest_values = []
    last_value = 100000

    for i in range(len(pred_cat)):
        if pred_cat[i] == 1:
            last_value += (100000 * backtesting_df[i])
        else:
            last_value -= (100000 * backtesting_df[i])

        backtest_values.append(last_value)

    plt.plot(backtest_values)
    plt.show()


