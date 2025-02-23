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
file_path5 = "Mouse_summary.xlsx"
file_path21 = "Rat_summary.xlsx"

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
           
        }}

        /* Ensure only the "Choose a section" text is white */
        section[data-testid="stSidebar"] label {{
            color: white !important;
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

    
    logo_path2 = "NCN.png"
    image2 = Image.open(logo_path2)
    
    # Create two columns: one for the logo, one for the text
    col1, col2 = st.columns([1, 3])  # Adjust ratio as needed
    
    with col1:
        # Display the logo
        st.image(image2)
    
    with col2:
        # Display the text next to the logo
        st.markdown(
            """
            **Project financed by Polish National Science Centre grant 2019/34/E/NZ4/00387**
            """
        )

# === PROJECT DESCRIPTION ===
elif page == "PROJECT DESCRIPTION":
    st.title("Project Description")
    logo_path3 = "Palm.png"
    image3 = Image.open(logo_path3)
    
    # Create two columns: one for the logo, one for the text
    col1, col2 = st.columns([1, 3])  # Adjust ratio as needed
    
    with col1:
        # Display the logo
        st.image(image3)
    
    with col2:
        # Display the text next to the logo
        st.markdown(
            """
            <style>
            .text-container {
                width: 100%;  /* Makes the width dynamic */
                max-width: 10%;  /* Ensures text is not too wide */
                text-align: justify;
                font-size: 16px;
                margin: auto;  /* Centers the text */
                padding: 10px; /* Adds slight spacing */
                word-wrap: break-word; /* Ensures long words wrap properly */
                margin-top: 30px; /* Adds space above the text */
            }
    
            @media (min-width: 768px) {
                .text-container {
                    max-width: 100%;  /* More narrow on larger screens */
                }
            }
    
            @media (min-width: 1024px) {
                .text-container {
                    max-width: 100%;  /* Even more narrow for big screens */
                }
            }
            </style>
    
            <div class="text-container">
                <p>
                Protein lipidation is a widely occurring post-translational modification that significantly impacts human physiology and disease processes. 
                One specific type, S-palmitoylation, involves attaching a 16-carbon fatty acid (palmitate) to proteins. This dynamic and reversible modification 
                influences protein stability and trafficking within the membrane. 
                Recent experimental studies suggest that S-palmitoylation acts as a precise molecular switch, rapidly modulating protein functions and 
                subcellular localization over minutes to hours. 
                Neural tissue, in particular, contains a high concentration of proteins regulated by this modification. 
                Advances in high-resolution detection techniques have greatly enhanced our understanding of the role of protein palmitoylation in brain function and dysfunction.
                The zinc finger DHHC (ZDHHC) domain-containing protein family is the main group of enzymes responsible for catalyzing protein S-palmitoylation, and 23 members have been identified in mammalian cells.
                Deacylation is catalyzed by palmitoyl-protein thioesterases (PPTs) such as palmitoyl-protein thioesterase 1 and 2 (PPT1/2), acyl-protein thioesterases APT1/2 and alpha/beta hydrolase domain-containing proteins 10 and 19 (ABHDs).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    
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
    - **Data Collection**: Proteomic analysis results from published studies on brain tissue samples were gathered and merged.  
    - **Protein Identification**: Gene IDs corresponding to palmitoylated proteins were mapped to protein names and key characteristics using the UniProt database.  
    - **Data Visualization**: Tools like Cytoscape and Metascape were used to visualize enriched pathways and analyze protein interactions.  
    
    **HOW TO USE**  
    - Use the left dropdown menu for aggregated data or individual protein data. Tables and graphics in most cases are interactive.  
    """)
    
    st.write("")  
    st.write("**Comments, suggestions:**")  # Bold header for clarity
    
    # Load and display the logo in a column
    logo_path4 = "Nencki.jpg"
    image4 = Image.open(logo_path4)
    
    # Create two columns: one for the logo, one for the text
    col1, col2 = st.columns([1, 3])  # Adjust ratio as needed
    
    with col1:
        st.image(image4)  # Display logo once
    
    with col2:
        st.write("")
        st.write("T. Wojtowicz, Nencki Institute of Experimental Biology, Polish Academy of Sciences  (t.wojtowicz AT nencki.edu.pl)")
        st.write("A. Pytys, Nencki Institute of Experimental Biology, Polish Academy of Sciences  (a.pytys AT nencki.edu.pl)")


# === ALL PROTEINS MERGED-TABLE ===
elif page == "ALL PROTEINS MERGED-TABLE":
    st.title("List of original publications reporting palmitoylated proteins compared in this study")
    st.write("""
    
        Mouse studies:

    """)
    
    file_path5
    df_mouse2 = pd.read_excel(file_path5, engine="openpyxl")
    st.dataframe(df_mouse2, use_container_width=True)

    st.write("""
        
        Rat studies:
        
    """)
    
    df_rat = pd.read_excel(file_path21, engine="openpyxl")
    st.dataframe(df_rat, use_container_width=True)

    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("Reports of mass-spectrometry palmitoylated proteins are merged in single database. Use filter to search protein of interest.", df.columns)
    
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
        "Publications list",
        "Mouse common protein table", 
        "Metascape Mouse palmitoylome",
        "ShinyGO Mouse palmitoylome",
       

    ])

    if mouse_section == "Publications list":
        st.title("List of original publications reporting palmitoylated proteins in mice compared in this study")
       
        df_mouse = pd.read_excel(file_path2, engine="openpyxl")
        st.dataframe(df_mouse, use_container_width=True)
    
    if mouse_section == "Mouse common protein table":
        # Title of the Streamlit app
        st.title("Gene Occurrence Analysis")


 

        @st.cache_data
        def load_data(uploaded_file):
            df = pd.read_excel(uploaded_file, engine="openpyxl", header=0)
            df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
            return df

            # Load the data (call the function)
            uploaded_file = "gene_occurrences_analysis_mouse.xlsx"
            df = load_data(uploaded_file)
        
       
  
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
                
              
        # 📌 Display Title
        st.title("Mouse palmitoylome - proteins common across multiple publications.")
        st.write("" "")
        st.write("""   Analysis of 184 palmitoylated proteins common in at least 6 out of 8 (75%) publications (see Data Summary for reference).""")
        st.write("" "")
        st.write("""1. Metascape - Network of enriched terms colored by cluster, where nodes that share the same cluster are typically close to each other.
                        Size of the node is proportional to the number of proteins associated with biological term / pathway. 
            """)
        imagex = Image.open("1_MOUSE_Go_Network.png")  # Replace with an actual file
        st.image(imagex, use_container_width=True)


  



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
        st.title("Mouse palmitoylome - proteins common across multiple publications analyzed with ShinyGo (https://bioinformatics.sdstate.edu/go/)")
        st.write(" " )
        st.write("1. Enrichment in Gene Ontology terms")
      
        # 📌 GitHub Raw PDF URL
        Gene_Ontology_Mouse_1 = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/Gene_Ontology_Mouse_1.png"
        try:
            response = requests.get(Gene_Ontology_Mouse_1, timeout=10)  # Prevent long waits
            response.raise_for_status()  # Check if URL is valid (200 OK)
        
            # Open the image
            image = Image.open(BytesIO(response.content))
        
            image = image.convert("RGBA")  # Keep original quality
            st.image(image, use_container_width=True)  # Display without modification
        
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error loading image: {e}")
            
        # 📌 Hierarchical clustering tree
        st.write("2. A hierarchical clustering tree summarizes the correlation among significant pathways listed in the Enrichment tab. Pathways with many shared protein ID are clustered together. Bigger dots indicate more significant P-values.")
      
        Gene_Ontology_Mouse_2 = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/Gene_Ontology_Mouse_2.png"
        try:
            response = requests.get(Gene_Ontology_Mouse_2, timeout=10)  # Prevent long waits
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

