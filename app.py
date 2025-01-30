import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image
import pandas as pd
import os

# Ustawienie strony na pełną szerokość
st.set_page_config(layout="wide")

# Sidebar menu
st.sidebar.title("Menu")
page = st.sidebar.selectbox("GENERAL INFORMATION", [
    "MAIN", "PROJECT DESCRIPTION", "DATASETS DESCRIPTION", "ALL PROTEINS MERGED-TABLE",
    "Mouse Data", "Rat Data"
])

# Strona główna
if page == "MAIN":
    st.title("RAT AND MOUSE COMPARATIVE")
    st.title("BRAIN TISSUE PALMITOYLOMES")
    logo_path = "Logo2.png"
    st.image(logo_path, use_container_width=False)

elif page == "PROJECT DESCRIPTION":
    st.title("Project Description")
    st.write("""
   **Project Overview**
   
   The aim of this project is to review existing mass spectrometry studies reporting on palmitate-enriched proteins in rat and mouse brain tissues...
   
   **Key Objectives**
   
   - Integrate published palmitoylomes obtained via mass spectrometry into a searchable database as a useful research tool.
   - Identify proteins that are consistently reported in their palmitoylated form.
   - Characterize protein families that undergo palmitoylation.
   
   **Methods**
   - Data Collection: Proteomic analysis results from published studies on brain tissue samples were gathered and merged.
   - Protein Identification: Gene IDs corresponding to palmitoylated proteins were mapped to protein names...
   - Data Visualization: Tools like Cytoscape and Metascape were used to visualize enriched pathways and analyze protein interactions.
    """)

elif page == "ALL PROTEINS MERGED-TABLE":
    df = pd.read_excel("All_merged.xlsx", engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("Filter data:", df.columns)
    filters = {column: st.multiselect(f"Filter {column}:", df[column].dropna().unique()) for column in filter_columns}
    for column, selected_values in filters.items():
        df = df[df[column].isin(selected_values)]
    st.dataframe(df, use_container_width=True)

# Mouse Data
elif page == "Mouse Data":
    subpage = st.sidebar.radio("Mouse Data Sections", [
        "Data Summary", "Metascape Protein Overlap Analysis", "Metascape Enriched Ontology Clusters", 
        "Metascape Protein-protein Interaction Network", "Interpretation"
    ])
    st.title(f"Mouse Data - {subpage}")
    st.write("Content for Mouse Data - " + subpage)

# Rat Data
elif page == "Rat Data":
    subpage = st.sidebar.radio("Rat Data Sections", [
        "Data Summary", "Metascape Protein Overlap Analysis", "Metascape Enriched Ontology Clusters", 
        "Metascape Protein-protein Interaction Network", "Interpretation"
    ])
    st.title(f"Rat Data - {subpage}")
    st.write("Content for Rat Data - " + subpage)
