import streamlit as st
from transformers import pipeline

# 1. Cargar el modelo solo una vez (caché)
@st.cache_resource
def load_model():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_model()

# 2. Interfaz de usuario
st.title("🧠 Clasificador de Tópicos Flexible (Zero-Shot)")

st.write("Escribe un texto y proporciona las categorías posibles (separadas por comas).")

texto = st.text_area("Texto a analizar:", "Messi ganó el Balón de Oro y es considerado el mejor futbolista del mundo.")
etiquetas = st.text_input("Categorías (separadas por comas):", "deportes, política, economía, tecnología")

if st.button("Clasificar"):
    if texto and etiquetas:
        # Convertir string a lista
        candidate_labels = [e.strip() for e in etiquetas.split(",")]

        # 3. Clasificación
        resultados = classifier(texto, candidate_labels)

        # 4. Mostrar resultados
        st.subheader("Resultados de Clasificación")
        st.bar_chart(dict(zip(resultados["labels"], resultados["scores"])))
    else:
        st.warning("Por favor ingresa texto y categorías.")
