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
st.markdown("""
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
  filte
