import pandas as pd
from sklearn import tree
from sklearn.ensemble import AdaBoostRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_validate
from tqdm import tqdm
import os

print('start')
output_train_x = pd.read_csv("output_data/output_train_x.csv")
output_train_y = pd.read_csv("output_data/output_train_y.csv")
output_train_y.loc[output_train_x.index, :]
assert(output_train_y.shape[0] == output_train_x.shape[0])

AdaBoost_Full_Results = None
for n_estimators in tqdm(range(25,30)):
    for learning_rate in tqdm(range(88, 91)):
        for md in tqdm(range(3,5)):
            if os.path.isfile('AdaBoost_crossval/' + str(n_estimators) + str(md) + str(learning_rate) + 'Adaboost.csv') == False:
                clf = tree.DecisionTreeRegressor(max_depth=md)
                clf1 = AdaBoostRegressor(base_estimator=clf, n_estimators=n_estimators, learning_rate=(learning_rate/1000), random_state=0)
                scores = cross_validate(clf1, output_train_x,output_train_y['ARRIVAL_DELAY'], cv=5, scoring='r2', return_train_score=True)
                dictionary = {'n_estimators': [] , 'learning_rate':[], 'test_score': [], 'train_score': [], 'max_depth': [], 'fit_time': [], 'train_minus_test': []}
                dictionary['n_estimators'].append(n_estimators)
                dictionary['max_depth'].append(md)
                dictionary['learning_rate'].append(learning_rate/1000)
                dictionary['test_score'].append(scores['test_score'].mean())
                dictionary['train_score'].append(scores['train_score'].mean())
                dictionary['fit_time'].append(scores['fit_time'].mean())
                dictionary['train_minus_test'].append((scores['train_score'].mean()) - (scores['test_score'].mean()))
                AdaBoost_Results=pd.DataFrame(dictionary)
                AdaBoost_Results.to_csv('AdaBoost_crossval/' + str(n_estimators) + str(md) + str(learning_rate) + 'Adaboost.csv', index=None)
            else:
                AdaBoost_Results = pd.read_csv('AdaBoost_crossval/' + str(n_estimators) + str(md) + str(learning_rate) + 'Adaboost.csv')
            if AdaBoost_Full_Results is None:
                AdaBoost_Full_Results = AdaBoost_Results
            else:
                AdaBoost_Full_Results = pd.concat([AdaBoost_Full_Results, AdaBoost_Results], axis=0)
AdaBoost_Full_Results.sort_values(by=['test_score'], inplace=True, ascending=False)
AdaBoost_Full_Results = AdaBoost_Full_Results.round(3)
AdaBoost_Full_Results.to_csv('AdaBoost_full_crossval_results.csv', index=None)
print('done')