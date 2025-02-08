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
from io import BytesIO


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
st.markdown(f"""
    <style>
        [data-testid="stSidebar"] {{
            background-image: url("data:image/png;base64,{sidebar_bg_image}");
            background-size: cover;
            background-position: center;
            color: white !important; /* Ensures all text in the sidebar is white */
        }}
        [data-testid="stSidebar"] * {{
            color: white !important; /* Applies white color to all elements inside the sidebar */
        }}
    </style>
""", unsafe_allow_html=True)



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


                 ** **
                 ** **
                 Comments, suggestions, should be sent to (t.wojtowicz AT nencki.edu.pl)
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
        "Mouse common protein table", 
        "Metascape Mouse palmitoylome",
        "ShinyGO Mouse palmitoylome",
       

    ])

    if mouse_section == "Data Summary":
        st.title("Mouse Data Summary")
        st.write("""
        
        List of original publications reporting palmitoylated proteins in mice compared in this study:
        
        """)
        df_mouse = pd.read_excel(file_path2, engine="openpyxl")
        st.dataframe(df_mouse, use_container_width=True)
    

    if mouse_section == "Mouse common protein table":
        # Title of the Streamlit app
        st.title("Gene Occurrence Analysis")


        # Show "LOADING" blinking icon while loading
        with st.status("Loading data...", expanded=True) as status:
            st.markdown("""
                <style>
                    @keyframes blink {
                        0% { color: red; }
                        50% { color: transparent; }
                        100% { color: red; }
                    }
                    
                    .blinking-text {
                        font-size: 24px;
                        font-weight: bold;
                        color: red;
                        animation: blink 1s infinite;
                    }
                    
                    .blinking-text-wrapper {
                        text-align: center;
                        margin-top: 10px;
                    }
                </style>
                
                <div class="blinking-text-wrapper">
                    <span class="blinking-text">LOADING</span>
                </div>
            """, unsafe_allow_html=True)
        
            # Simulate loading delay (for testing purposes)
           # time.sleep(10)




        @st.cache_data
        def load_data(uploaded_file):
            df = pd.read_excel(uploaded_file, engine="openpyxl", header=0)
            df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
            return df
        # Show "LOADING" blinking icon while loading
        with st.status("Loading data...", expanded=True) as status:
            st.markdown("""
                <style>
                    @keyframes blink {
                        0% { color: red; }
                        50% { color: transparent; }
                        100% { color: red; }
                    }
                    
                    .blinking-text {
                        font-size: 24px;
                        font-weight: bold;
                        color: red;
                        animation: blink 1s infinite;
                    }
                    
                    .blinking-text-wrapper {
                        text-align: center;
                        margin-top: 10px;
                    }
                </style>
                
                <div class="blinking-text-wrapper">
                    <span class="blinking-text">LOADING</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Simulate loading delay (for testing purposes)
            # time.sleep(10)
        
            # Load the data (call the function)
            uploaded_file = "gene_occurrences_analysis_mouse.xlsx"
            df = load_data(uploaded_file)
        
            # Mark as loaded
            status.update(label="Data will be shown in a moment!", state="complete", expanded=False)





        
        # Apply FIRE color scheme: We will use a scale from yellow to red
        def row_color(val):
            """Color the rows based on the number of reports (Fire heatmap)."""
            if isinstance(val, (int, float)) and 1 <= val <= 8:
                # Create color intensity based on the occurrence value
                color_intensity = val / 8  # Scale the color intensity from 1 to 8
                # Fire-like color gradient from yellow to red (R->G->B)
                r = int(255 - color_intensity * 255)
                g = int(255 - color_intensity * 255)
                b = 255
                color = f"rgb({r}, {g}, {b})"
                return [f"background-color: {color}"] * len(df.columns)  # Apply color to all columns in the row
            return [""] * len(df.columns)

        # Filter by Gene ID
        gene_filter = st.text_input("Filter by Gene ID (partial match)")
        
        # Apply filter
        if gene_filter:
            filtered_df = df[df["Gene_ID"].str.contains(gene_filter, case=False, na=False)]
        else:
            filtered_df = df
        
        # Apply the color scheme to the dataframe
        styled_df = filtered_df.style.apply(lambda row: row_color(row['Sum Reports']), axis=1)
        
        # Convert the dataframe to an HTML table with rotated column names
        html_table = filtered_df.to_html(classes='dataframe', index=False)
        
        # Apply custom CSS to rotate column headers 90 degrees
        st.markdown("""
            <style>
                .dataframe th {
                    writing-mode: vertical-rl;
                    transform: rotate(180deg);
                    padding: 10px;
                    text-align: center;
                    font-size: 14px;  /* Adjust size to fit better */
                }
                .dataframe td {
                    padding: 8px;
                }
                .stDataFrame > div {
                    overflow-x: auto;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Display the customized HTML table
        st.markdown(html_table, unsafe_allow_html=True)






    
################################################################################################################################################################################################################
    
    if mouse_section == "Metascape Mouse palmitoylome":
        # GitHub Raw URL of your image
        GITHUB_IMAGE_URL = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/1_MOUSE_Go_Network.png"
                
              
        # 📌 Display Title
        st.title("Mouse palmitoylome - proteins common across multiple publications.")
        st.write("" "")
        st.write("""   Analysis of 184 palmitoylated proteins common in at least 6 out of 8 (75%) publications (see Data Summary for reference).""")
        st.write("" "")
        st.write("""1. Metascape - Network of enriched terms colored by cluster, where nodes that share the same cluster are typically close to each other.
                        Size of the node is proportional to the number of proteins associated with biological term / pathway. 
            """)
            
    
    # ✅ Fetch and Display High-Resolution Image
    try:
        response = requests.get(GITHUB_IMAGE_URL, timeout=10)  # Prevent long waits
        response.raise_for_status()  # Check if URL is valid (200 OK)
    
        # Open the image
        image = Image.open(BytesIO(response.content))
    
        # 🔍 Fix resolution: Increase DPI & enhance quality
        high_res_image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)  # 2x scaling
        
        # 📌 Display only the high-resolution image (NO ZOOM)
        st.image(high_res_image, use_container_width=True)  # ✅ Updated parameter
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error loading image: {e}")


  # 📌 Display Title
    st.write("2. Metascape - Bar graph of enriched terms across input gene lists, colored by p-values.")
  
    # 📌 GitHub Raw PDF URL
    GITHUB_PDF_URL2 = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/2_Enrichment_heatmap_HeatmapSelectedGO.png"  # Replace with your actual URL
    try:
        response = requests.get(GITHUB_PDF_URL2, timeout=10)  # Prevent long waits
        response.raise_for_status()  # Check if URL is valid (200 OK)
    
        # Open the image
        image = Image.open(BytesIO(response.content))
    
        image = image.convert("RGBA")  # Keep original quality
        st.image(image, use_container_width=True)  # Display without modification
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error loading image: {e}")


  # 📌 Display Title
    st.write("3. Metascape - Protein-protein interaction network according to Molecular Complex Detection (MCODE). Algorithm identified densely connected network components.")
  
    # 📌 GitHub Raw PDF URL
    GITHUB_3 = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/3_MCODE.png"  # Replace with your actual URL
    try:
        response = requests.get(GITHUB_3, timeout=10)  # Prevent long waits
        response.raise_for_status()  # Check if URL is valid (200 OK)
    
        # Open the image
        image = Image.open(BytesIO(response.content))
    
        image = image.convert("RGBA")  # Keep original quality
        st.image(image, use_container_width=True)  # Display without modification
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error loading image: {e}")
  
  
    
    # 📌 GitHub Raw Image URL for legend table
    GITHUB_4 = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/3_legend_table.png"
    
    try:
        response = requests.get(GITHUB_4, timeout=10)
        response.raise_for_status()
    
        # Open and convert the image
        legend_table = Image.open(BytesIO(response.content)).convert("RGBA")  
        st.image(legend_table, use_container_width=True)
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error loading legend table image: {e}")
          
################################################################################################################################################################################################################
    if mouse_section == "ShinyGO Mouse palmitoylome":        
      # 📌 Display Title
        st.write("3. Metascape - Protein-protein interaction network according to Molecular Complex Detection (MCODE). Algorithm identified densely connected network components.")
      
        # 📌 GitHub Raw PDF URL
        GITHUB_3 = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/3_MCODE.png"  # Replace with your actual URL
        try:
            response = requests.get(GITHUB_3, timeout=10)  # Prevent long waits
            response.raise_for_status()  # Check if URL is valid (200 OK)
        
            # Open the image
            image = Image.open(BytesIO(response.content))
        
            image = image.convert("RGBA")  # Keep original quality
            st.image(image, use_container_width=True)  # Display without modification
        
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error loading image: {e}")
  
  
# === RAT DATA ===
elif page == "RAT DATA":
    st.title("Rat Data")
    st.write("Rat data section under development.")

