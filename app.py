import os
import streamlit as st
import base64
from openai import OpenAI
import openai
# from PIL import Image
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_drawable_canvas import st_canvas

Expert=" "
profile_imgenh=" "

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# =========================
# Configuración y Estilos (SOLO UI)
# =========================
st.set_page_config(page_title='Tablero Inteligente', layout="wide", page_icon="🧠")

st.markdown("""
<style>
/* Tipografía global */
html, body, [class*="css"]  {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", Arial, sans-serif;
}

/* Encabezado principal */
.app-header {
  background: linear-gradient(135deg, #3b82f6 0%, #22c55e 100%);
  border-radius: 16px;
  padding: 20px 24px;
  color: white !important;
  box-shadow: 0 6px 24px rgba(0,0,0,.08);
  margin-bottom: 14px;
}

/* Sidebar translúcido */
[data-testid="stSidebar"] {
  background: rgba(127,127,127,0.06) !important;
  backdrop-filter: blur(8px);
  border-right: 1px solid rgba(127,127,127,0.12);
}

/* Tarjetas */
.card {
  border: 1px solid rgba(0,0,0,.07);
  border-radius: 16px;
  padding: 18px;
  background: #ffffffaa;
  backdrop-filter: blur(6px);
  box-shadow: 0 4px 18px rgba(0,0,0,.06);
}

/* Botones */
.stButton > button {
  border-radius: 12px;
  height: 42px;
  font-weight: 600;
}

/* Inputs redondeados */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div, .stColorPicker input {
  border-radius: 12px !important;
}

/* Slider suave */
.stSlider > div [role="slider"] {
  height: 14px !important;
  border-radius: 999px !important;
}

/* Borde para el lienzo */
.canvas-wrap {
  border: 1px dashed rgba(0,0,0,.2);
  border-radius: 14px;
  padding: 8px;
}

/* Texto secundario heredado */
label, p, .stMarkdown, .stCaption, .stText {
  color: inherit !important;
}

/* Soporte tema oscuro/claro */
@media (prefers-color-scheme: dark) {
  h1, h2, h3, h4 { color: #eaeaea !important; }
}
@media (prefers-color-scheme: light) {
  h1, h2, h3, h4 { color: #1f2937 !important; }
}
</style>
""", unsafe_allow_html=True)

# =========================
# Contenido original (texto/estructura)
# =========================
# =========================
# Encabezado y sidebar (UI)
# =========================
st.markdown(
    '''
<div class="app-header">
  <h2 style="margin:0;">🧠 Tablero Inteligente</h2>
  <div>Interpreta un boceto dibujado y obtén una breve descripción con IA.</div>
</div>
''',
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("### Acerca de")
    st.write("Esta aplicación demuestra la capacidad de interpretar un **boceto** usando visión.")
    st.caption("Consejo: usa líneas oscuras sobre fondo blanco para mejores resultados.")

st.markdown("#### ✏️ Dibuja en el lienzo y presiona **Analiza la imagen**")

# =========================
# Parámetros del dibujo (sin cambios lógicos)
# =========================
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000"
bg_color = '#FFFFFF'

# =========================
# Lienzo (misma API)
# =========================
st.markdown("#### Lienzo")
st.markdown('<div class="canvas-wrap">', unsafe_allow_html=True)
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=340,
    width=520,
    drawing_mode=drawing_mode,
    key="canvas",
)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# API Key (misma lógica)
# =========================
ke = st.text_input('Ingresa tu Clave', type="password", placeholder="sk-...")
os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Botón (misma lógica)
analyze_button = st.button("Analiza la imagen", type="secondary")

# =========================
# Proceso de análisis (idéntico)
# =========================
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')

        # Codificar la imagen en base64
        base64_image = encode_image_to_base64("img.png")

        prompt_text = (f"Describe in spanish briefly the image")

        # Create the payload for the completion request
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url":f"data:image/png;base64,{base64_image}",
                    },
                ],
            }
        ]

        # Make the request to the OpenAI API (misma llamada)
        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model= "gpt-4o-mini",  # o1-preview ,gpt-4o-mini
              messages=[
                {
                   "role": "user",
                   "content": [
                     {"type": "text", "text": prompt_text},
                     {
                       "type": "image_url",
                       "image_url": {
                         "url": f"data:image/png;base64,{base64_image}",
                       },
                     },
                   ],
                  }
                ],
              max_tokens=500,
              )

            # Mostrar resultado (misma data, mejor presentación)
            st.markdown("##### Resultado")
            if response.choices[0].message.content is not None:
                full_response += response.choices[0].message.content
                message_placeholder.markdown(full_response + " ▌")

            message_placeholder.markdown(f"""
<div class="card">
  <div style="font-weight:600;margin-bottom:6px;">Descripción breve</div>
  <div>{full_response}</div>
</div>
""", unsafe_allow_html=True)

            if Expert== profile_imgenh:
               st.session_state.mi_respuesta= response.choices[0].message.content

            # Miniatura de la última imagen (solo UI)
            try:
                st.markdown("###### Última imagen analizada")
                st.image("img.png", caption="img.png", use_container_width=True)
            except Exception:
                pass

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    # Warnings para acción del usuario (igual)
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
