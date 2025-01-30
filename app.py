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

# === SIDEBAR MENU ===
st.sidebar.title("Menu")

# Dropdown for data-related sections
page = st.sidebar.selectbox("Choose a section", [
    "MAIN", "Data Summary", "Metascape Protein Overlap Analysis",
    "Metascape Enriched Ontology Clusters", "Metascape Protein-Protein Interaction Network", "Interpretation"
])

# === MAIN PAGE (DEFAULT) ===
if page == "MAIN":
    st.title("RAT AND MOUSE COMPARATIVE") 
    st.title("BRAIN TISSUE PALMITOYLOMES")
    logo_path = "Logo2.png"  # Update the path if needed
    st.image(logo_path, use_container_width=False)

# === DATA SUMMARY ===
elif page == "Data Summary":
    st.title("Data Summary")
    st.write("Summary of the palmitoylome data collected for rat and mouse brain tissue...")

# === METASCAPE PROTEIN OVERLAP ANALYSIS ===
elif page == "Metascape Protein Overlap Analysis":
    st.title("Metascape Protein Overlap Analysis")
    st.write("Analysis of overlapping proteins using Metascape...")

# === METASCAPE ENRICHED ONTOLOGY CLUSTERS ===
elif page == "Metascape Enriched Ontology Clusters":
    st.title("Metascape Enriched Ontology Clusters")
    st.write("Functional ontology clusters enriched in palmitoylome dataset...")

# === METASCAPE PROTEIN-PROTEIN INTERACTION NETWORK ===
elif page == "Metascape Protein-Protein Interaction Network":
    st.title("Metascape Protein-Protein Interaction Network")
    st.write("Network analysis of palmitoylated proteins...")
    try:
        img = Image.open("interaction_network.png")
        zoomed_img = image_zoom(img)
        if zoomed_img:
            st.image(zoomed_img, caption="Protein-Protein Interaction Network", use_container_width=True)
    except FileNotFoundError:
        st.error("Image file not found.")

# === INTERPRETATION ===
elif page == "Interpretation":
    st.title("Interpretation")
    st.write("Interpretation of the palmitoylome data in the context of brain function and disease...")

# === ADDITIONAL SECTIONS ===
# STRING Network
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
