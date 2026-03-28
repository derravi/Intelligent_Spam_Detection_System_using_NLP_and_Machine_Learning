import streamlit as st
import requests
import time

# =====================
# 🔹 Page Config
# =====================
st.set_page_config(
    page_title="Spam Detector", 
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================
# 🔹 Custom CSS
# =====================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Gradient background for title */
    .title-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Prediction cards */
    .pred-card {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid;
    }
    
    .pred-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Spam styling */
    .spam {
        border-left-color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    /* Ham styling */
    .ham {
        border-left-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Delete button styling */
    .delete-btn > button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .delete-btn > button:hover {
        box-shadow: 0 5px 15px rgba(239, 68, 68, 0.4);
    }
    
    /* Input area styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* History items */
    .history-item {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: rgba(255,255,255,0.1);
        transform: translateY(-2px);
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        height: 2px;
        border: none;
    }
    
    /* Metric styling */
    .metric {
        text-align: center;
        padding: 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    
    /* Animation for predictions */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.5s ease;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        padding: 1rem;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .badge-spam {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .badge-ham {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    /* Loading animation */
    .loading {
        text-align: center;
        padding: 2rem;
    }
    
    .loader {
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top: 3px solid #667eea;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# =====================
# 🔹 API Configuration
# =====================
API_URL = "http://127.0.0.1:8000"

# =====================
# 🔹 Session State Initialization
# =====================
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "prediction_made" not in st.session_state:
    st.session_state.prediction_made = False
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# =====================
# 🔹 Title Section
# =====================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="title-gradient">📩 AI Text Spam Detection</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">Protect your inbox with AI-powered spam detection</p>', unsafe_allow_html=True)

# =====================
# 🔹 Main Input Section
# =====================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### ✍️ Enter Your Message")
        text = st.text_area(
            "Message content",
            height=150,
            placeholder="Type or paste your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        predict_button = st.button("🔍 Predict", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# 🔹 Prediction Section
# =====================
if predict_button:
    if not text.strip():
        st.warning("⚠️ Please enter a message to analyze")
    else:
        with st.spinner("🔍 Analyzing message..."):
            try:
                res = requests.post(
                    f"{API_URL}/spam_pred",
                    json={"input_text": text},
                    timeout=10
                )
                
                result = res.json()["Prediction"]
                st.session_state.prediction_made = True
                st.session_state.last_prediction = result
                
                # Results container
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                st.markdown("### 📊 Prediction Results")
                
                # Create columns for metrics
                models = ["Logistic Regression", "Naive Bayes", "XGBoost"]
                
                # Display predictions in a grid
                cols = st.columns(3)
                for idx, model in enumerate(models):
                    pred = result[model]["Prediction"]
                    acc = result[model]["Accuracy"]
                    
                    with cols[idx]:
                        pred_class = "spam" if pred.lower() == "spam" else "ham"
                        icon = "🚨" if pred.lower() == "spam" else "✅"
                        color = "#ef4444" if pred.lower() == "spam" else "#10b981"
                        
                        st.markdown(f"""
                        <div class="pred-card {pred_class}" style="border-left-color: {color};">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <strong style="font-size: 1.1rem;">{model}</strong>
                                <span class="badge badge-{pred_class}">{icon} {pred.upper()}</span>
                            </div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: {color};">
                                {acc}%
                            </div>
                            <div style="font-size: 0.8rem; color: #888; margin-top: 0.5rem;">
                                Confidence Score
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to the API server. Please make sure the backend is running.")
            except Exception as e:
                st.error(f"🚨 An error occurred: {str(e)}")

# =====================
# 🔹 History Section
# =====================
st.markdown("<hr>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        history_button = st.button(
            "📜 View History" if not st.session_state.show_history else "📜 Hide History",
            use_container_width=True
        )
        
        if history_button:
            st.session_state.show_history = not st.session_state.show_history
    
    if st.session_state.show_history:
        with st.spinner("Loading history..."):
            try:
                res = requests.get(f"{API_URL}/history", timeout=10)
                
                if res.status_code == 404:
                    st.info("📭 No history found. Start by making some predictions!")
                else:
                    data = res.json()["data"]
                    
                    if not data:
                        st.info("📭 No history entries yet.")
                    else:
                        st.markdown("### 📜 Prediction History")
                        st.markdown(f"*Total entries: {len(data)}*")
                        
                        # Display history items
                        for item in data:
                            pred_class = "spam" if item['prediction'].lower() == "spam" else "ham"
                            icon = "🚨" if pred_class == "spam" else "✅"
                            color = "#ef4444" if pred_class == "spam" else "#10b981"
                            
                            st.markdown(f"""
                            <div class="history-item">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                                    <div>
                                        <span style="font-weight: bold; font-size: 1rem;">ID: {item['id']}</span>
                                        <span class="badge badge-{pred_class}" style="margin-left: 1rem;">{icon} {item['prediction'].upper()}</span>
                                    </div>
                                </div>
                                <div style="margin-top: 0.5rem;">
                                    <div style="color: #888; font-size: 0.8rem; margin-bottom: 0.25rem;">Message:</div>
                                    <div style="background: rgba(255,255,255,0.05); padding: 0.5rem; border-radius: 10px; font-size: 0.9rem;">
                                        {item['text'][:200]}{'...' if len(item['text']) > 200 else ''}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to the API server. Please check if the backend is running.")
            except Exception as e:
                st.error(f"🚨 Error loading history: {str(e)}")

# =====================
# 🔹 Delete Section
# =====================
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("### 🗑️ Manage History")
st.markdown("*Remove unwanted entries from the prediction history*")

col1, col2 = st.columns(2)

# 🔹 Delete All
with col1:
    st.markdown("#### Clear All Records")
    st.markdown("*Remove all history entries at once*")
    delete_all_button = st.button("🗑️ Clear All History", key="delete_all", use_container_width=True)
    
    if delete_all_button:
        with st.spinner("Clearing history..."):
            try:
                res = requests.delete(f"{API_URL}/history", timeout=10)
                
                if res.status_code == 200:
                    st.success("✅ All history cleared successfully!")
                    time.sleep(1)
                    st.rerun()
                elif res.status_code == 404:
                    st.warning("⚠️ No data found to delete")
                else:
                    st.error(f"❌ Failed to clear history: {res.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to the API server.")
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")

# 🔹 Delete One
with col2:
    st.markdown("#### Delete Specific Record")
    st.markdown("*Remove a single entry by its ID*")
    
    delete_id = st.number_input(
        "Enter record ID",
        min_value=1,
        step=1,
        key="delete_id_input",
        help="Enter the ID of the record you want to delete"
    )
    
    delete_one_button = st.button("🗑️ Delete Record", key="delete_one", use_container_width=True)
    
    if delete_one_button:
        if delete_id:
            with st.spinner(f"Deleting record {delete_id}..."):
                try:
                    res = requests.delete(f"{API_URL}/history/{int(delete_id)}", timeout=10)
                    
                    if res.status_code == 200:
                        st.success(f"✅ Record ID {int(delete_id)} deleted successfully!")
                        time.sleep(1)
                        st.rerun()
                    elif res.status_code == 404:
                        st.warning(f"⚠️ Record ID {int(delete_id)} not found")
                    else:
                        st.error(f"❌ Failed to delete: {res.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Cannot connect to the API server.")
                except Exception as e:
                    st.error(f"🚨 Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a valid ID")

# =====================
# 🔹 Footer
# =====================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #888; font-size: 0.8rem;">
    <p>🔒 Secure Spam Detection System | Powered by Machine Learning</p>
    <p>✨ Made with Streamlit</p>
</div>
""", unsafe_allow_html=True)