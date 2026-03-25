from fastapi import FastAPI
from fastapi.responses import JSONResponse 
import pickle
from Schema.spam_model import spam_detection
import pandas as pd

#Access the Pickle model for ML training Pipelines
with open('Models/pkl_model.pkl','rb') as f:
    model = pickle.load(f)

vectorizer = model['vectorizer_model']
le = model["label_encoder"]
lnb_model = model['MultinomialNB_model']
lr_model = model['Linear_regressor_model']
xgb = model['xgbooster_model']
logistic_regressor_accuracy = model['lr_accuracy']
MultinomialNB_accuracy = model['lnb_accuracy']
xgb_accuracy = model['xgb_accuracy']

app = FastAPI(title="Intelligent Spam Detection System using NLP and Machine Learning")


@app.get("/")
def default_route():
    return {'message':'Intelligent Spam Detection System using NLP and Machine Learning'}

@app.post("/spam_pred")
def spam_prediciton(tx:spam_detection):
    
    new_df = pd.DataFrame([{
        "text":tx.input_text
    }])

    unwanted_charecters = r'[.><+\-*/=!@#$%^&()\-:;?`~]'

    new_df['text'] = new_df['text'].str.lower()
    new_df['text'] = new_df['text'].replace(unwanted_charecters," ",regex=True)
    new_df['text'] = new_df['text'].str.strip()
    new_df['text'] = new_df['text'].replace(r'\s+',' ',regex=True)
    new_df['text'] = new_df['text'].replace(r'\d+',' ',regex=True)


    output = vectorizer.transform(new_df['text'])

    #For Multinomial Naive Bayes
    lnb_final_output = lnb_model.predict(output)[0]

    #For Logistic Regression  
    lr_final_output = lr_model.predict(output)[0]

    #For XGboost Regression 
    xgboost_output = xgb.predict(new_df)
    xgboost_final_output = le.inverse_transform(xgboost_output)[0]


    return JSONResponse(status_code=200,
        content={
            "Status":"Status",
            "Prediction": {
                "Logistic Regression":{
                    "Prediction":lnb_final_output,
                    "Accuracy":logistic_regressor_accuracy
                },
                "Naive Bayes":{
                    "Prediction":lr_final_output,
                    "Accuracy":MultinomialNB_accuracy   
                },
                "Naive Bayes":{
                    "Prediction":xgboost_final_output,
                    "Accuracy":xgb_accuracy   
                }

                
            }
        })