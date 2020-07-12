import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import datasets
from sklearn import svm
flightsdata = pd.read_csv("input_data_df.csv", nrows=10)
cont_flightsdata = flightsdata['SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY’]
target_flightsdata = flightsdata['ARRIVAL_DELAY']



dictionary = {'kernelname': [] , 'cvalue':[] , 'recallval': []}
for ker in ['rbf', 'poly', 'linear']:
    for val in range(5,20):
        clf = svm.SVC(kernel=ker, C=(val/1000))
        scores = cross_val_score(clf, x_train, y_train, cv=5, 
                         scoring='recall_macro')
        dictionary['kernelname'].append(ker)
        dictionary['cvalue'].append(val/1000)
        dictionary['recallval'].append(scores.mean())
new_dataframe=pd.DataFrame(dictionary)
print(new_dataframe)