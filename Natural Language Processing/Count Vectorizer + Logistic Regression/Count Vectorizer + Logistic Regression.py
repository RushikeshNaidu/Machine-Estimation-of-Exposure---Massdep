#Importing necessary libraries

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.linear_model import LogisticRegression
from sklearn import model_selection, preprocessing


# ---------------------- Loading Data ----------------------------------------------------------

SEED = 2000
os.chdir('D:/Massdep/Input Data Final/Positive FIles/Y')# Please enter the directory containing the positive flagged PDF files
documents = []
for file in glob.glob("*.txt"): # read all txt files in working directory
    file_content = open(file, "r")
    lines = file_content.read().splitlines()
    for line in lines:
        documents.append(line)

data = pd.DataFrame({'Documents': documents, 'Label': 1})


os.chdir('D:/Massdep/Input Data Final/Negative FIles/N') # Please enter the directory containing the negative flagged PDF files
documents1 = []
for file in glob.glob("*.txt"): # read all txt files in working directory
    file_content = open(file, "r")
    lines = file_content.read().splitlines()
    for line in lines:
        documents1.append(line)

data1 = pd.DataFrame({'Documents': documents1, 'Label': 0})


data = data.append(data1)

data['Documents'].replace('', np.nan, inplace=True)

data.dropna(subset=['Documents'], inplace=True)

#split the dataset into training and validation datasets 
train_x, test_x, train_y, test_y = model_selection.train_test_split(data['Documents'], data['Label'])
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(train_x, train_y, test_size=.2, random_state=SEED)

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)
test_y  = encoder.fit_transform(test_y)

print ("Train set has total {0} entries with {1:.2f}% negative, {2:.2f}% positive".format(len(train_x),(len(train_x[train_y == 0]) / (len(train_x)*1.))*100,  (len(train_x[train_y == 1]) / (len(train_x)*1.))*100))
print ("Validation set has total {0} entries with {1:.2f}% negative, {2:.2f}% positive".format(len(valid_x),(len(valid_x[valid_y == 0]) / (len(valid_x)*1.))*100,(len(valid_x[valid_y == 1]) / (len(valid_x)*1.))*100))
print ("Test set has total {0} entries with {1:.2f}% negative, {2:.2f}% positive".format(len(test_x),(len(test_x[test_y == 0]) / (len(test_x)*1.))*100, (len(test_x[test_y == 1]) / (len(test_x)*1.))*100))


#----------------------------------------------------------------------------------------------
"""Natural Language Processing - Count Vectorizer + Logistic Regression"""
#---------------------------------------------------------------------------------------------

ctv = CountVectorizer(analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3), stop_words = 'english')

# Fitting Count Vectorizer to both training and test sets (semi-supervised learning)
ctv.fit(list(train_x) + list(valid_x))
xtrain_ctv =  ctv.transform(train_x) 
xvalid_ctv = ctv.transform(valid_x)

# Fitting a simple Logistic Regression on Counts
clf = LogisticRegression(C=1.0)
clf.fit(xtrain_ctv, train_y)
predictions = clf.predict(xvalid_ctv)

print ("Average Accuracy: %0.3f " % accuracy_score(valid_y, predictions))

print(classification_report(valid_y, predictions))


#---------------------Plotting Confusion Matrix -----------------------------------------------

# Creates a confusion matrix
cm = confusion_matrix(valid_y, predictions) 

# Transform to df for easier plotting
cm_df = pd.DataFrame(cm)

plt.figure(figsize=(5.5,4))
sns.heatmap(cm_df, annot=True)
plt.title('Logistic Regression \nAccuracy:{0:.3f}'.format(accuracy_score(valid_y, predictions)))
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()