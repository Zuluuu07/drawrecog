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


# Streamlit 
st.set_page_config(page_title='Tablero Inteligente', page_icon='🧠', layout='wide')

# ==== ESTILOS — SOLO VISUAL ====
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
      font-family: 'Quicksand', sans-serif !important;
      background: transparent !important;
    }

    /* Títulos sin fondo ni bloques */
    h1, h2, h3, h4 {
      background: none !important;
      box-shadow: none !important;
      border: none !important;
      margin-top: .25rem;
      margin-bottom: .35rem;
      font-weight: 700;
      letter-spacing: .2px;
    }

    /* Colores adaptativos a modo claro/oscuro */
    @media (prefers-color-scheme: dark) {
      h1, h2, h3, h4 { color: #eaeaea !important; }
    }
    @media (prefers-color-scheme: light) {
      h1, h2, h3, h4 { color: #1f2937 !important; }
    }

    /* Sidebar translúcido */
    [data-testid="stSidebar"] {
      background: rgba(127,127,127,0.06) !important;
      backdrop-filter: blur(8px);
      border-right: 1px solid rgba(127,127,127,0.12);
    }

    /* Entradas redondeadas */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stColorPicker input {
      border-radius: 12px !important;
    }

    /* Slider más suave */
    .stSlider > div [role="slider"] {
      height: 14px !important;
      border-radius: 999px !important;
    }
    .stSlider > div [data-baseweb="slider"] > div {
      border-radius: 999px !important;
    }

    /* Botones con gradiente */
    .stButton > button {
      background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
      color: #fff !important;
      border: none !important;
      border-radius: 12px !important;
      font-weight: 700 !important;
      padding: .6rem 1rem !important;
      box-shadow: 0 8px 22px rgba(0,0,0,.25);
      transition: all .2s ease-in-out;
    }
    .stButton > button:hover {
      filter: brightness(1.05);
      transform: translateY(-1px);
    }

    /* Lienzo con esquinas redondeadas y sombra */
    canvas {
      border-radius: 18px !important;
      border: 1px solid rgba(127,127,127,0.18) !important;
      box-shadow: 0 10px 28px rgba(0,0,0,.22) !important;
    }

    /* Texto secundario */
    label, p, .stMarkdown, .stCaption, .stText { color: inherit !important; }

    /* Divisores suaves */
    hr { border-top: 1px solid rgba(127,127,127,0.18) !important; }
    </style>
    """,
    unsafe_allow_html=True
)
# ==== FIN DE ESTILOS ====


st.title('Tablero Inteligente')
with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto")
st.subheader("Dibuja el boceto en el panel  y presiona el botón para analizarla")

# Add canvas component
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000" 
bg_color = '#FFFFFF'

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=api_key)

analyze_button = st.button("Analiza la imagen", type="secondary")

if canvas_result.image_data is not None and api_key and analyze_button:
    with st.spinner("Analizando ..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")
        prompt_text = (f"Describe in spanish briefly the image")

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

        try:
            full_response = ""
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model= "gpt-4o-mini",  
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
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
