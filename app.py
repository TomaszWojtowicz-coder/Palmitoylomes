import streamlit as st
from streamlit_image_zoom import image_zoom

# Menu boczne (sidebar)
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Wybierz stronę", ["Główna", "STRING Network", "Cytoscape", "Metascape"])

# Strona główna
if page == "Główna":
    st.title("Witamy w aplikacji")
    st.write("Wybierz jedną z sekcji w menu po lewej stronie.")

# Sekcja: STRING Network
elif page == "STRING Network":
    st.title("STRING Network")
    st.image("STRING network - 2--clustered.png", caption="STRING Network Visualization", use_container_width=True)

# Ładowanie obrazu z opcją zoom
try:
    img_path = "STRING network - 2--clustered.png"
    zoomed_img = image_zoom(img_path)
    if zoomed_img is not None:
        st.image(zoomed_img, caption="STRING Network Visualization (Zoomed)", use_container_width=True)
except FileNotFoundError:
    st.error(f"Nie znaleziono pliku: {img_path}. Upewnij się, że plik istnieje.")





# Sekcja: Cytoscape
elif page == "Cytoscape":
    st.title("Cytoscape Network")
    st.write("Pobierz plik .cys do wizualizacji w Cytoscape:")
    with open("Enrichment_GO_GONetwork.cys", "rb") as cys_file:
        st.download_button(label="Pobierz plik Cytoscape (.cys)",
                           data=cys_file,
                           file_name="Enrichment_GO_GONetwork.cys",
                           mime="application/octet-stream")

# Sekcja: Metascape
elif page == "Metascape":
    st.title("Metascape Visualization")
    st.markdown("[Otwórz wizualizację Metascape](https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/)")
    st.write("Lub zobacz podgląd tutaj:")
    st.components.v1.iframe("https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/", height=600, scrolling=True)

# Sekcja: Enrichment Heatmap
st.sidebar.header("Dodatkowe zasoby")
if st.sidebar.checkbox("Pokaż Heatmap PDF"):
    st.title("Enrichment Heatmap")
    with open("Enrichment_heatmap_HeatmapSelectedGO.pdf", "rb") as pdf_file:
        pdf_data = pdf_file.read()
    st.download_button(label="Pobierz PDF", data=pdf_data, file_name="Enrichment_heatmap_HeatmapSelectedGO.pdf", mime="application/pdf")
    st.write("Podgląd:")
    st.pdf("Enrichment_heatmap_HeatmapSelectedGO.pdf")

st.title("STRING Network with Zoom")
