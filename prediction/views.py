from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImportantClassifiersForm
from sklearn.model_selection import train_test_split # Used to split the dataset effeciently
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.externals.six import StringIO
from sklearn.ensemble import RandomForestClassifier
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv
import os

# Create your views here.
def index(request):
    form = ImportantClassifiersForm(request.POST)
    template_name = 'ask_for_input.html'
    context = {
    'form':form
    }
    print(template_name)
    return render(request, template_name, context)

def show_result(request):
    print("inside show_result")
    template_name = 'show_result.html'
    result = request.POST.get('first_classifier')
    context = {
    'result':result
    }
    print(result)
    return render(request, template_name, context)

def show_table_of_database(request):
    print("inside show database")
    template_name = 'show_table_of_database.html'
    path_to_file = "/home/maninder/School/SE188/project/"

    county_df = pd.read_csv(path_to_file + "County.csv", header = [0])
    mapping_df = pd.read_csv(path_to_file +"Mapping.csv", header = [0])
    master_kickstarter_df = pd.read_csv(path_to_file + "MasterKickstarter.csv", header = [0])
    #print the county_df
    list(county_df.columns.values)
    list(mapping_df.columns.values)
    list(master_kickstarter_df.columns.values)
    #different statuses
    #   ['successful', 'failed', 'live', 'canceled', 'suspended']
    #Series - is one dimensional i think
    a = master_kickstarter_df.loc[master_kickstarter_df["status"] == "failed"]["goal"]
    b = master_kickstarter_df.loc[master_kickstarter_df["status"] == "failed"]["pledged"]
    c = a - b
    #c is a 'pandas.core.series.Series'from sklearn.model_selection import train_test_split
    c.mean()
    #get the dataframes of the of the datasets of different statuses
    a1 = master_kickstarter_df.loc[master_kickstarter_df["status"] == "successful"]
    b1 = master_kickstarter_df.loc[master_kickstarter_df["status"] == "failed"]
    c1 = master_kickstarter_df.loc[master_kickstarter_df["status"] == "live"]
    d1 = master_kickstarter_df.loc[master_kickstarter_df["status"] == "canceled"]
    e1 = master_kickstarter_df.loc[master_kickstarter_df["status"] == "suspended"]

    #seperate target variable from data
    #get all the columns of the master_kickstarter_df
    all_master_columns = master_kickstarter_df.columns.values
    #get the index of the target variable and data index's in their own variables
    target_index = all_master_columns.tolist().index("status")
    data_indexes = np.delete(all_master_columns, target_index, None)
    #get the value at target_index, then store it in target_index
    target_index = all_master_columns[target_index]
    #parse the target from master_kickstarter_df table
    target_df = master_kickstarter_df[target_index]
    #get all the other indexes other than target
    data_df = master_kickstarter_df[data_indexes]

    #have to do something about the columns with string sort_values and other problem values
    #<------------Temporary--------------->
    #get all the columns columns which are strings, for which we only need to look at one row
    test_row = data_df.loc[70302]
    #get the index of anything thats not an int or a float
    temp = []
    for i in range(test_row.size-1):
        if not(isinstance(test_row[i], int)) and not(isinstance(test_row[i], float)):
            print("Value type at index ", i, " is: ", type(test_row[i]))
            temp.append(i)
    #remove the non numeric value columns
    data_indexes = np.delete(data_indexes, temp, None)
    data_indexes[3]
    #also remove the 'id' column (too big numbers in it)
    data_indexes = np.delete(data_indexes, 3, None)
    #data without any string valued columns
    data_df = master_kickstarter_df[data_indexes]

    #----
    #replace all the "nan" and "inf" valeus from the columns
    data_df = data_df.fillna(0)
    #----

    #convert values from 64 types to 32 types
    test_row = data_df.loc[4313]
    temp1 = [] #for all the int64 columns
    temp2 = [] #for all the float64 columns
    for i in range(test_row.size-1):
        if (isinstance(test_row[i], np.int64)):
            temp1.append(i)

        if (isinstance(test_row[i], np.float64)):
            temp2.append(i)

    #get names of the columns in question
    int64_cols = data_indexes.copy()
    float64_cols = data_indexes.copy()
    #---
    int64_cols = np.delete(int64_cols, temp1, None)
    float64_cols = np.delete(float64_cols, temp2, None)
    #call the method that does that for both
    change_df_col_type(data_df, int64_cols, np.int32)
    change_df_col_type(data_df, float64_cols, np.float32)

    #<------------Temporary--------------->

    #Prediction TIME
    x_train, x_test, y_train, y_test = train_test_split(data_df, target_df, test_size=.30, random_state=0)
    dtc = tree.DecisionTreeClassifier(max_depth=None)

    x_train

    dtc.fit(x_train, y_train)

    print(dtc.score(x_train, y_train))
    y_predictions = dtc.predict(x_test)

    print('Accuracy for given train:test split 1 = ', accuracy_score(y_test, y_predictions))

    context = {
        'master_kickstarter_df':master_kickstarter_df,
    }
    return render(request, template_name, context)
