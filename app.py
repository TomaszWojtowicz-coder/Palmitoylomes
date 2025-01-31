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
        h1 { font-size: 30px !important; }  /* Zmień wielkość H1 */
        h2 { font-size: 25px !important; }  /* Opcjonalnie zmień H2 */
        h3 { font-size: 22px !important; }
        h1, h2, h3, h4, h5, h6 { text-indent: 30px; margin-bottom: 60px; background-color: #e9e6fc; color: #3f3f4d; }
        .stSidebar { background-color: #bfbad9 !important; color: white !important; }
        .stButton > button { background-color: #966edb; color: #1F1A3D; }
    </style>
""", unsafe_allow_html=True)

# File path for dataset
file_path = "All_merged.xlsx"
# File path for dataset
file_path2 = "Mouse_summary.xlsx"

# === SIDEBAR MENU ===
#st.sidebar.title("Menu")

# Dropdown for navigation
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
    logo_path = "Logo2.png"  # Update the path if needed
    st.image(logo_path, use_container_width=False)

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
        
        
        st.markdown("""
            <style>
                .dataframe tbody tr th, .dataframe tbody tr td {
                    font-size: 14px;  /* Adjust font size */
                }
            </style>
        """, unsafe_allow_html=True)
        
        
        
        # Title of the Streamlit app
        st.title("Gene Occurrence Analysis")
        
        # Upload the Excel file (adjust path as necessary)
        uploaded_file = "gene_occurrences_analysis_mouse.xlsx"
        df = pd.read_excel(uploaded_file)
        
        # Apply proportional row coloring based on occurrences
        def color_cells(val):
            """Apply background color based on the occurrence value (proportional)."""
            max_val = df.iloc[:, 1:-1].max().max()  # Maximum number of occurrences for scaling
            color_intensity = val / max_val if max_val > 0 else 0  # Scale the color intensity
            # Use a color scale (from white to red)
            color = f"rgba(255, {255 - int(color_intensity * 255)}, {255 - int(color_intensity * 255)}, 1)"
            return f"background-color: {color};"
        
        # Apply the color function to all columns except the "Gene_ID" and "Occurrences"
        styled_df = df.style.applymap(color_cells, subset=df.columns[1:-1])
        
        # Add filter widget to filter by "Gene_ID"
        gene_filter = st.text_input("Filter by Gene ID (partial match)")
        
        # Filter the dataframe based on the input Gene ID filter
        if gene_filter:
            filtered_df = df[df["Gene_ID"].str.contains(gene_filter, case=False, na=False)]
            st.write(f"Filtered results for '{gene_filter}':")
            st.dataframe(filtered_df.style.applymap(color_cells, subset=filtered_df.columns[1:-1]), use_container_width=True)
        else:
            st.write("Displaying full data:")
            st.dataframe(styled_df, use_container_width=True)




    
    


    
    elif mouse_section == "Metascape Protein Overlap Analysis":
        st.title("Mouse Metascape Protein Overlap Analysis")
        st.write("Analysis of overlapping proteins in mouse data using Metascape...")
    
    elif mouse_section == "Metascape Enriched Ontology Clusters":
        st.title("Mouse Metascape Enriched Ontology Clusters")
        st.write("Functional ontology clusters enriched in mouse palmitoylome dataset...")
    
    elif mouse_section == "Metascape Protein-Protein Interaction Network":
        st.title("Mouse Metascape Protein-Protein Interaction Network")
        st.write("Protein interaction network in mouse data...")
        try:
            img = Image.open("interaction_network_mouse.png")
            zoomed_img = image_zoom(img)
            if zoomed_img:
                st.image(zoomed_img, caption="Protein-Protein Interaction Network (Mouse)", use_container_width=True)
        except FileNotFoundError:
            st.error("Image file not found.")
    
    elif mouse_section == "Interpretation":
        st.title("Mouse Data Interpretation")
        st.write("Interpretation of the mouse palmitoylome data...")

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
        st.write("Summary of the palmitoylome data collected for rat brain tissue...")

    
    elif rat_section == "Metascape Protein Overlap Analysis":
        st.title("Rat Metascape Protein Overlap Analysis")
        st.write("Analysis of overlapping proteins in rat data using Metascape...")
    
    elif rat_section == "Metascape Enriched Ontology Clusters":
        st.title("Rat Metascape Enriched Ontology Clusters")
        st.write("Functional ontology clusters enriched in rat palmitoylome dataset...")
    
    elif rat_section == "Metascape Protein-Protein Interaction Network":
        st.title("Rat Metascape Protein-Protein Interaction Network")
        st.write("Protein interaction network in rat data...")
        try:
            img = Image.open("interaction_network_rat.png")
            zoomed_img = image_zoom(img)
            if zoomed_img:
                st.image(zoomed_img, caption="Protein-Protein Interaction Network (Rat)", use_container_width=True)
        except FileNotFoundError:
            st.error("Image file not found.")
    
    elif rat_section == "Interpretation":
        st.title("Rat Data Interpretation")
        st.write("Interpretation of the rat palmitoylome data...")

