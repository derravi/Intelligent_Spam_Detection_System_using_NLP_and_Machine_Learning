#!/bin/bash

echo "Starting FastAPI..."
uvicorn Api:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit..."
streamlit run Frontend/frontend.py --server.port 8501 --server.address 0.0.0.0