#!/usr/bin/env bash
pip install -r requirements.txt
streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
