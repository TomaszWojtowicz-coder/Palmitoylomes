import streamlit as st
from PIL import Image
import pandas as pd
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from streamlit.components.v1 import html
import json
import requests
import xml.etree.ElementTree as ET
import base64

# Ensure correct image zoom library is imported
from streamlit_image_zoom import image_zoom  # Ensure you have the 'streamlit_image_zoom' package installed

# Set page layout
st.set_page_config(layout="wide")

# CSS Styling
st.markdown("""
    <style>
        body, .stApp { background-color: #ffffff; color: #3f3f4d; }
        h1 { font-size: 30px !important; }
        h2 { font-size: 25px !important; }
        h3 { font-size: 22px !important; }
        h1, h2, h3, h4, h5, h6 { text-indent: 30px; margin-bottom: 60px; background-color: #e9e6fc; color: #3f3f4d; }
        .stButton > button { background-color: #966edb; color: #1F1A3D; }
        .dataframe th {
            writing-mode: vertical-rl;
            transform: rotate(180deg);
            padding: 20px;
            text-align: center;
            font-size: 20px;
        }
        .dataframe td {
            padding: 8px;
        }
        .stDataFrame > div {
            overflow-x: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Apply CSS for dropdown and input styling
st.markdown("""
    <style>
        div[data-baseweb="input"] {
            background-color: #f0f8ff; 
            border: 2px solid #3498db; 
            border-radius: 10px;        
            padding: 5px;
        }
        div[data-baseweb="select"] {
            background-color: #f0f8ff;  
            border: 2px solid #3498db;  
            border-radius: 10px;        
            padding: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# File path for dataset
file_path = "All_merged.xlsx"
file_path2 = "Mouse_summary.xlsx"

# Function to convert an image to Base64
def get_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Load the image and convert to Base64
sidebar_bg_image = get_base64("x2.png")  # Ensure the correct file path

# Apply CSS with inline Base64 image and set text color to white
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-image: url("data:image/png;base64,{sidebar_bg_image}");
            background-size: cover;
            background-position: center;
            color: white !important; /* Ensures all text in the sidebar is white */
        }
        [data-testid="stSidebar"] * {
            color: white !important; /* Applies white color to all elements inside the sidebar */
        }
    </style>
""".format(sidebar_bg_image=sidebar_bg_image), unsafe_allow_html=True)

# === SIDEBAR MENU ===
page = st.sidebar.selectbox("Choose a section", [
    "MAIN", 
    "PROJECT DESCRIPTION", 
    "ALL PROTEINS MERGED-TABLE", 
    "MOUSE DATA", 
    "RAT DATA"
])

# === MAIN PAGE ===
if page == "MAIN":
    logo_path = "logo database.png"
    image = Image.open(logo_path)
    
    orig_width, orig_height = image.size
    new_width = orig_width // 2
    st.image(image, width=new_width)

# === PROJECT DESCRIPTION ===
elif page == "PROJECT DESCRIPTION":
    st.title("Project Description")
    st.write("""
               **Project Overview**

                The aim of this project is to review existing mass spectrometry studies reporting palmitate-enriched proteins in rat and mouse brain tissues to better understand 
                the groups of proteins regulated by this post-translational modification. Since results from different studies vary significantly, we highlight proteins that have been most frequently reported as palmitoylated.
                Additionally, the presented database may serve as a valuable resource for researchers looking for target proteins to study. 
        
                **Key Objectives**

                - Integrate published palmitoylomes obtained via mass spectrometry into a searchable database as a useful research tool.
                - Identify proteins that are consistently reported in their palmitoylated form.
                - Characterize protein families that undergo palmitoylation.

                **Methods**

                - Data Collection: Proteomic analysis results from published studies on brain tissue samples were gathered and merged.
                - Protein Identification: Gene IDs corresponding to palmitoylated proteins were mapped to protein names and key characteristics using the UniProt database.
                - Data Visualization: Tools like Cytoscape and Metascape were used to visualize enriched pathways and analyze protein interactions.

                 **HOW TO USE**

                 - Use left dropdown menu for aggregated data or individual protein data. Tables and graphics in most cases are interactive.
    """)

# === ALL PROTEINS MERGED-TABLE ===
elif page == "ALL PROTEINS MERGED-TABLE":
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("Reports of mass-spectrometry palmitoylated proteins are merged in single database:", df.columns)
    
    filters = {}
    for column in filter_columns:
        unique_values = df[column].dropna().unique()
        selected_values = st.multiselect(f"Filter {column}:", unique_values)
        if selected_values:
            filters[column] = selected_values

    for column, selected_values in filters.items():
        df = df[df[column].isin(selected_values)]

    st.dataframe(df, use_container_width=True)

# === MOUSE DATA ===
elif page == "MOUSE DATA":
    mouse_section = st.sidebar.selectbox("Choose Mouse Data Section", [
        "Data Summary",
        "Metascape Protein Overlap Analysis",
        "Metascape Enriched Ontology Clusters",
        "Metascape Protein-Protein Interaction Network",
        "Interpretation"
    ])

    if mouse_section == "Data Summary":
        st.title("Mouse Data Summary")
        df_mouse = pd.read_excel(file_path2, engine="openpyxl")
        st.dataframe(df_mouse, use_container_width=True)

    elif mouse_section == "Metascape Protein Overlap Analysis":
        st.title("Mouse Metascape Protein Overlap Analysis")

    elif mouse_section == "Metascape Enriched Ontology Clusters":
        st.title("Mouse Metascape Enriched Ontology Clusters")

    elif mouse_section == "Metascape Protein-Protein Interaction Network":
        st.title("Mouse Metascape Protein-Protein Interaction Network")
        st.write("Protein interaction network in mouse data...")

        # GitHub Raw URL for the file
        GITHUB_URL = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/1.xgmml"

        def fetch_xgmml_file(url):
            response = requests.get(url)
            return response.text if response.status_code == 200 else None
        
        xgmml_data = fetch_xgmml_file(GITHUB_URL)
        if xgmml_data:
            st.success("Successfully loaded XGMML file.")

# === RAT DATA ===
elif page == "RAT DATA":
    st.title("Rat Data")
    st.write("Rat data section under development.")

