import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

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
    
    # Wczytanie obrazu
    img_path = "STRING network - 2--clustered.png"
    try:
        img = Image.open(img_path)
        st.image(img, caption="STRING Network Visualization", use_container_width=True)
        
        # Wyświetlanie obrazu z możliwością powiększania
        st.write("Kliknij na obrazek, aby powiększyć (zoom).")
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.axis('off')  # Wyłącz osie
        st.pyplot(fig)
    except FileNotFoundError:
        st.error(f"Nie znaleziono pliku: {img_path}. Upewnij się, że plik istnieje.")

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
    st.markdown("[Otwórz wizualizację Metascape](https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/)")
    st.write("Lub zobacz podgląd tutaj:")
    st.components.v1.iframe("https://metascape.org/gp/Content/CyJS/index.html?session_id=thqv3v8hs&Network=GONetwork&Style=ColorByCluster#/", height=600, scrolling=True)

# Sekcja: Enrichment Heatmap
st.sidebar.header("Dodatkowe zasoby")
if st.sidebar.checkbox("Pokaż Heatmap PDF"):
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
