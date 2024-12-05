import streamlit as st
import requests
import matplotlib.pyplot as plt
import time
import os
import numpy as np
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="monitoring-kki-2024", page_icon="🌍", layout="wide")
# Back4App credentials
APPLICATION_ID = "8bfJ9zjY6QwRlihGZ2Ln0IZsxaKpNBIEkztavQnE"
REST_API_KEY = "C33dLXBbeIjGAcQELuCvfxJWEb9gTw1S68L1YRwr"
BASE_URL = "https://parseapi.back4app.com/classes/Monitoring"

# Function to fetch data from Back4App
def fetch_monitoring_data():
    headers = {
        "X-Parse-Application-Id": APPLICATION_ID,
        "X-Parse-REST-API-Key": REST_API_KEY,
    }
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return []

#sidebar
st.sidebar.markdown('<h4 class="sidebar-text">NAVIGASI LINTASAN</h4>', unsafe_allow_html=True)
path = st.sidebar.radio("", ["Lintasan A ⚓", "Lintasan B ⚓"])
start_monitoring_button = st.sidebar.button("START BUTTON", key="start_monitoring_button")

#Header
col1, col2, col3, col4 = st.columns([1,4,4,1])
with col1:
    st.image('Images/logo.jpeg', width=75)
with col2:
    st.markdown("<h6 class='header-text'> BARELANG MARINE ROBOTICS TEAM </h6>", unsafe_allow_html=True)
with col3:
    st.markdown("<h6 class='header-text'> POLITEKNIK NEGERI BATAM </h6>", unsafe_allow_html=True)
with col4:
    st.image('Images/polibatamLogo.jpeg', width=80)

#lintasan
if path == "Lintasan A ⚓":
    st.markdown("<h5 class='judul-text'>LINTASAN A</h5>", unsafe_allow_html=True)
elif path == "Lintasan B ⚓":
    st.markdown("<h5 class='judul-text'>LINTASAN B</h5>", unsafe_allow_html=True)


table_placeholder = st.empty()
while True:
    monitoring_data = fetch_monitoring_data()

    if monitoring_data:
        # Prepare the data for the table
        table_data = [{"COG": item.get("COG", "N/A"), "SOG_Knot": item.get("SOG_Knot", "N/A")} for item in monitoring_data]
        # Update the table in the placeholder
        with table_placeholder:
            st.table(table_data)
    else:
        with table_placeholder:
            st.write("No data available.")
    time.sleep(5)


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: #b2d3eb;
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
    <style>
        .header-text {
            text-align: center;
            color: #ffff;
            background-color: #3A6E8F;
            padding: 15px; 
            border-radius: 15px;
            margin-bottom: 1px; 
            border: 2px solid white;
            font-size: 16px;
            font-family: 'Montserrat', sans-serif;

        }
        .judul-text {
            text-align: center;
            color: white;
            background-color: #65A7D3;
            padding: 5px; 
            border-radius: 10px;
            margin-bottom: 5px; 
            border: 2px solid white;
            font-size: 14px;
            font-family: 'Montserrat', sans-serif;

        }
        [data-testid="stMetricValue"] {
            font-size: 16px;
            color : #242649;
            font-family: 'Montserrat', sans-serif;
            font-weight: bold; 

        }
        [data-testid="stMetricLabel"] {
            font-size: 12px;
            color : black;
            font-family: 'Montserrat', sans-serif;
        }
        .stButton > button {
            background-color: #4CAF50; 
            color: #ffff;    
            border: 2px solid white;
            font-weight: bold; 
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .sidebar-text {
            text-align: center;
            color: #FFFF;
            background-color: #3A6E8F;
            padding: 10px; 
            border-radius: 15px;
            border: 2px solid white;
            font-size: 12px;
            font-family: 'Montserrat', sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #7FBADC;
            color: #ffff;
            font-weight: bold;
            font-family: 'Montserrat', sans-serif; 
        }
    </style>
    """, 
    unsafe_allow_html=True
)
