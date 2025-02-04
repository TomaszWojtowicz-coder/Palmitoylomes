import streamlit as st
from PIL import Image
import pandas as pd
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from streamlit.components.v1 import html

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
        .stSidebar { background-color: #bfbad9 !important; color: white !important; }
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

# File path for datasets
file_path = "All_merged.xlsx"
file_path2 = "Mouse_summary.xlsx"

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
    st.title("COMPARATIVE DATABASE OF RAT AND MOUSE") 
    st.title("BRAIN TISSUE PALMITOYLOMES")
    logo_path = "Logo.jpg"
    image = Image.open(logo_path)
    
    orig_width, orig_height = image.size
    new_width = orig_width // 2
    st.image(image, width=new_width)
    st.write("Comments and suggestions on how to improve database (t.wojtowicz AT nencki.edu.pl)") 

# === PROJECT DESCRIPTION ===
elif page == "PROJECT DESCRIPTION":
    st.title("Project Description")
    st.write("""
               **Project Overview**
               The aim of this project is to review existing mass spectrometry studies reporting on palmitate-enriched proteins in rat and mouse brain tissues to better understand 
               the patterns of protein palmitoylation. 
    """)

# === ALL PROTEINS MERGED-TABLE ===
elif page == "ALL PROTEINS MERGED-TABLE":
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("Reports of mass-spectrometry palmitoylated proteins are merged in a single database", df.columns)
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
        "Metascape - Enriched Terms",
        "Interpretation"
    ])

    if mouse_section == "Data Summary":
        st.title("Mouse Data Summary")
        st.write("""
        List of original publications reporting palmitoylated proteins in mice compared in this study:
        """)
        df_mouse = pd.read_excel(file_path2, engine="openpyxl")
        st.dataframe(df_mouse, use_container_width=True)

    elif mouse_section == "Metascape - enriched terms":
        st.title("Metascape - Enriched Terms")
        st.write("""
        **Description:**  
        Bar graph of enriched terms across input gene lists, colored by p-values.  
        183 mouse palmitoylated proteins found in 6 out of 8 studies.
        """)

        # Display PDF (Alternative method using HTML iframe)
        pdf_file_path = "1. Enrichment_heatmap_HeatmapSelectedGO.pdf"
        
        if os.path.exists(pdf_file_path):
            st.write("**Zoomable PDF View**")
            pdf_embed_code = f"""
            <iframe src="{pdf_file_path}" width="100%" height="600px"></iframe>
            """
            html(pdf_embed_code, height=600)
        else:
            st.error("PDF file not found!")

# === RAT DATA ===
elif page == "RAT DATA":
    rat_section = st.sidebar.selectbox("Choose Rat Data Section", [
        "Data Summary",
        "Metascape Protein Overlap Analysis",
        "Metascape Enriched Ontology Clusters",
        "Metascape Protein-Protein Interaction Network",
        "Interpretation"
    ])

    if rat_section == "Data Summary":
        st.title("Rat Data Summary")
        st.write("Summary of the palmitoylome data collected for rat brain tissue...")
    
    elif rat_section == "Metascape Protein Overlap Analysis":
        st.title("Rat Metascape Protein Overlap Analysis")
        st.write("Analysis of overlapping proteins in rat data using Metascape...")
    
    elif rat_section == "Metascape Protein-Protein Interaction Network":
        st.title("Rat Metascape Protein-Protein Interaction Network")
        st.write("Protein interaction network in rat data...")
        try:
            img = Image.open("interaction_network_rat.png")
            zoomed_img = image_zoom(img)
            st.image(zoomed_img, caption="Protein-Protein Interaction Network (Rat)", use_container_width=True)
        except FileNotFoundError:
            st.error("Image file not found.")

    elif rat_section == "Interpretation":
        st.title("Rat Data Interpretation")
        st.write("Interpretation of the rat palmitoylome data...")
