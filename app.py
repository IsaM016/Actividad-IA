import streamlit as st
from groq import Groq

# 1. Configuración segura de la API
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# 2. Inicializar historial de la conversación
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("🤖 Chatbot con Memoria (Groq + Streamlit)")

# 3. Mostrar historial en pantalla
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Añadir mensaje del usuario al historial
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Mostrar el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Enviar historial completo al modelo
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state["messages"]
    )

    respuesta = response.choices[0].message.content

    # Añadir respuesta del modelo al historial
    st.session_state["messages"].append({"role": "assistant", "content": respuesta})

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta)
