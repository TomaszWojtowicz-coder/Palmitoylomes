import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image  # Importujemy bibliotekę PIL
import pandas as pd
import os


# Ustawienie strony na pełną szerokość
st.set_page_config(layout="wide")

# CSS for dark theme with updated text size, color (gold), and sidebar color
st.markdown("""
    <style>
        /* Zmiana ogólnych ustawień tła aplikacji */
        body, .stApp {
            background-color: #ffffff;  /* Tło całej strony na czarne */
            color: white;  /* Kolor czcionki na biały */
        }

        /* Zmiana wyglądu górnego paska */
        header {
            background-color: #bfbad9 !important;  /* Kolor tła paska nawigacyjnego */
        }

        /* Zmiana stylu nagłówków */
        h1, h2, h3, h4, h5, h6 {
            text-indent: 30px;
            margin-bottom: 60px;
            background-color: #e9e6fc !important;
            color: #3f3f4d !important;  /* Kolor nagłówków na złoty (gold) */
        }

        /* Sidebar (menu z lewej strony) */
        .stSidebar {
            background-color: #bfbad9 !important;  /* Kolor tła bocznego menu - teraz taki sam jak górny pasek */
            color: white !important;  /* Kolor czcionki na biały */
        }

        /* Ikony w sidebarze */
        .stSidebar svg {
            fill: #3f3f4d !important;  /* Kolor ikon w menu na biały */
        }

        /* Styl dla elementów w sidebarze */
        .stSidebarContent {
            background-color: #1F1A3D !important;
        }

        /* Zmiana tła dla przycisków */
        .stButton > button {
            background-color: #966edb;  /* Kolor tła przycisków na złoty */
            color: #1F1A3D;  /* Kolor czcionki przycisków na czarny */
        }

        /* Stylowanie tła dla formularzy i inputów */
        .stTextInput input, .stTextInput textarea {
            background-color: #b4a4bf;  /* Kolor tła inputów na fioletowy */
            color: white !important;  /* Kolor czcionki w inputach na biały */
        }

        /* Tabela - zmiana koloru tła i tekstu */
        .stDataFrame, .stTable {
            background-color: #6A0DAD;
            color: white;
        }

        /* Kolory dla linków */
        a {
            color: #EAB8E4 !important;
        }

        /* Target smaller font text, set to gold and increase font size */
        .stMarkdown p, .stText {
            color: #3f3f4d !important;  /* Gold text */
            font-size: 18px !important;  /* Increase font size */
        }

        /* Ensure all text on pages is white or pink, including in sections */
        .stMarkdown, .stText, .stDataFrame, .stTable, .stWrite, .stSelectbox, .stMultiselect, .stButton, .stTextInput, .stTextArea, .stRadio {
            color: #342340 !important;  /* Ensure text is pink */
            font-size: 20px !important;  /* Uniform font size */
        }

        /* Customize multiselect box */
        .stMultiSelect label, .stMultiSelect div {
            color: #342340 !important;  /* Multiselect text color */
            font-size: 20px !important;  /* Font size */
        }

        /* Ensure that placeholder text in input fields is the correct color */
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #342340 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Ścieżka do pliku Excel
file_path = "All_merged.xlsx"

# Menu boczne (sidebar)
st.sidebar.title("Menu")
page = st.sidebar.selectbox("GENERAL INFORMATION", ["MAIN", "PROJECT DESCRIPTION", "DATASETS DESCRIPTION", "ALL PROTEINS MERGED-TABLE"])

# Strona główna
if page == "MAIN":
    st.title("RAT AND MOUSE COMPARATIVE") 
    st.title("BRAIN TISSUE PALMITOYLOMES")
    logo_path = "Logo2.png"  # Update the path if needed
    st.image(logo_path, use_container_width=False)

# PROJECT DESCRIPTION
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
    """)


# DATASETS DESCRIPTION
elif page == "ALL PROTEINS MERGED-TABLE":
    df = pd.read_excel(file_path, engine="openpyxl")
    st.title("Multi-Filter Excel Data")
    filter_columns = st.multiselect("All reported palmitoylated proteins merged in single database. Use multifilter to filter data:", df.columns)  # Limit to 8
    filters = {}
    for column in filter_columns:
        unique_values = df[column].dropna().unique()  # Get unique values
        selected_values = st.multiselect(f"Filter {column}:", unique_values)  # Allow selection
        if selected_values:
            filters[column] = selected_values  # Store selections

    for column, selected_values in filters.items():
        df = df[df[column].isin(selected_values)]

    st.dataframe(df, use_container_width=True)

# STRING Network
elif page == "STRING Network":
    st.title("STRING Network")
    try:
        img_path = "STRING network - 2--clustered.png"
        img = Image.open(img_path)
        zoomed_img = image_zoom(img)
        if zoomed_img is not None:
            st.image(zoomed_img, caption="STRING Network Visualization (Zoomed)", use_container_width=True)
    except FileNotFoundError:
        st.error(f"File not found: {img_path}. Ensure the file exists.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Cytoscape
elif page == "Cytoscape":
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
elif page == "Metascape":
    st.title("Metascape Visualization")
    st.markdown("[OPEN Metascape Visualization](https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/)")
    st.write("Or view a preview here:")
    st.components.v1.iframe(
        "https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/",
        height=800,
        width="100%",
        scrolling=True
    )
