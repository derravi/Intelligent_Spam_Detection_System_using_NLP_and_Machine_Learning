Project Title:- Intelligent Spam Detection System using NLP and Machine Learning

CSV file download link:- https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset?resource=download 

Overview:- This project focuses on building an intelligent spam detection system using NLP and machine learning techniques. It converts text data into numerical features using TF-IDF and applies a Naive Bayes model for classification. The system efficiently identifies spam messages with high accuracy and supports real-time prediction through a simple user interface.

#Steps for Run This Projects.

Step:-1 
-> Install all the Library which is mentioned in the requirements.txt file.

Step:-2
-> open the 1st terminal on the same folder then Run belov the command;
    -> Command:- uvicorn Api:app --reload

Step:-3
-> Open the second terminal on the Frontend folder and run the belov comman;
    -> streamlit run frontend.py

Step:-4
-> The Frontend View Automaticaly Open in your browser through the "localhost:8501"

Step:-5 
-> Now Project is redy for Run.

#Project Structure

├── 📁 Data_Cleaning
│   └── 📄 EDA.ipynb
├── 📁 Data_set
│   ├── 📄 spam.csv
│   └── 📄 updated.csv
├── 📁 Database
│   └── 📄 history.db
├── 📁 Frontend
│   └── 🐍 frontend.py
├── 📁 Models
│   └── 📄 pkl_model.pkl
├── 📁 Schema
│   └── 🐍 spam_model.py
├── 🐍 Api.py
├── 🐳 Dockerfile
├── 📝 README.md
├── 📄 history.db
├── 📄 main.ipynb
├── 🐍 main.py
└── 📄 requirements.txt