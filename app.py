import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image  # Importujemy bibliotekę PIL
import pandas as pd
import os

# Ustawienie strony na pełną szerokość
st.set_page_config(layout="wide")

# Ścieżka do pliku Excel
file_path = "All_merged.xlsx"

# Menu boczne (sidebar)
st.sidebar.title("Menu")
page = st.sidebar.selectbox("GENERAL INFORMATION", ["MAIN", "PROJECT DESCRIPTION", "DATASETS DESCRIPTION", "ALL PROTEINS MERGED-TABLE"])
# Strona główna
if page == "MAIN":
    st.title("RAT AND MOUSE COMPARATIVE") 
    #st.title("")
    st.title("BRAIN TISSUE PALMITOYLOMES")
    # st.write("CHOOSE SECTION")
# Load and display the logo
    # Load and display the logo
    logo_path = "Logo.webp"  # Update the path if needed
    st.image(logo_path, use_container_width=True)
#logo_path = "logo3.webp"  # Update the path if needed
 #   st.image(logo_path, use_column_width=True)

#PROJECT DESCRIPTION
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


#DATASETS DESCRIPTION
# 📊 Sekcja: Wyświetlanie danych z Excela
elif page == "ALL PROTEINS MERGED-TABLE":
    st.title("Excel Data: All Merged")

    if os.path.exists(file_path):
        try:
            # ✅ Sprawdzenie rozmiaru pliku
            if os.path.getsize(file_path) == 0:
                st.error("❌ Excel file is empty.")
            else:
                # ✅ Wczytanie pliku Excel
                df = pd.read_excel(file_path, engine="openpyxl")

                # ✅ Sprawdzenie, czy dane nie są puste
                if df.empty:
                    st.warning("⚠️ The file was loaded but contains no data.")
                else:
                    # ✅ Wyświetlenie tabeli
                    st.dataframe(df, use_container_width=True)
                    st.write(f"📊 Data contains {df.shape[0]} rows and {df.shape[1]} columns.")
        
        except Exception as e:
            st.error(f"❌ Error loading Excel file: {e}")
    else:
        st.error(f"❌ File not found: {file_path}. Please upload the correct file.")

# Sekcja: STRING Network
elif page == "STRING Network":
    st.title("STRING Network")
    try:
        img_path = "STRING network - 2--clustered.png"
        
        # Otwieramy obraz przy użyciu PIL (Pillow)
        img = Image.open(img_path)

        # Przekazujemy obraz do funkcji image_zoom
        zoomed_img = image_zoom(img)
        if zoomed_img is not None:
            st.image(zoomed_img, caption="STRING Network Visualization (Zoomed)", use_container_width=True)
    except FileNotFoundError:
        st.error(f"File not found: {img_path}. Ensure the file exists.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Sekcja: Cytoscape
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

# Sekcja: Metascape
elif page == "Metascape":
    st.title("Metascape Visualization")
    st.markdown("[OPEN Metascape Visualization](https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/)")
    st.write("Or view a preview here:")
    st.components.v1.iframe(
        "https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/",
        height=800,  # Wysokość iframe
        width="100%",  # Szerokość w procentach
        scrolling=True
    )

# Sekcja: Enrichment Heatmap
#st.sidebar.header("MOUSE COMPARATIVE PALMITOYLOME")
#st.sidebar.header("RAT COMPARATIVE PALMITOYLOME")
#st.sidebar.header("EXTRAS")
#if st.sidebar.checkbox("SHOW Heatmap PDF"):
#    st.title("Enrichment Heatmap")
#    try:
#        with open("Enrichment_heatmap_HeatmapSelectedGO.pdf", "rb") as pdf_file:
#            pdf_data = pdf_file.read()
#        st.download_button(label="Download Heatmap PDF", data=pdf_data, file_name="Enrichment_heatmap_HeatmapSelectedGO.pdf", mime="application/pdf")
 #       st.markdown("""
  #      <iframe src="Enrichment_heatmap_HeatmapSelectedGO.pdf" width="100%" height="600px">
   #     </iframe>
    #    """, unsafe_allow_html=True)
  #  except FileNotFoundError:
   #     st.error("Heatmap PDF file not found. Ensure it has been uploaded.")
