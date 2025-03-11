import streamlit as st
import os
import base64
import time
import datetime
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import joblib
import json
from datetime import datetime, timedelta
from collections import Counter


# ✅ Set Page Configuration FIRST!
st.set_page_config(
    page_title="Smart Serve - Food Waste Management",
    page_icon="🍽️",
    layout="wide",
)

logo_path = r"C:\Users\G6\Desktop\hackathon\assets\images\logo final.png"  # Use a relative path
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="120"/>'
else:
    logo_html = ""

st.markdown(
    f"""
    <div class="card">
        {logo_html}
        <h1 class="center">Smart 🍽️ Serve</h1>
        <h4 class="center">Revolutionizing Food Waste Management.</h4>
    </div>
    """,
    unsafe_allow_html=True
)


# Now import other modules
from home import show_home
from ai_waste_prediction import show_ai_waste_prediction
from inventory import show_inventory
from donation import show_donation
from recipes import show_recipes
from leaderboard import show_leaderboard

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🧠 AI Waste Prediction", "⏲️ Inventory & Expiry Alerts", "🤝 Food Donation","👨‍🍳 Recipe Suggestions","🏆 Leaderboard"])

# Call respective function based on page selection
if page == "🏠 Home":
    show_home()
elif page == "🧠 AI Waste Prediction":
    show_ai_waste_prediction()
elif page == "⏲️ Inventory & Expiry Alerts":
    show_inventory()
elif page == "🤝 Food Donation":
    show_donation()
elif page == "👨‍🍳 Recipe Suggestions":
    show_recipes()
elif page == "🏆 Leaderboard":
    show_leaderboard()
