import streamlit as st
from PIL import Image
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import requests
import streamlit.components.v1 as components

# Set page layout
st.set_page_config(layout="wide")

# File paths on GitHub
logo_url = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/Logo.jpg"
graphml_url = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/1.graphml"

# Sidebar Menu
page = st.sidebar.selectbox("Choose a section", [
    "MAIN", 
    "PROJECT DESCRIPTION", 
    "ALL PROTEINS MERGED-TABLE", 
    "MOUSE DATA", 
    "RAT DATA"
])

if page == "MAIN":
    st.title("COMPARATIVE DATABASE OF RAT AND MOUSE")
    st.title("BRAIN TISSUE PALMITOYLOMES")
    st.image(logo_url, width=300)
    st.write("Comments: t.wojtowicz AT nencki.edu.pl") 

elif page == "MOUSE DATA":
    mouse_section = st.sidebar.selectbox("Choose Mouse Data Section", [
        "Metascape Protein Overlap Analysis"
    ])

    if mouse_section == "Metascape Protein Overlap Analysis":
        st.title("Mouse Metascape Protein Overlap Analysis")

        try:
            response = requests.get(graphml_url)
            response.raise_for_status()

            # Save file temporarily
            graphml_temp_path = "temp_graph.graphml"
            with open(graphml_temp_path, "wb") as f:
                f.write(response.content)

            # Load and visualize the graph
            G = nx.read_graphml(graphml_temp_path)
            net = Network(notebook=True, height="600px", width="100%", bgcolor="#ffffff", font_color="black")
            net.from_nx(G)

            # Save as HTML
            graph_html_path = "graph_visualization.html"
            net.save_graph(graph_html_path)

            # Display in Streamlit
            with open(graph_html_path, "r", encoding="utf-8") as f:
                components.html(f.read(), height=700)

            st.success("Graph visualization loaded successfully from GitHub!")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to load graph: {e}")
