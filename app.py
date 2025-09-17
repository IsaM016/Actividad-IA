import streamlit as st
from groq import Groq

# 1. Cargar API Key de forma segura
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# 2. Inicializar historial con mensaje de sistema
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Eres un asistente útil y conversacional."}
    ]

st.title("🤖 Chatbot con Memoria (Groq + Streamlit)")

# 3. Mostrar historial previo (sin mostrar el system prompt)
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 4. Entrada de usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Guardar mensaje del usuario
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Enviar todo el historial al modelo de Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ Modelo actualizado
            messages=st.session_state["messages"]
        )
        respuesta = response.choices[0].message.content

        # Guardar respuesta del modelo
        st.session_state["messages"].append({"role": "assistant", "content": respuesta})

        with st.chat_message("assistant"):
            st.markdown(respuesta)

    except Exception as e:
        st.error(f"Error con la API de Groq: {e}")
