import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image  
import pandas as pd

# Set page layout
st.set_page_config(layout="wide")

# Sidebar menu
st.sidebar.title("Menu")
page = st.sidebar.selectbox(
    "GENERAL INFORMATION",
    [
        "MAIN", 
        "PROJECT DESCRIPTION", 
        "ALL PROTEINS MERGED-TABLE", 
        "Mouse Data", 
        "Rat Data"
    ]
)

# Main Page
if page == "MAIN":
    st.title("RAT AND MOUSE COMPARATIVE BRAIN TISSUE PALMITOYLOMES")
    logo_path = "Logo2.png"
    st.image(logo_path, use_container_width=False)

# Project Description
elif page == "PROJECT DESCRIPTION":
    st.title("Project Description")
    st.write("""
    **Project Overview**
    
    This project reviews mass spectrometry studies on palmitate-enriched proteins in rat and mouse brain tissues. 
    The goal is to identify protein families regulated by palmitoylation and compile a useful database for researchers.
    """)

# Datasets Description
elif page == "ALL PROTEINS MERGED-TABLE":
    file_path = "All_merged.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("All Reported Palmitoylated Proteins")
    filter_columns = st.multiselect("Filter Data:", df.columns)
    
    filters = {col: st.multiselect(f"Select values for {col}:", df[col].dropna().unique()) for col in filter_columns}
    for col, values in filters.items():
        if values:
            df = df[df[col].isin(values)]

    st.dataframe(df, use_container_width=True)

# Mouse Data
elif page == "Mouse Data":
    st.title("Mouse Data")

    mouse_section = st.radio("Select Analysis:", [
        "Data Summary",
        "Metascape Protein Overlap Analysis",
        "Metascape Enriched Ontology Clusters",
        "Metascape Protein-protein Interaction Network",
        "Interpretation"
    ])

    if mouse_section == "Data Summary":
        st.write("Summary of palmitoylated proteins found in mouse brain tissue.")
    elif mouse_section == "Metascape Protein Overlap Analysis":
        st.write("Analysis of overlapping proteins in mouse data.")
    elif mouse_section == "Metascape Enriched Ontology Clusters":
        st.write("Functional clusters enriched in mouse proteins.")
    elif mouse_section == "Metascape Protein-protein Interaction Network":
        st.write("Network analysis of protein-protein interactions in mouse data.")
    elif mouse_section == "Interpretation":
        st.write("Biological interpretation of mouse palmitoylome findings.")

# Rat Data
elif page == "Rat Data":
    st.title("Rat Data")

    rat_section = st.radio("Select Analysis:", [
        "Data Summary",
        "Metascape Protein Overlap Analysis",
        "Metascape Enriched Ontology Clusters",
        "Metascape Protein-protein Interaction Network",
        "Interpretation"
    ])

    if rat_section == "Data Summary":
        st.write("Summary of palmitoylated proteins found in rat brain tissue.")
    elif rat_section == "Metascape Protein Overlap Analysis":
        st.write("Analysis of overlapping proteins in rat data.")
    elif rat_section == "Metascape Enriched Ontology Clusters":
        st.write("Functional clusters enriched in rat proteins.")
    elif rat_section == "Metascape Protein-protein Interaction Network":
        st.write("Network analysis of protein-protein interactions in rat data.")
    elif rat_section == "Interpretation":
        st.write("Biological interpretation of rat palmitoylome findings.")
