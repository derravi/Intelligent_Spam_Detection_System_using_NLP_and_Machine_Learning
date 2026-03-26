from fastapi import FastAPI
from fastapi.responses import JSONResponse 
import pickle
from Schema.spam_model import spam_detection
import pandas as pd
import sqlite3

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


# =========================
# Sqlite3 DataBase setup
# =========================
new_df_file = sqlite3.connect("Database/history.db",check_name_thread=False)
new_db_object = new_df_file.cursor()

new_db_object.execute(
    """create table if not exists history(
    id integer primary key autoincrement,
    text text,
    prediction text
    )"""
)
#Commit for save File 
new_db_object.commit()


#Main App
app = FastAPI(title="Intelligent Spam Detection System using NLP and Machine Learning")

#Save the History of
history_data = []

#Default Route
@app.get("/")
def default_route():
    return {
        "Project": "Spam Detection API",
        "Version": "1.0",
        "Status": "Active ✅",

        "Description": "Detects spam or human text using ML models.",

        "Models": {
            "Naive Bayes": MultinomialNB_accuracy,
            "Logistic Regression": logistic_regressor_accuracy,
            "XGBoost": xgb_accuracy
        },

        "Tech": [
            "FastAPI",
            "TF-IDF",
            "Scikit-learn",
            "XGBoost"
        ],

        "Endpoint": {
            "POST /spam_pred": {
                "input": {"input_text": "Win ₹1000 now"},
                "output": "spam / human"
            }
        }
    }

#Prediction Apis
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
    xgboost_output = xgb.predict(output)
    xgboost_final_output = le.inverse_transform(xgboost_output)[0]

    #Save the XGboost Model prediction because they have very hig model accuracy
    new_db_object.execute(
        "insert into history (text , prediction) values (?, ?)",
        (tx.input_text,xgboost_final_output)
    )

    new_db_object.commit()

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
                "XGBoost":{
                    "Prediction":xgboost_final_output,
                    "Accuracy":xgb_accuracy   
                }
            }
        })

#History End point
@app.get("/history")
def get_history():

    new_db_object.execute("select * from history order by id desc")
    rows = new_db_object.fetchall()

    data = []
    for i in rows:
        data.append({
            "id":rows[0],
            "text":rows[1],
            "prediction":rows[2],
        })

    return {"history":data}

#remove the full history from the database
@app.delete("/history")
def delet_all_data():
    new_db_object.execute("delete from history")
    new_db_object.commit()

    return {"message":"All history deleted."}

#Remove the specific history
@app.delete("/history/{id}")
def delete_single(id:int):
    new_db_object.execute("delete from history where id = ?", (id,))
    new_db_object.commit()

    return {"message":f"Record {id} is deleted."}