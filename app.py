import os
import streamlit as st
import base64
from openai import OpenAI
import openai
#from PIL import Image
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

# ─────────────────────────────────────────────────────────────
# 🎨 Decoración (no cambia funcionalidad)
st.set_page_config(page_title='Tablero Inteligente', page_icon='🎨', layout="wide")
st.markdown("""
<style>
/* Tipografía y look & feel */
html, body, [class*="css"]  { font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial; }
h1, h2, h3 { letter-spacing: .2px }

/* Tarjeta contenedora */
.box {
  border: 1px solid rgba(0,0,0,.08);
  border-radius: 18px;
  padding: 18px 20px;
  background: linear-gradient(180deg, rgba(250,250,252,1) 0%, rgba(248,248,251,1) 100%);
  box-shadow: 0 2px 12px rgba(0,0,0,.04);
}

/* Encabezado con gradiente */
.banner {
  border-radius: 18px;
  padding: 16px 18px;
  background: radial-gradient(1100px circle at 5% -20%, #e9f0ff 0%, transparent 40%),
              radial-gradient(1100px circle at 95% -20%, #ffece9 0%, transparent 40%),
              linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
  border: 1px solid rgba(0,0,0,.06);
}

/* Chips */
.chip {
  display:inline-block; padding:4px 10px; border-radius:999px;
  background:#f1f5f9; font-size:12px; margin-right:6px; border:1px solid #e5e7eb;
}

/* Footer */
.footer {
  color:#6b7280; font-size:12px; text-align:center; margin-top:24px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="banner"><h1>🧠 Tablero Inteligente</h1>'
            '<div class="chip">Canvas</div><div class="chip">Visión</div>'
            '<div class="chip">OpenAI</div></div>', unsafe_allow_html=True)
st.write("")

# ─────────────────────────────────────────────────────────────
# UI original (texto) + ligeras mejoras visuales
st.title('')  # mantiene la llamada original sin afectar el layout
with st.sidebar:
    st.subheader("Acerca de:")
    st.write("En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto.")
    st.markdown("---")
    st.caption("Consejo: usa fondo blanco y trazo negro para obtener resultados más nítidos.")
st.subheader("✏️ Dibuja el boceto en el panel y presiona el botón para analizarla")

# Add canvas component (mantengo tus parámetros)
#bg_image = st.sidebar.file_uploader("Cargar Imagen:", type=["png", "jpg"])
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
#stroke_color = '#FFFFFF'
#bg_color = '#000000'
stroke_color = "#000000"
bg_color = '#FFFFFF'
#realtime_update = st.sidebar.checkbox("Update in realtime", True)

st.markdown("#### Lienzo", help="Dibuja a mano alzada y luego pulsa **Analiza la imagen**.")
st.markdown('<div class="box">', unsafe_allow_html=True)

# Create a canvas component (idéntico en funcionalidad)
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    #background_image= None #Image.open(bg_image) if bg_image else None,
    drawing_mode=drawing_mode,
    key="canvas",
)

st.markdown('</div>', unsafe_allow_html=True)
st.divider()

ke = st.text_input('🔐 Ingresa tu Clave', type="password", help="Tu API key de OpenAI")
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Botón (mismo nombre/uso)
analyze_button = st.button("🔍 Analiza la imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        # Encode the image
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')

        # Codificar la imagen en base64
        base64_image = encode_image_to_base64("img.png")

        prompt_text = (f"Describe in spanish briefly the image")

        # Create the payload for the completion request (se mantiene tu estructura)
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

        # Make the request to the OpenAI API
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
            if response.choices[0].message.content is not None:
                    full_response += response.choices[0].message.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            if Expert== profile_imgenh:
               st.session_state.mi_respuesta= response.choices[0].message.content

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    # Warnings for user action required
    if not api_key:
        st.warning("Por favor ingresa tu API key.")

# ─────────────────────────────────────────────────────────────
# Footer decorativo (no funcional)
st.markdown('<div class="footer">Hecho con Streamlit • ✨ Manteniendo tu lógica original sin cambios</div>',
            unsafe_allow_html=True)
