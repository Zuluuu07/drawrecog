import os
import streamlit as st
import base64
from openai import OpenAI
import openai
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
# 🌙 Tema visual mejorado
st.set_page_config(page_title='Tablero Inteligente', page_icon='🧠', layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  {
  font-family: 'Poppins', sans-serif !important;
  background-color: transparent !important;
}

/* Encabezado */
h1 {
  text-align: center;
  font-weight: 700;
  font-size: 2.5em;
  color: #e3e3e3;
  text-shadow: 0 0 20px rgba(157, 78, 221, 0.5);
  margin-bottom: 0.2em;
}

/* Subtítulos */
h2, h3, h4 {
  color: #dcdcdc !important;
}

/* Bloques */
.section {
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.05);
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  margin-bottom: 25px;
}

/* Botones */
button, .stButton>button {
  background: linear-gradient(135deg, #845ef7 0%, #5b5ce0 100%) !important;
  color: white !important;
  border-radius: 12px !important;
  border: none !important;
  font-weight: 600 !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.25);
}
button:hover {
  background: linear-gradient(135deg, #6c4ad0 0%, #4a4bc2 100%) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.stTextInput>div>div>input {
  border-radius: 10px;
}

/* Footer */
.footer {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Encabezado bonito sin fondo blanco
st.markdown("<h1>🧠 Tablero Inteligente</h1>", unsafe_allow_html=True)
st.caption("Interpreta bocetos con inteligencia artificial 🖌️")

# Sidebar
with st.sidebar:
    st.subheader("ℹ️ Acerca de")
    st.write("Esta aplicación demuestra cómo una IA puede **interpretar un boceto** dibujado por el usuario.")
    st.markdown("---")
    st.caption("💡 Consejo: usa trazo negro sobre fondo blanco para mejores resultados.")

# Sección principal
st.markdown("<h3>✏️ Dibuja el boceto y presiona el botón para analizarlo</h3>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Canvas y parámetros
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Ancho de línea', 1, 30, 5)
stroke_color = "#000000"
bg_color = '#FFFFFF'

st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("##### 🎨 Lienzo")
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
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# API key input
ke = st.text_input('🔐 Ingresa tu Clave', type="password", help="Tu clave personal de OpenAI")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENA]()_
