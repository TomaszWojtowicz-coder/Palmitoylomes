import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image
import pandas as pd
import os

# Set page layout
st.set_page_config(layout="wide")

# CSS Styling
st.markdown("""
    <style>
        body, .stApp { background-color: #ffffff; color: #3f3f4d; }
        h1, h2, h3, h4, h5, h6 { text-indent: 30px; margin-bottom: 60px; background-color: #e9e6fc; color: #3f3f4d; }
        .stSidebar { background-color: #bfbad9 !important; color: white !important; }
        .stButton > button { background-color: #966edb; color: #1F1A3D; }
    </style>
""", unsafe_allow_html=True)

# File path for dataset
file_path = "All_merged.xlsx"

# === MAIN PAGE (DEFAULT) ===
st.title("RAT AND MOUSE COMPARATIVE") 
st.title("BRAIN TISSUE PALMITOYLOMES")
logo_path = "Logo2.png"  # Update the path if needed
st.image(logo_path, use_container_width=False)

# === SIDEBAR MENU ===
st.sidebar.title("Menu")

# PROJECT DESCRIPTION
project_menu = st.sidebar.selectbox("Project Description", ["", "Overview & Methods", "All Proteins Merged - Table"])

if project_menu == "Overview & Methods":
    st.title("Project Description")
    st.write("""
   **Project Overview**
   The aim of this project is to review existing mass spectrometry studies reporting on palmitate-enriched proteins in rat and mouse brain tissues...
    """)

elif project_menu == "All Proteins Merged - Table":
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("All reported palmitoylated proteins merged in a single database. Use multifilter to filter data:", df.columns)
    filters = {}
    for column in filter_columns:
        unique_values = df[column].dropna().unique()
        selected_values = st.multiselect(f"Filter {column}:", unique_values)
        if selected_values:
            filters[column] = selected_values

    for column, selected_values in filters.items():
        df = df[df[column].isin(selected_values)]

    st.dataframe(df, use_container_width=True)

# === MOUSE DATA MENU ===
mouse_menu = st.sidebar.selectbox("Mouse Data", [
    "", "Data Summary", "Metascape Protein Overlap Analysis",
    "Metascape Enriched Ontology Clusters", "Metascape Protein-Protein Interaction Network", "Interpretation"
])

if mouse_menu == "Data Summary":
    st.title("Mouse Data - Summary")
    st.write("Summary of the palmitoylome data collected for mouse brain tissue...")

elif mouse_menu == "Metascape Protein Overlap Analysis":
    st.title("Mouse Data - Metascape Protein Overlap Analysis")
    st.write("Analysis of overlapping proteins using Metascape...")

elif mouse_menu == "Metascape Enriched Ontology Clusters":
    st.title("Mouse Data - Metascape Enriched Ontology Clusters")
    st.write("Functional ontology clusters enriched in mouse palmitoylome dataset...")

elif mouse_menu == "Metascape Protein-Protein Interaction Network":
    st.title("Mouse Data - Protein-Protein Interaction Network")
    st.write("Network analysis of palmitoylated proteins in mouse brain tissue...")
    try:
        img = Image.open("mouse_interaction_network.png")
        zoomed_img = image_zoom(img)
        if zoomed_img:
            st.image(zoomed_img, caption="Mouse Protein-Protein Interaction Network", use_container_width=True)
    except FileNotFoundError:
        st.error("Image file not found.")

elif mouse_menu == "Interpretation":
    st.title("Mouse Data - Interpretation")
    st.write("Interpretation of mouse palmitoylome data in the context of brain function and disease...")

# === RAT DATA MENU ===
rat_menu = st.sidebar.selectbox("Rat Data", [
    "", "Data Summary", "Metascape Protein Overlap Analysis",
    "Metascape Enriched Ontology Clusters", "Metascape Protein-Protein Interaction Network", "Interpretation"
])

if rat_menu == "Data Summary":
    st.title("Rat Data - Summary")
    st.write("Summary of the palmitoylome data collected for rat brain tissue...")

elif rat_menu == "Metascape Protein Overlap Analysis":
    st.title("Rat Data - Metascape Protein Overlap Analysis")
    st.write("Analysis of overlapping proteins using Metascape...")

elif rat_menu == "Metascape Enriched Ontology Clusters":
    st.title("Rat Data - Metascape Enriched Ontology Clusters")
    st.write("Functional ontology clusters enriched in rat palmitoylome dataset...")

elif rat_menu == "Metascape Protein-Protein Interaction Network":
    st.title("Rat Data - Protein-Protein Interaction Network")
    st.write("Network analysis of palmitoylated proteins in rat brain tissue...")
    try:
        img = Image.open("rat_interaction_network.png")
        zoomed_img = image_zoom(img)
        if zoomed_img:
            st.image(zoomed_img, caption="Rat Protein-Protein Interaction Network", use_container_width=True)
    except FileNotFoundError:
        st.error("Image file not found.")

elif rat_menu == "Interpretation":
    st.title("Rat Data - Interpretation")
    st.write("Interpretation of rat palmitoylome data in the context of brain function and disease...")

# === ADDITIONAL SECTIONS ===
# STRING Network
st.sidebar.markdown("---")
if st.sidebar.button("STRING Network"):
    st.title("STRING Network")
    try:
        img_path = "STRING network - 2--clustered.png"
        img = Image.open(img_path)
        zoomed_img = image_zoom(img)
        if zoomed_img:
            st.image(zoomed_img, caption="STRING Network Visualization (Zoomed)", use_container_width=True)
    except FileNotFoundError:
        st.error(f"File not found: {img_path}. Ensure the file exists.")

# Cytoscape
if st.sidebar.button("Cytoscape"):
    st.title("Cytoscape Network")
    st.write("Download the .cys file for visualization in Cytoscape:")
    try:
        with open("Enrichment_GO_GONetwork.cys", "rb") as cys_file:
            st.download_button(label="Download Cytoscape File (.cys)",
                               data=cys_file,
                               file_name="Enrichment_GO_GONetwork.cys",
                               mime="application/octet-stream")
    except FileNotFoundError:
        st.error("Cytoscape file not found. Make sure it has been uploaded.")

# Metascape
if st.sidebar.button("Metascape"):
    st.title("Metascape Visualization")
    st.markdown("[OPEN Metascape Visualization](https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/)")
    st.write("Or view a preview here:")
    st.components.v1.iframe(
        "https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/",
        height=800,
        width="100%",
        scrolling=True
    )
