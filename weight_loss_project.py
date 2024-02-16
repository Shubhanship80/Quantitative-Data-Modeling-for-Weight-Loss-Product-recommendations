# -*- coding: utf-8 -*-
"""Weight_loss project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13hVhj-f7vm4ClSR8VALI49jSo02hnMC-

# Final Project (100)

<hr>
<br>

# Prerequisite Code
"""

import pandas as pd
import gensim
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from wordcloud import WordCloud
from sklearn.metrics import classification_report, recall_score, precision_score, f1_score, roc_curve, auc, precision_recall_curve

from google.colab import drive
drive.mount('/content/drive/')

reviews = pd.read_csv('/content/drive/My Drive/weightloss.csv')

"""# Part 1 (50)

## Directions

Include your code and any required written information immediately under the relevant sections or prompts in the space provided.

You will submit your code and written responses in this .ipynb template notebook in the space provided under the sectioned prompts. Under the prompts there are code and/or text cells provided. If additional cells are needed, add the cells under the appropriate heading.

Your code and written responses should be easy for someone who did not write the code or perform the analysis to follow. Points will be deducted for extraneous code or if file naming instructions are not followed.

**Note:** Your Part 1 submission will only include responses for Part 1. Part 2 should remain blank or hidden in the Part 1 submission.

<br>

**Due:** 11/26 at 11:59 PM ET

**Points:** 50

## 1.1 Problem Definition & Statement (20)

**1.1 A (5) First, use the code cell below to identify your group's selected dataset and the target variable (column name) that will be used for predictive modeling.**
"""

# @title Identify Problem/Dataset

Dataset = 'weightloss.csv' # @param ["lotion-reviews.csv", "spam.csv", "airlines.csv", "weightloss.csv", "amazon_reviews.csv"]
Target_Variable = 'rating' # @param {type:"string"}

print(Dataset)
print(Target_Variable)

"""**1.1 B (15) Next, use the text cell below for your problem definition and statement.**

**The problem statement should discuss the following: what is the problem and who it affects, financial/social implications of having a solution to the problem, how the model would be used in practice, and the acceptable level of model performance.**

Before offering a new weight loss program, our company decided to analyze the reviews and pick the best weight loss products for our customers. The dataset includes reviews of 39 drugs with ratings from 1 to 10. We would like to be able to predict positive reviews in order to provide drug reccomendation.
With implementtation of the model, we are looking to develop the successful weight loss program and increase customer satisfuction.

This dataset encapsulates the drugs and reviews of airline customers, offering a view of satisfaction levels and areas of potential improvement. Without a robust system for analyzing this data, there are substantial missed opportunities for airlines to enhance their business processes. Improving customer satisfaction based on the customer ratings and recommendations has the potential to promote or revitalize customer loyalty. Increased customer loyalty, in turn, translates to a positive impact on revenue and possibly profits. In addition, addressing the insights derived from this feedback can directly impact the overall customer experience. Content customers not only benefit the individual but also contribute to a more positive reputation for the airline as a whole.

The success of this model should be measured by its ability to accurately identify patterns and trends within the dataset, providing actionable information for airlines. We will be aiming for well-balanced scores, with a focus on identifying the negative class, which will be the most constructive for airlines to focus on. Ideally, this model will also be adaptable to varying scales of airline operations so that it may be utilized in both large international and smaller regional airlines.

<hr>
<br>

## 1.2 Data: Cleansing and Preprocessing (15)

**1.2 A (10) Use the code cell below (and add any additional cells, as necessary) to cleanse and preprocess the data that you will use in your analysis.**
"""

reviews.head()

reviews = reviews.drop(['rev_ID', 'date'], axis=1)

reviews.info()

missing_values = reviews.isnull().sum()
print(missing_values)

sns.heatmap(reviews.isnull(), cbar= False)                       #No missing values are present in the dataset

reviews['drugName'].nunique() # to check the number of unique values in column drugName. There are reviews for 39 different drugs.

reviews['drugName'].value_counts()

reviews.drugName.hist(xrot=90)

reviews.condition.hist(xrot= 90)

reviews['sentiment'] = reviews['rating'].replace({1:0, 2:0, 3:0, 4:0, 5:0, 6:1, 7:1, 8:1, 9:1, 10:1})
reviews.sentiment.hist()

print('Positive label proportion: ', reviews.sentiment.mean())

# Grouping the data by 'drugName' and calculating the mean rating for each drug
drug_ratings = reviews.groupby('drugName')['rating'].mean().reset_index()

# Sorting the drugs by their average ratings
sorted_drugs = drug_ratings.sort_values('rating', ascending=False)

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.bar(sorted_drugs['drugName'], sorted_drugs['rating'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Drug Name')
plt.ylabel('Average Rating')
plt.title('Average Rating per Drug')
plt.tight_layout()

# Show plot
plt.show()

plt.figure(figsize=(8, 6))
plt.bar(reviews['drugName'].value_counts().index, reviews['drugName'].value_counts().values, color='green')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Drug Name')
plt.ylabel('Number of Reviews')
plt.title('Number of Reviews per Drug')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(reviews['rating'], reviews['usefulCount'], alpha=0.5, color='green')
plt.xlabel('Rating')
plt.ylabel('Useful Count')
plt.title('Rating vs. Useful Count')
plt.tight_layout()
plt.show()

"""**1.2 B (5) In the text cell below, briefly describe and discuss (in paragraph format) the cleansing and preprocessing steps taken to prepare the data for analysis.**

To prepare the data for analysis, our initial steps involved examining the variable types and identifying any missing values within the dataset. After examining the data, we realised that there are no missing values in dataset. we removed the columns that we felt are not useful  9Co (rev_ID , date).considering all rating columns as potential target variables for sentiment analysis, we checked the distribution of values within these columns. Subsequently, we reset the index to prevent potential issues during model development.

---

## 1.3 Data: Description & EDA (15)

**1.3 A (8) Use the code cell below (and add any additional cells, as necessary) to describe the data and perform exploratory data analysis.**

**Description and EDA of the dataset should include: dataset overview, preview, dimensionality, visualization (text, target variable), descriptive statistics, and can include Cluster Analysis.**
"""

reviews.head()

reviews.shape

reviews.describe()

# Creating a vectorizer variable for clustering based on reviews.
feedback=[]
rating=[]
feedback=reviews['review'].tolist()
rating=reviews['rating'].tolist()
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words = 'english')
Vec = vectorizer.fit_transform(feedback)

# Evaluating the optimal number of natural clusters using the k-means model on reviews.
Sum_of_squared_distances = []
K = range(1,6)
for k in K:
   km = KMeans(n_clusters=k, max_iter=200, n_init=10)
   km = km.fit(Vec)
   Sum_of_squared_distances.append(km.inertia_)
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

# Performing data clustering using the optimal k-value for the K-Means model.
true_k = 2
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10, random_state=42)
model.fit(Vec)
labels=model.labels_
cl=pd.DataFrame(list(zip(reviews['rating'],labels)),columns=['rating','cluster'])
for i in range(1,11):
    rating_clusters = cl[cl['rating'] == i]['cluster'].value_counts()

text_data = ' '.join(reviews['review'].astype(str))

# Generate a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for Reviews')
plt.show()

"""**1.3 B (7) In the text cell below, describe (in paragraph format) the dataset and any important findings from your description and EDA. A discussion of class imbalance should also be included if present.**

The dataset represents customer reviews for the drugs by pharmaceuticals. The dataset contains 7 columns and 2438 rows. After cleaning and preprocessing, there are only 2 columns left with numerical values: rating, and usefulcount.
Descriptive statistics show that the mean for rating is 7.83. This suggests that there are many low rating reviews.
we figured out that the drug Phentermine has most reviews.we found through our exploratory data analysis that drugs like Zantryl,Wellbutrin XL,Bupropion,Suprenza,Desoxyn,Didrex,Methamphetamine have an average rating of 10.we also see that there is a relationship between rating and usefulcount.
For sentiment analysis, we decided to assign reviews with ratings from 1 to 5 the value of 0, considering them to be negative reviews. All other reviews were considered positive and were assigned the rating of 1. Based on the data analysis, we have an imbalanced dataset where we would try to balance while modeling. we performed word analysis to see which words appear in the reviews. We performed elbow method.We did ot find any missing values in the dataset.This dataset does not exhibit any class imbalance. This is because both clusters' sum of squared distances decreases at a similar rate due to the symmetry of the elbow curve.
The elbow curve indicates that two clusters are the ideal number for this dataset. This is due to the fact that after two clusters, the sum of squared distances (SSD) starts to change at a much slower rate.
The SSD serves as a gauge for the degree of cluster segregation.we generated word clouds for both sentiments to identify and highlight the most common words in reviews for each sentiment, respectively.

---

<br>

# Part 2 (50)
"""

!pip install -q -U tensorflow-text
!pip install -q tf-models-official

"""## Directions

Include your code and any required written information immediately under the relevant sections or prompts in the space provided.

You will submit your code and written responses in this .ipynb template notebook in the space provided under the sectioned prompts. Under the prompts there are code and/or text cells provided. If additional cells are needed, add the cells under the appropriate heading.

Your Final Project Part 2 submission should include all Part 1 and Part 2 code and responses.

Your code and written responses should be easy for someone who did not write the code or perform the analysis to follow. Points will be deducted for extraneous code or if file naming instructions are not followed.

<br>

**Due:** 12/17 at 11:59 PM ET

**Points:** 50

## 2.1 Analysis (25)

**2.1 (25) Perform (at least) 3 types of classification analysis demonstrated in the course. At least one type must be a deep learning model using either a pre-trained or data-trained embedding layer.**
"""

#Spliting Data
X = reviews['review']
y = reviews['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)

# Listing the models that will be built

names = ["Logistic Regression", "SVM", "Decision Tree", "AdaBoost", "Neural Net"]

# Defining the correponding list of classifiers, setting parameters where needed

classifiers = [LogisticRegression(),
               SVC(probability=True),
               DecisionTreeClassifier(max_depth=5),
               AdaBoostClassifier(),
               MLPClassifier(alpha=1, max_iter=1000)
               ]

#Choose a BERT model to fine-tune

bert_model_name = 'small_bert/bert_en_uncased_L-2_H-128_A-2'  #@param ["bert_en_uncased_L-12_H-768_A-12", "bert_en_cased_L-12_H-768_A-12", "bert_multi_cased_L-12_H-768_A-12", "small_bert/bert_en_uncased_L-2_H-128_A-2", "small_bert/bert_en_uncased_L-2_H-256_A-4", "small_bert/bert_en_uncased_L-2_H-512_A-8", "small_bert/bert_en_uncased_L-2_H-768_A-12", "small_bert/bert_en_uncased_L-4_H-128_A-2", "small_bert/bert_en_uncased_L-4_H-256_A-4", "small_bert/bert_en_uncased_L-4_H-512_A-8", "small_bert/bert_en_uncased_L-4_H-768_A-12", "small_bert/bert_en_uncased_L-6_H-128_A-2", "small_bert/bert_en_uncased_L-6_H-256_A-4", "small_bert/bert_en_uncased_L-6_H-512_A-8", "small_bert/bert_en_uncased_L-6_H-768_A-12", "small_bert/bert_en_uncased_L-8_H-128_A-2", "small_bert/bert_en_uncased_L-8_H-256_A-4", "small_bert/bert_en_uncased_L-8_H-512_A-8", "small_bert/bert_en_uncased_L-8_H-768_A-12", "small_bert/bert_en_uncased_L-10_H-128_A-2", "small_bert/bert_en_uncased_L-10_H-256_A-4", "small_bert/bert_en_uncased_L-10_H-512_A-8", "small_bert/bert_en_uncased_L-10_H-768_A-12", "small_bert/bert_en_uncased_L-12_H-128_A-2", "small_bert/bert_en_uncased_L-12_H-256_A-4", "small_bert/bert_en_uncased_L-12_H-512_A-8", "small_bert/bert_en_uncased_L-12_H-768_A-12", "albert_en_base", "electra_small", "electra_base", "experts_pubmed", "experts_wiki_books", "talking-heads_base"]

map_name_to_handle = {
    'bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3',
    'bert_en_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/3',
    'bert_multi_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/3',
    'small_bert/bert_en_uncased_L-2_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-2_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-2_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-2_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-4_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-4_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-4_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-4_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-6_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-6_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-6_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-6_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-8_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-8_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-8_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-8_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-10_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-10_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-10_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-10_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-12_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-12_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-12_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-768_A-12/1',
    'albert_en_base':
        'https://tfhub.dev/tensorflow/albert_en_base/2',
    'electra_small':
        'https://tfhub.dev/google/electra_small/2',
    'electra_base':
        'https://tfhub.dev/google/electra_base/2',
    'experts_pubmed':
        'https://tfhub.dev/google/experts/bert/pubmed/2',
    'experts_wiki_books':
        'https://tfhub.dev/google/experts/bert/wiki_books/2',
    'talking-heads_base':
        'https://tfhub.dev/tensorflow/talkheads_ggelu_bert_en_base/1',
}

map_model_to_preprocess = {
    'bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'bert_en_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-2_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-4_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-6_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-8_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-10_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'small_bert/bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'bert_multi_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_multi_cased_preprocess/3',
    'albert_en_base':
        'https://tfhub.dev/tensorflow/albert_en_preprocess/3',
    'electra_small':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'electra_base':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'experts_pubmed':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'experts_wiki_books':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
    'talking-heads_base':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3',
}

tfhub_handle_encoder = map_name_to_handle[bert_model_name]
tfhub_handle_preprocess = map_model_to_preprocess[bert_model_name]

print(f'BERT model selected           : {tfhub_handle_encoder}')
print(f'Preprocess model auto-selected: {tfhub_handle_preprocess}')

from keras.metrics import *
import tensorflow as tf
import tensorflow_hub as hub # pre-trained models
import tensorflow_text as text # text pre-processing functions
from official.nlp import optimization  # to create AdamW optimizer

#Creating a list of metrics
METRICS = [
      TruePositives(name='tp'),
      FalsePositives(name='fp'),
      TrueNegatives(name='tn'),
      FalseNegatives(name='fn'),
      BinaryAccuracy(name='accuracy'),
      Precision(name='precision'),
      Recall(name='recall'),
      AUC(name='auc'),
      AUC(name='prc', curve='PR'), # precision-recall curve

]

#Instantiating clear session
from keras.backend import clear_session
clear_session()

def build_classifier_model():
  text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
  preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
  encoder_inputs = preprocessing_layer(text_input)
  encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')
  outputs = encoder(encoder_inputs)
  net = outputs['pooled_output']
  net = tf.keras.layers.Dense(64,activation='relu')(net)
  net = tf.keras.layers.Dense(28,activation='relu')(net)
  net = tf.keras.layers.Dropout(0.2)(net)
  net = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(net)
  return tf.keras.Model(text_input, net)

epochs = 10
steps_per_epoch = 100
num_train_steps = steps_per_epoch * epochs
num_warmup_steps = int(0.1*num_train_steps)

init_lr = 5e-5
optimizer = optimization.create_optimizer(init_lr=init_lr,
                                          num_train_steps=num_train_steps,
                                          num_warmup_steps=num_warmup_steps,
                                          optimizer_type='adamw')

classifier_model = build_classifier_model()
loss = tf.keras.losses.BinaryCrossentropy()

classifier_model.compile(optimizer=optimizer,
                         loss=loss,
                         metrics=METRICS)

print(f'Training model with {tfhub_handle_encoder}')
history = classifier_model.fit(x=X_train.values,y=y_train,
                               validation_data=(X_test.values,y_test),
                               epochs=epochs)

"""## 2.2 Model Evaluation (15)

**2.2 A (8) Evaluate the models on both the training and testing sets to obtain both performance and goodness of fit.**
"""

# Iterating through the list of models
# Executing the pipeline (TFIDF Vectorizer + model) for each
# Calculating the print out the metrics for each model

for name, clf in zip(names, classifiers):
  clf_pipe = Pipeline([
                    ('tfidf', TfidfVectorizer()), # transforms word/count feature representation into word/tfidf feature vector
                    (name, clf), # builds a NB model assuming multinomial feature distributions
                    ])

  clf_pipe.fit(X_train,y_train)

  pred = clf_pipe.predict(X_test)
  pred_prob = clf_pipe.predict_proba(X_test)[:, 1]

  fpr, tpr, thresholds = roc_curve(y_test, pred_prob)
  precision, recall, thresholds_pr = precision_recall_curve(y_test, pred)

  print('\n\n', name, '\n\n')
  print(classification_report(y_test, pred))
  print('ROC AUC: ', auc(fpr, tpr))
  print('Precision/Recall AUC: ', auc(precision, recall))
  print('\n\n')

model_results = classifier_model.evaluate(X_train.values, y_train, batch_size=128, verbose=0)

for name, value in zip(classifier_model.metrics_names, model_results):
  print(name, ': ', value)

model_results = classifier_model.evaluate(X_test.values, y_test, batch_size=128, verbose=0)

for name, value in zip(classifier_model.metrics_names, model_results):
  print(name, ': ', value)

"""**2.2 B (7) Based on your output in 2.2A, discuss and compare the goodness of fit and performance for each of the classification models. Which model is preferred? Why? Explain.**

Goodness of Fit and Performance Comparison:
Logistic Regression (LR): Strong overall performance (accuracy 0.84, f1 0.27). High precision for class 0 (0.96) Good ROC AUC (0.89).

SVM: Excellent performance (accuracy 0.86, f1 0.41). High precision for both classes (0.85, 1.00). lower recall for class 0 (0.26). Highest ROC AUC (0.91).

Decision Tree: Good performance (accuracy 0.83, f1 0.35). High recall for class 1 (0.97), but precision suffers (0.79). Low recall for class 0 (0.24). Lowest ROC AUC (0.64).

AdaBoost: Similar to LR in overall performance (accuracy 0.83, f1 0.47). High precision for class 1 (0.87), highest recall for class 1 (0.92). Good ROC AUC (0.79).

Neural Net: Similar to LR and AdaBoost in overall performance (accuracy 0.87, f1 0.99). High precision for class 0 (0.92), moderate recall for class 1 (0.87). Good ROC AUC (0.90).


Preferred Model:

Neural Networks: Highest accuracy, f1, and ROC AUC, with good balance between precision and recall for both classes. High overall performance.

## 2.3 Discussion & Conclusion (10)

**2.3 (10) Briefly summarize the problem statement and data. Then, discuss your analysis and findings. Within the context of the business problem and your analysis results, provide business recommendations. Be sure to discuss any limitations, constraints, or ethical concerns that could impact the implementation of the recommended solution.**

**Problem statement and Summary of Data:**

The problem involves choosing the top weight loss products according to customer reviews in order to increase a new weight loss program's efficacy. Reviews of 39 medications, each with a rating between 1 and 10, make up the dataset. Anticipating favorable evaluations is intended to help with medication recommendations and boost client satisfaction.

**Analysis and Findings:**

Data exploration: After cleaning, there are 2438 rows and 7 columns in the dataset. There is a mix of high and low ratings, as seen by the mean rating of 7.83. The most reviews are for Phentermine, while some medications (like Zantryl and Wellbutrin XL) are consistently rated highly.

Sentiment Analysis: Sentiment labels were assigned in order to make modeling easier. The majority of the reviews in the dataset are positive, indicating a class imbalance.

Classification Models: We trained and assessed five models: Neural Net, SVM, AdaBoost, Decision Tree, and Logistic Regression. In terms of recall, accuracy, precision, and ROC AUC, the Neural Net model performs better than the others.

BERT Deep Learning Model: Shows strong performance with high recall, accuracy, precision, and ROC AUC on training and testing data.

**Business recommendations:**

Model of Choice: The Neural Net and BERT models perform better, particularly when it comes to correctly identifying positive reviews. Neural Net is favored because of the significance of recall and precision in medication recommendations.

Applying the Model: Using the Neural Net model to analyze customer reviews' sentiment in real time. Making recommendations for the best weight-loss medications for the new program based on the insights gained.

Impact on Business: Higher customer satisfaction leads to higher customer loyalty, which raises sales and profits. The model contributes to the weight loss program's success by helping with the thoughtful selection of weight loss medications.

**Limitations and Ethical Issues:**

Unbalanced Dataset: To avoid skewed model results, addressing the class imbalance. When modeling, use of  methods such as oversampling or undersampling.

Performance Metrics: When choosing metrics, taking in the  business priorities into account. Finding the right balance between recall and precision for weight loss medication recommendations is essential.

Data Privacy: Verifying adherence to applicable laws. Keep client information safe while deploying the model.

Ethical Implications: Clearly stating the goals and constraints of the model. Avoiding biases when recommending drugs as the health of customers top priority.

**Conclusion:**

The analysis highlights how important advanced models are to optimizing product recommendations for weight loss. Robust solutions are provided by the Neural Net and BERT models, which help make the weight loss program successful. However, responsible implementation necessitates careful consideration of ethical issues and limitations.
"""