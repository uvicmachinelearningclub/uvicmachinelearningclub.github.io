""" Skeleton code for loading and creating submission file for Kaggle-Higgs challenge http://www.kaggle.com/c/higgs-boson
    Run as: python higgs_model.py
    By James D. Pearce; jdpearce@uvic.ca """


import csv
import numpy as np
import math
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split

#################### Helpful functions ########################

def AMS(y,p,w):
    
    """ Approximate Median Significance defined as:
        AMS = sqrt(
        2 { (s + b + b_r) log[1 + (s/(b+b_r))] - s}
        where b_r = 10, b = background, s = signal, log is natural logarithm """
    
    br = 10.0
    s = (y*p*w).sum()
    b = ((1-y)*p*w).sum()
    radicand = 2 *( (s+b+br) * math.log (1.0 + s/(b+br)) -s)
    if radicand < 0:
        print 'radicand is negative. Exiting'
        exit()
    else:
        return math.sqrt(radicand)

def rank(a):
    
    """ Ranking function for making submission files,
        ranking events allows one to easily make ROC curves."""
    
    a = 1-a
    temp = a.argsort()
    ranks = np.empty(len(a), int)
    ranks[temp] = np.arange(len(a))
    return ranks+1

def classify_as_sb(a):
    if a == 1:
        return 's'
    return 'b'

if __name__ == '__main__':
    
    #################### Model Parameters ########################
    
    """ These parameters are not necessarily optimized"""
    
    split_level = 0.5 # % of data to be used for testing
    signal_threshold = 0.5 # minimum probability for output to be considered 'signal'
    do_test = True # Test model with training data. This should be set to False when generation submission file.
    make_submission = False
    scale_data = True
    sub_filename = 'higgs_model_sub.csv'
    
    #################### Loading Data ########################
    
    """ Download training and test higgs data http://www.kaggle.com/c/higgs-boson/data and unzip.
        Data consists of 30 features, event ids, event weights (training set) and class labels (training set).
        Some features have values set to -999.0, these correspond to events where the give object that the
        feature derives from is missing.
        
        For a technical description of the features see http://cds.cern.ch/record/1632191/files/ATLAS-CONF-2013-108.pdf """
    
    # Load data with csv reader
    training_dataset = "training.csv" # path to training data set.
    print '... loading training data'
    
    # Data is given as comma separated values (csv) in a standard .txt file
    data = np.array( list(csv.reader(open(training_dataset,'rb'), delimiter = ',')) )
    
    """ Use scikit-learn imputer http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Imputer.html
        to remove "missing" data, i.e. -999.0. Here I replace with mean value for feature,
        but then subtract it in the next step.
        
        Normalize feature with z-score:
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.scale.html#sklearn.preprocessing.scale
        this centers the mean to zero and scales each feature such that it has unit variance.
        
        The features correspond to data[1:,1:-2] as first row is header
        and Columns 0, 30 and 31 (last two, i.e. -2) are event ids, event weights and class label respectively."""
    
    # if scale_data == True: center and scale data. Set missing values to 0.0
    X = np.array(data[1:,1:-2], float)# cast all values as float
    if scale_data:
        imputer = preprocessing.Imputer(missing_values=-999.0, strategy='mean', axis=0, verbose=0, copy=False)
        imputer.fit_transform(X)
        X_train = preprocessing.scale(np.array(X)) # note "missing" values i.e. -999.0, are now set to 0.
    else:
        X_train = X
    
    """ Now data is a matrix, where each row is a instance and each column is a feature.
        or in numpy: X_train.shape => (n_instances, n_features) """
    
    # Make class label and weight vectors
    y_train = np.array([int(row[-1] == 's') for row in data[1:]]) # Encode class labels as s = 1 and b = 0
    w_train = np.array([float(row[-2]) for row in data[1:]]) # Weight vector encodes importance of each event to AMS metric.
    
    """ For prototyping one may want to test the classifier by splitting up the training set.
        Here we simply split the data into a separate test and training set,
        but in general cross-validation is a much better way of testing a classifier. See
        http://scikit-learn.org/stable/modules/cross_validation.html#computing-cross-validated-metrics """
    
    if do_test: # Be careful! Final optimization of hyperparameters should be done with full training set or CV.
        X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(X_train, y_train, w_train, test_size=split_level, random_state=42)
        # weights need to be rescaled for AMS calculation
        w_test *= 1./split_level
        w_train *= 1./(1. - split_level)
    
    ###################### Make classifier ########################
    
    """ Define classifier here. Sklearn has many classifiers to choose from:
        http://scikit-learn.org/stable/supervised_learning.html#supervised-learning"""

    #It's trivial to swap in other sklearn classifiers here.
    clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, verbose=2, n_jobs=-1)
    print 'Classifier:', clf
    
    """ Train, i.e. 'fit', classifier on training set and make predictions for test set."""
    
    print '... training'
    clf.fit(X_train,y_train)
    if do_test:
        prob = clf.predict_proba(X_test).T[1] # Returns vector of probabilities of instance being signal
        y_pred = prob > signal_threshold # Returns vector of bools: True if above threshold, False otherwise
        
        # Calculate accuracy of classifier on test data by counting instances with correct label prediction
        print 'Accuracy: ', sum( 1.0 for i in range(len(y_test)) if y_test[i] == int(y_pred[i]) )/float(len(y_test))
        
        ####################### Evaluating AMS metric ########################
        
        """ Calculate AMS metric: https://www.kaggle.com/c/higgs-boson/details/evaluation
            Threshold should be tuned for optimal AMS, one may want to perform a grid search:
            http://en.wikipedia.org/wiki/Hyperparameter_optimization
            i.e. check 100 or so thresholds between 0 and 1 and take the one that gives the maximum AMS. """
        
        ams = AMS(y_test,y_pred,w_test)
        print 'AMS: ', ams
    
    ####################### Make submission file ########################
    
    """ If bool is set classifier will run over test data and make a submission file for the kaggle competition.
        
        If training data is scaled, imputed or transformed in anyway the test data must also be transformed in an
        identical way.
        
        Test data set does not contain weights or class labels."""
    
    if make_submission:
        test_dataset = 'test.csv' # path to test data set.
        print '... loading test data'
        data_eval = np.array( list(csv.reader(open(test_dataset,'rb'), delimiter = ',')) )
        X_eval = np.array(data_eval[1:,1:], float)
        event_id = np.array(data_eval[1:,0], int)
        if scale_data:
            imputer.fit_transform(X_eval)
            X_eval = preprocessing.scale(np.array(X_eval)) # note "missing" values i.e. -999.0, are now set to 0.
        
        print '... making submission file'
        prob_eval = clf.predict_proba(X_eval).T[1]
        y_pred_eval =  prob_eval > signal_threshold
        print 'Number of submissions: ', len(prob_eval)
        pred = [classify_as_sb(y) for y in y_pred_eval] #1-->'s' and 0-->'b' for submission file
        ranks = rank(prob_eval) # submission file needs to be ranked.
        print 'Creating submission file: ', sub_filename
        f = open(sub_filename,"w")
        print >> f, "EventId,RankOrder,Class"
        for j in range(len(pred)): # print each line to submission file
            print >> f, str(event_id[j])+","+str(ranks[j])+","+str(pred[j])
        print '... done, bye'


