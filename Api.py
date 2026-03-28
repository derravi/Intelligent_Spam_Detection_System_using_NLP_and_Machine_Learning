from fastapi import FastAPI
from fastapi.responses import JSONResponse 
import pickle
from Schema.spam_model import spam_detection
import pandas as pd
import sqlite3
from fastapi import HTTPException

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
conn = sqlite3.connect("history.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    prediction TEXT
)
""")

conn.commit()


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
    cursor.execute(
    "INSERT INTO history (text, prediction) VALUES (?, ?)",
    (tx.input_text, xgboost_final_output)
    )
    conn.commit()

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
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cursor.fetchall()

    #check the history is available ot its empty
    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"Record with id {id} not found." 
        )

    data = []
    for i in rows:
        data.append({
            "id": i[0],
            "text": i[1],
            "prediction": i[2]
        })

    return {
        "status": "success",
        "count": len(data),
        "data": data
    }

#remove the full history from the database
@app.delete("/history")
def delete_history():
     ... 
     # check if data exists
     cursor.execute("select count(*) from history")
     count = cursor.fetchone()[0]

     if count == 0:
        raise HTTPException(
            status_code=404,
            detail="No history found."
        )

     cursor.execute("delete from history")
     conn.commit()

     return {
         "status":"success",
         "message":f"All {count} records deleted."
     }

#Remove the specific history
@app.delete("/history/{id}")
def delete_single(id: int):
    cursor.execute("select * from history where id = ?", (id,))
    record = cursor.fetchone()

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Record with id {id} not found."
        )

    cursor.execute("delete from history where id = ?", (id,))
    conn.commit()

    return {
        "status": "success",
        "message": f"Record {id} deleted"
    }