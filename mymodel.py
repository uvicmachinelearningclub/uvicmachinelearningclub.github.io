""" A Simple Random Forest Implimentaiton
Author : Brock Moir
Date : 15 July 2014
"""
import csv as csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

# I want a function that will tell me if a column has empty rows
def rows_are_empty(data, column):
  empty_rows = data[::,column] == ''
  if np.size(data[empty_rows,column])<1: return False
  else: return True

# Load our training and testing sets into NumPy arrays 
# First the training set
csv_train_file_object = csv.reader(open('train.csv', 'rb'))
train_header = csv_train_file_object.next()
train_data=[]

for row in csv_train_file_object:
    train_data.append(row[0:]) 
train_data = np.array(train_data) 

# Then the test set
csv_test_file_object = csv.reader(open('test.csv', 'rb')) 
test_header = csv_test_file_object.next() 
test_data=[]

for row in csv_test_file_object:
    test_data.append(row[0:])
test_data = np.array(test_data) 

# I want to build a random forest that uses Pclass, Sex, Age, SibSp, ParCh, and Fare
# In the traing set these are columns 2, 4, 5, 6, 7, 9
# In the testing set these are the same as the training columns minus one
# I will process both sets here

my_columns = np.array([2, 4, 5, 6, 7, 9])

train_data[::,4] = (train_data[::,4] == "female").astype(int)
test_data[::,3] = (test_data[::,3] == "female").astype(int)

# If there are missing values in any of these columns I will just fill them with the mean
# I wrote this up quick, so don't expect anything too fancy

for column in my_columns:
  if rows_are_empty(train_data, column):
    non_empty_rows = train_data[::,column] != '' # empty rows are read as an empty string
    empty_rows = train_data[::,column] == ''
    train_data[empty_rows, column] = np.mean(train_data[non_empty_rows, column].astype(float))
  if rows_are_empty(test_data, column-1):
    non_empty_rows = test_data[::,column-1] != ''
    empty_rows = test_data[::,column-1] == ''
    test_data[empty_rows, column-1] = np.mean(test_data[non_empty_rows, column-1].astype(float))

# For the purposes of testing your work without having to submit it is helpful to split up the training set.
# We can use the larger part to train our model, and the smaller part to determine our model's effectiveness.
# I will use 20% of the training set to cross-validate

X_train, X_xvalid, Y_train, Y_xvalid = cross_validation.train_test_split(train_data[::,my_columns].astype(float), train_data[::,1].astype(int), test_size=0.2, random_state=0)

print 'Training...'
# Here I create the random forest object, note that all these values are the defaults
# There can probably be some big improvements by fiddling with these values
# Check out the documentation at: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
forest = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features='auto', max_leaf_nodes=None, bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0, min_density=None, compute_importances=None)

forest = forest.fit( X_train, Y_train)                      # Training the forest
print 'Model score = %s' % forest.score(X_xvalid, Y_xvalid) # This most likely won't be the same as the submission score


print 'Predicting...'
output = forest.predict(test_data[::, my_columns-1].astype(float)).astype(int) # Produce a prediction

# The submission has a particular format, I write out a .csv file here

predictions_file = open("mymodel.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(test_data[::,0], output))
predictions_file.close()
print 'Done.'

