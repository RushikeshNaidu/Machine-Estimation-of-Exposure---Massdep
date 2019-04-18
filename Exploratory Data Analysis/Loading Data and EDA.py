# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:57:40 2019

@author: Rushikesh
"""

# ---------------------------------- Loading Data ---------------------------------------------------------

import glob
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection, preprocessing
import seaborn as sns
from wordcloud import WordCloud

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

#-------------------------------- Exploratory Data Analysis -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Handing Class Imbalance
    
plt.title('No of Datapoints per Label in train', fontsize=15)
sns.countplot(train_y)
plt.xticks(np.arange(2), ('Not an Exposure','Exposure'))
plt.show()

#WordCloud for reports with conditions not a exposure

neg_reps = data[data.Label == 0]
neg_string = []
for t in neg_reps.Documents:
    neg_string.append(t)
neg_string = pd.Series(neg_string).str.cat(sep=' ')


wordcloud = WordCloud(width=1600, height=800,max_font_size=200).generate(neg_string)
plt.figure(figsize=(12,10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

#WordCloud for reports with conditions which are an exposure

pos_reps = data[data.Label == 1]
pos_string = []
for t in pos_reps.Documents:
    pos_string.append(t)
pos_string = pd.Series(pos_string).str.cat(sep=' ')


wordcloud = WordCloud(width=1600, height=800,max_font_size=200).generate(pos_string)
plt.figure(figsize=(12,10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()