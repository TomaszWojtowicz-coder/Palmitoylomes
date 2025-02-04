import streamlit as st
from PIL import Image
import pandas as pd
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import requests
import networkx as nx
from pyvis.network import Network
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

# === FUNCTION TO LOAD GRAPHML AND DISPLAY IN PYVIS ===
def load_graph(graphml_url):
    try:
        response = requests.get(graphml_url)
        response.raise_for_status()

        # Save the downloaded file temporarily
        graphml_temp_path = "temp_graph.graphml"
        with open(graphml_temp_path, "wb") as f:
            f.write(response.content)

        # Load the graph using NetworkX
        G = nx.read_graphml(graphml_temp_path)

        # Convert NetworkX graph to PyVis
        net = Network(notebook=True, height="600px", width="100%", bgcolor="#ffffff", font_color="black")

        # Manually add nodes
        for node in G.nodes():
            net.add_node(node, label=str(node))

        # Manually add edges (ignore attributes to avoid errors)
        for edge in G.edges():
            net.add_edge(edge[0], edge[1])

        # Save graph as an HTML file
        graph_html_path = "graph_visualization.html"
        net.save_graph(graph_html_path)

        # Embed the HTML in Streamlit
        with open(graph_html_path, "r", encoding="utf-8") as f:
            html(f.read(), height=700)

        st.success("Graph visualization loaded successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load graph: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

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
        The aim of this project is to review existing mass spectrometry studies reporting on palmitate-enriched proteins in rat and mouse brain tissues.
    """)

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
        st.write("Visualizing the protein interaction network for mouse data...")
        
        # Load graph from GitHub (REPLACE with actual URL)
        graphml_url = "https://github.com/YOUR-REPO/mouse_graph.graphml"
        load_graph(graphml_url)

    elif mouse_section == "Interpretation":
        st.title("Mouse Data Interpretation")

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

    elif rat_section == "Metascape Protein Overlap Analysis":
        st.title("Rat Metascape Protein Overlap Analysis")

    elif rat_section == "Metascape Enriched Ontology Clusters":
        st.title("Rat Metascape Enriched Ontology Clusters")

    elif rat_section == "Metascape Protein-Protein Interaction Network":
        st.title("Rat Metascape Protein-Protein Interaction Network")
        st.write("Visualizing the protein interaction network for rat data...")

        # Load graph from GitHub (REPLACE with actual URL)
        graphml_url = "https://github.com/YOUR-REPO/rat_graph.graphml"
        load_graph(graphml_url)

    elif rat_section == "Interpretation":
        st.title("Rat Data Interpretation")
