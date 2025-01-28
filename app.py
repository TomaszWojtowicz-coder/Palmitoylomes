import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image  # Importujemy bibliotekę PIL


# Load and display the logo
logo_path = "Logo.webp"  # Update the path if needed
st.image(logo_path, use_column_width=True)

# Menu boczne (sidebar)
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Wybierz stronę", ["Główna", "STRING Network", "Cytoscape", "Metascape"])

# Rest of your code continues...
if page == "Główna":
    st.title("Witamy w aplikacji")
    st.write("Wybierz jedną z sekcji w menu po lewej stronie.")



# Menu boczne (sidebar)
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Choose", ["MAIN", "STRING Network", "Cytoscape", "Metascape"])

# Strona główna
if page == "MAIN":
    st.title("WELCOME TO RAT AND MOUSE") 
    st.title("")
    st.title("BRAIN TISSUE PALMITOYLOME")
    #st.write("CHOOSE SECTION")

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
        st.error(f"Nie znaleziono pliku: {img_path}. Upewnij się, że plik istnieje.")
    except Exception as e:
        st.error(f"Wystąpił błąd: {e}")

# Sekcja: Cytoscape
elif page == "Cytoscape":
    st.title("Cytoscape Network")
    st.write("Pobierz plik .cys do wizualizacji w Cytoscape:")
    try:
        with open("Enrichment_GO_GONetwork.cys", "rb") as cys_file:
            st.download_button(label="Pobierz plik Cytoscape (.cys)",
                               data=cys_file,
                               file_name="Enrichment_GO_GONetwork.cys",
                               mime="application/octet-stream")
    except FileNotFoundError:
        st.error("Nie znaleziono pliku .cys. Upewnij się, że został poprawnie załadowany.")

# Sekcja: Metascape
elif page == "Metascape":
    st.title("Metascape Visualization")
    st.markdown("[OPEN Metascape Visualization](https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/)")
    st.write("Lub zobacz podgląd tutaj:")
    st.components.v1.iframe(
        "https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/",
        height=800,  # Wysokość iframe
        width=1200,  # Szerokość w pikselach
        scrolling=True
    )

# Sekcja: Enrichment Heatmap
st.sidebar.header("EXTRAS")
if st.sidebar.checkbox("SHOW Heatmap PDF"):
    st.title("Enrichment Heatmap")
    try:
        with open("Enrichment_heatmap_HeatmapSelectedGO.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button(label="Pobierz PDF", data=pdf_data, file_name="Enrichment_heatmap_HeatmapSelectedGO.pdf", mime="application/pdf")
        st.markdown("""
        <iframe src="Enrichment_heatmap_HeatmapSelectedGO.pdf" width="100%" height="600px">
        </iframe>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Nie znaleziono pliku PDF. Upewnij się, że został poprawnie załadowany.")
