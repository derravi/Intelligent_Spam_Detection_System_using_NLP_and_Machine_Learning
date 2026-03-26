import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Spam Detection", page_icon="📩")

st.title("📩 Intelligent Spam Detection System")

st.write("Enter a message to check whether it is Spam or Human.")

# Input box
user_input = st.text_area("Enter your message here")

# Button
if st.button("Predict"):

    if user_input.strip() == "":
        
        st.warning("Please enter some text")
    
    else:
        try:
            # API call
            response = requests.post(
                "http://127.0.0.1:8000/spam_pred",
                json={"input_text": user_input}
            )

            result = response.json()

            st.subheader("📊 Prediction Results")

            # Extract predictions
            lr = result["Prediction"]["Logistic Regression"]
            nb = result["Prediction"]["Naive Bayes"]
            xgb = result["Prediction"]["XGBoost"]

            # Display nicely
            st.write("### Logistic Regression")
            st.success(f"Prediction: {lr['Prediction']} | Accuracy: {lr['Accuracy']}%")

            st.write("### Naive Bayes")
            st.info(f"Prediction: {nb['Prediction']} | Accuracy: {nb['Accuracy']}%")

            st.write("### XGBoost")
            st.warning(f"Prediction: {xgb['Prediction']} | Accuracy: {xgb['Accuracy']}%")

        except Exception as e:
            st.error(f"Error: {e}")