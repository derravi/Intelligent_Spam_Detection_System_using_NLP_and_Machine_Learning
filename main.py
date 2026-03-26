# =========================
# LOAD LIBRARY
# =========================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.utils import resample
from sklearn.linear_model import LogisticRegression
import pickle
from xgboost import XGBClassifier

from sklearn.preprocessing import LabelEncoder

# =========================
# LOAD DATA
# =========================

try:

    df = pd.read_csv("Data_set/updated.csv")
    print("File loaded successfully")
    
except FileNotFoundError as e:
    print(f"File not found: {e}.")
    
except Exception as e1:
    print(f"Something went wrong: {e1}.")

print(f"Les see the Old data Into this CSV file they have total {df.shape[0]} rows and the {df.shape[1]} columns.")

df = df.drop(['Unnamed: 0'],axis=1)

df.head()

df['input'] = df['input'].fillna(df['input'].mode()[0])
print("EDA Completed.")

# =========================
# DATA BALANCING 
# =========================

df_human = df[df['output'] == 'human']
df_spam = df[df['output'] == 'spam']

new_spam_upscale = resample(
    df_spam,
    replace=True,
    n_samples = len(df_human),
    random_state=42
)

new_df = pd.concat([df_human,new_spam_upscale])

print("Data Balanced.")

print(new_df['output'].value_counts())

x=new_df['input']
y=new_df['output']

x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=42,test_size=0.2)
print("Data Training testing is completed.")

#Using Vectorized

vectorizer = TfidfVectorizer()

x_train_tfidf = vectorizer.fit_transform(x_train)
x_test_tfidf = vectorizer.transform(x_test)

print("Vectorization is completed.")

#MultinomialNB Model Training

lnb_model = MultinomialNB()

lnb_model.fit(x_train_tfidf,y_train)

lnb_prediciotn = lnb_model.predict(x_test_tfidf)

print("MultinomialNB Model trained successfully.")

# Lets see the mathamatics terms
# For MultinomialNB Model
print("Lets see the mathamatics terms For MultinomialNB Model.\n")

MultinomialNB_accuracy = round(accuracy_score(y_test,lnb_prediciotn)*100,2)

print("Accuracy Score of MultinomialNB model:",MultinomialNB_accuracy)
print("\nClassification Report:", classification_report(y_test,lnb_prediciotn))
print("\nconfusion matrix:\n", confusion_matrix(y_test,lnb_prediciotn))

# Logistic REgression model Training

lr_model = LogisticRegression()

lr_model.fit(x_train_tfidf,y_train)

lr_prediciton = lr_model.predict(x_test_tfidf)

print("Logistic Regression Model trained successfully.")



# Lets see the mathamatics terms
# Logistic Regression Model

print("Lets see the mathamatics terms For Logistic Regression.\n")

logistic_regressor_accuracy = round(accuracy_score(y_test,lr_prediciton)*100,2)

print("Accuracy Score of the Logistic Regressio odel:",logistic_regressor_accuracy)
print("\nClassification Report:", classification_report(y_test,lr_prediciton))
print("\nconfusion matrix:\n", confusion_matrix(y_test,lr_prediciton))



# encode labels
le = LabelEncoder()
y_train_encoded = le.fit_transform(y_train)
y_test_encoded = le.transform(y_test)

# model
xgb = XGBClassifier(
    random_state=42,
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6
)

# train
xgb.fit(x_train_tfidf, y_train_encoded)

# predict
xgb_prediction = xgb.predict(x_test_tfidf)

# decode back (optional)
xgb_prediction_labels = le.inverse_transform(xgb_prediction)

# accuracy
xgb_accuracy = round(accuracy_score(y_test, xgb_prediction_labels)*100,2)

print("Accuracy Score:", xgb_accuracy)
print("\nClassification Report:\n", classification_report(y_test, xgb_prediction_labels))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, xgb_prediction_labels))

# Compare the accuracy of all models

if MultinomialNB_accuracy > logistic_regressor_accuracy and MultinomialNB_accuracy > xgb_accuracy:
    print(f"MultinomialNB has highest accuracy: {MultinomialNB_accuracy}")

elif logistic_regressor_accuracy > xgb_accuracy:
    print(f"Logistic Regression has highest accuracy: {logistic_regressor_accuracy}")

else:
    print(f"XGBoost has highest accuracy: {xgb_accuracy}")

#User Inout 

text =  input("Enter the Text:- ")

new_data = pd.DataFrame([{
    "text" : text
}])

unwanted_charecters = r'[.><+\-*/=!@#$%^&()\-:;?`~]'

new_data['text'] = new_data['text'].str.lower()
new_data['text'] = new_data['text'].replace(unwanted_charecters," ",regex=True)
new_data['text'] = new_data['text'].str.strip()
new_data['text'] = new_data['text'].replace(r'\s+',' ',regex=True)
new_data['text'] = new_data['text'].replace(r'\d+',' ',regex=True)


txt_output = vectorizer.transform(new_data['text'])


lnb_final_output = lnb_model.predict(txt_output)[0]
lr_final_output = lr_model.predict(txt_output)[0]

xgboost_prediction = xgb.predict(txt_output)
xgboost_prediction_output = le.inverse_transform(xgboost_prediction)[0]


print("\nModel Comparison Result:\n")

print(f"{'Model':<30} | {'Prediction':<10} | Accuracy")
print("-"*60)

print(f"{'Logistic Regression':<30} | {lr_final_output:<10} | {round(logistic_regressor_accuracy,2)}%")

print(f"{'Multinomial Naive Bayes':<30} | {lnb_final_output:<10} | {round(MultinomialNB_accuracy,2)}%")

print(f"{'XGboost Regression':<30} | {xgboost_prediction_output:<10} | {round(xgb_accuracy,2)}%")

print("-"*60)

#Make the pickle model
model = {
    "vectorizer_model" : vectorizer,
    "label_encoder":le,
    "MultinomialNB_model" : lnb_model,
    "Linear_regressor_model" : lr_model,
    "xgbooster_model":xgb,
    "lr_accuracy":logistic_regressor_accuracy,
    "lnb_accuracy":MultinomialNB_accuracy,
    "xgb_accuracy":xgb_accuracy,
}
with open("Models/pkl_model.pkl",'wb') as f:
    pickle.dump(model,f)
print("Pickle model is Created.")