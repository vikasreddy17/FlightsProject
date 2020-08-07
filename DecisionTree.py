import pandas as pd
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeRegressor
import pdb
from tqdm import tqdm
import os

print('start')
am_rows=1000
output_train_x = pd.read_csv("output_data/output_train_x.csv")
output_train_y = pd.read_csv("output_data/output_train_y.csv")
output_train_y.loc[output_train_x.index, :]
assert(output_train_y.shape[0] == output_train_x.shape[0])

Decision_Tree_Full_Results = None
dictionary = {'max_leaf_nodes': [] , 'max_depth':[] , 'test_score': [], 'train_score': [], 'train_minus_test': []}
for leafnodes in tqdm(range(19,27)):
    for md in tqdm(range(3,20)):
    	if os.path.isfile('decision_tree_crossval/' + str(md) + str(leafnodes) + '.csv') == False:
            clf = tree.DecisionTreeRegressor(max_leaf_nodes=leafnodes, max_depth=md)
            scores = cross_validate(clf, output_train_x,output_train_y['ARRIVAL_DELAY'], cv=5, scoring='r2', return_train_score=True)
            dictionary['max_leaf_nodes'].append(leafnodes)
            dictionary['max_depth'].append(md)
            dictionary['test_score'].append(scores['test_score'].mean())
            dictionary['train_score'].append(scores['train_score'].mean())
            dictionary['train_minus_test'].append((scores['train_score'].mean()) - (scores['test_score'].mean()))
            Decision_Tree_Results = pd.DataFrame(dictionary)
            Decision_Tree_Results.to_csv('decision_tree_crossval/' + str(md) + str(leafnodes) + '.csv', index=None)
    	else:
    		Decision_Tree_Results = pd.read_csv('decision_tree_crossval/' + str(md) + str(leafnodes) + '.csv')
    	if Decision_Tree_Full_Results is None:
    		Decision_Tree_Full_Results = Decision_Tree_Results
    	else:
    		Decision_Tree_Full_Results = pd.concat([Decision_Tree_Full_Results, Decision_Tree_Results], axis=0)
Decision_Tree_Full_Results.to_csv('Decision_Tree_Full_Results.csv', index=None)
print('done')