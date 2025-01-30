import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image  
import pandas as pd

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
logo_path = "Logo2.png"
st.image(logo_path, use_container_width=False)

# === PROJECT DESCRIPTION MENU ===
project_description = st.sidebar.button("Project Description")

if project_description:
    st.title("Project Description")
    st.write("""
   **Project Overview**
   The aim of this project is to review existing mass spectrometry studies reporting on palmitate-enriched proteins in rat and mouse brain tissues...
    """)

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
