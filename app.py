import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("Interaktywna grafika")

# Ustawienia płótna
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Kolor wypełnienia
    stroke_width=3,                       # Grubość linii
    stroke_color="black",                 # Kolor linii
    background_color="white",             # Kolor tła
    height=400,
    width=600,
    drawing_mode="freedraw",              # Tryb rysowania (np. freedraw, line, circle)
    key="canvas"
)

# Wyświetl wynik
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data, caption="Twoje rysowanie")
