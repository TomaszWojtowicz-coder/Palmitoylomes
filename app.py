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

                The aim of this project is to review existing mass spectrometry studies reporting on palmitate-enriched proteins in rat and mouse brain tissues to better understand 
                the patterns of protein palmitoylation. Since results from different studies vary significantly, we highlight proteins that have been most frequently reported as palmitoylated.
                By compiling these findings, we hope to improve the understanding of which protein families are regulated by this specific post-translational modification. Additionally, 
                the presented database may serve as a valuable resource for researchers looking for target proteins to study. 
        
                **Key Objectives**

                - Integrate published palmitoylomes obtained via mass spectrometry into a searchable database as a useful research tool.
                - Identify proteins that are consistently reported in their palmitoylated form.
                - Characterize protein families that undergo palmitoylation.

                **Methods**

                - Data Collection: Proteomic analysis results from published studies on brain tissue samples were gathered and merged.
                - Protein Identification: Gene IDs corresponding to palmitoylated proteins were mapped to protein names and key characteristics using the UniProt database.
                - Data Visualization: Tools like Cytoscape and Metascape were used to visualize enriched pathways and analyze protein interactions.

                 **HOW TO USE**

                 - Use left dropdown menu to search for protein of interest or results of analysis
    """)

# === ALL PROTEINS MERGED-TABLE ===
elif page == "ALL PROTEINS MERGED-TABLE":
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("Reports of mass-spectrometry palmitoylated proteins are merged in single database (mouse data n=8 studies, rat data n=3 studies). Multifilter of data can be applied:", df.columns)  # Limit to 8
    filters = {}
    for column in filter_columns:
        unique_values = df[column].dropna().unique()  # Get unique values
        selected_values = st.multiselect(f"Filter {column}:", unique_values)  # Allow selection
        if selected_values:
            filters[column] = selected_values  # Store selections

    for column, selected_values in filters.items():
        df = df[df[column].isin(selected_values)]

    st.dataframe(df, use_container_width=True)

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
        st.write("""
        
        List of original publications reporting palmitoylated proteins in mice compared in this study:
        
        """)
        df_mouse = pd.read_excel(file_path2, engine="openpyxl")
        st.dataframe(df_mouse, use_container_width=True)
        

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
            
            # Load the data
            uploaded_file = "gene_occurrences_analysis_mouse.xlsx"
            df = load_data(uploaded_file)
            
            # Ensure Protein Name stays horizontal
            df_styled = df.style.set_table_styles(
                [
                    {'selector': 'th',
                     'props': [('writing-mode', 'vertical-rl'), ('transform', 'rotate(180deg)'), ('text-align', 'center'), ('padding', '10px')]},
                    {'selector': 'th:nth-child(2)',  # Second column (Protein name)
                     'props': [('writing-mode', 'horizontal-tb'), ('transform', 'none'), ('text-align', 'center')]}
                ]
            )
            
            st.dataframe(df_styled, use_container_width=True)


            # Mark as loaded (removes the blinking "RUNNING" text)
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

    elif mouse_section == "Metascape Protein Overlap Analysis":
        st.title("Mouse Metascape Protein Overlap Analysis")
        st.write("Analysis of overlapping proteins in mouse data using Metascape...")
    
    elif mouse_section == "Metascape Enriched Ontology Clusters":
        st.title("Mouse Metascape Enriched Ontology Clusters")
        st.write("Functional ontology clusters enriched in mouse palmitoylome dataset...")
    
    elif mouse_section == "Metascape Protein-Protein Interaction Network":
        st.title("Mouse Metascape Protein-Protein Interaction Network")
        st.write("Protein interaction network in mouse data...")
                
        
        # Function to Load and Display Cytoscape.js Network
        def display_cytoscape_network(cyjs_data):
            # Check if the cyjs_data has elements
            if 'elements' not in cyjs_data or len(cyjs_data['elements']) == 0:
                st.error("The CYJS data doesn't contain valid elements.")
                return
            
            # Display the data for debugging purposes
            st.json(cyjs_data['elements'][0])  # Display the first element for inspection
        
            # HTML and JS code for Cytoscape
            st.components.v1.html(f"""
                <html>
                <head>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.0/cytoscape.min.js"></script>
                    <style>
                        #cy {{
                            width: 100%;
                            height: 600px;
                            border: 1px solid black;
                        }}
                    </style>
                </head>
                <body>
                    <div id="cy"></div>
                    <script>
                        var cy = cytoscape({{
                            container: document.getElementById('cy'),
                            elements: {json.dumps(cyjs_data['elements'])},  // Use the elements from the loaded data
                            style: [
                                {{
                                    selector: 'node',
                                    style: {{
                                        'background-color': '#6fa3ef',
                                        'label': 'data(name)',
                                        'font-size': '12px',
                                        'text-valign': 'center',
                                        'text-halign': 'center'
                                    }}
                                }},
                                {{
                                    selector: 'edge',
                                    style: {{
                                        'width': 2,
                                        'line-color': '#ddd',
                                        'target-arrow-color': '#ddd',
                                        'target-arrow-shape': 'triangle'
                                    }}
                                }}
                            ],
                            layout: {{
                                name: 'cose'  // Adjust layout: 'cose', 'circle', 'grid', 'breadthfirst'
                            }}
                        }});
                    </script>
                </body>
                </html>
            """, height=650)
        
        # Streamlit App to display Cytoscape.js network
        st.title("Interactive Cytoscape.js Network")
        
        # GitHub URL to load the 1.cyjs file
        github_url = "https://raw.githubusercontent.com/TomaszWojtowicz-coder/Palmitoylomes/main/1.cyjs"
        
        try:
            response = requests.get(github_url)
            response.raise_for_status()  # Ensure the request was successful
            cyjs_data = response.json()  # Parse the JSON from the URL
            display_cytoscape_network(cyjs_data)  # Display Cytoscape network
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading CYJS file: {e}")
        except json.JSONDecodeError:
            st.error("Failed to decode JSON. Ensure the CYJS file is correctly formatted.")
