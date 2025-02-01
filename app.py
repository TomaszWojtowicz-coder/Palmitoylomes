import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image
import pandas as pd
import os
import time  

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
        .dataframe th:nth-child(2) {
            writing-mode: horizontal-tb !important;
            transform: none !important;
        }
        .dataframe td {
            padding: 8px;
        }
        .stDataFrame > div {
            overflow-x: auto;
        }
    </style>
""", unsafe_allow_html=True)

# File path for dataset
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

# === ALL PROTEINS MERGED-TABLE ===
if page == "ALL PROTEINS MERGED-TABLE":
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("Reports of mass-spectrometry palmitoylated proteins are merged in single database (mouse data n=8 studies, rat data n=3 studies). Multifilter of data can be applied:", df.columns)
    
    filters = {}
    for column in filter_columns:
        unique_values = df[column].dropna().unique()
        selected_values = st.multiselect(f"Filter {column}:", unique_values)
        if selected_values:
            filters[column] = selected_values

    for column, selected_values in filters.items():
        df = df[df[column].isin(selected_values)]

    st.dataframe(df, use_container_width=True)

# === MOUSE DATA (Gene Occurrence Table) ===
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
        st.write("List of original publications reporting palmitoylated proteins in mice compared in this study:")

        df_mouse = pd.read_excel(file_path2, engine="openpyxl")
        st.dataframe(df_mouse, use_container_width=True)

        # Load gene occurrence data
        @st.cache_data
        def load_data(uploaded_file):
            df = pd.read_excel(uploaded_file, engine="openpyxl", header=0)
            df.columns = df.columns.str.strip()
            return df
        
        uploaded_file = "gene_occurrences_analysis_mouse.xlsx"
        df = load_data(uploaded_file)
        
        # Ensure second column (Protein Name) remains horizontal
        df_styled = df.style.set_table_styles([
            {'selector': 'th',
             'props': [('writing-mode', 'vertical-rl'), ('transform', 'rotate(180deg)'), ('text-align', 'center'), ('padding', '10px')]},
            {'selector': 'th:nth-child(2)',  # Second column (Protein name)
             'props': [('writing-mode', 'horizontal-tb'), ('transform', 'none'), ('text-align', 'center')]}
        ])
        
        st.dataframe(df_styled, use_container_width=True)
