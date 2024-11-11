import streamlit as st
from groq import Groq

#Comando de ejecucion:
#python -m streamlit run d:\Programacion\Python\IA\desafio9.py

modelos = ["llama3-8b-8192","llama3-70b-8192","mixtral-8x7b-32768"]
modeloEnUso = ""
clienteUsuario = ""
claveSecreta = ""
mensaje = ""

def crearUsuario():
    claveSecreta = st.secrets["CLAVE_API"]
    return Groq(api_key=claveSecreta)

def configurarModelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role" : "user", "content" : mensajeDeEntrada}],
        stream = True
    )

def generarRespuesta(chatCompleto):
    respuestaCompleta = ""
    for frase in chatCompleto:
        if frase.choices[0].delta.content:
            respuestaCompleta += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuestaCompleta

st.set_page_config(page_title="ChatBot", page_icon="⚡", layout="centered")
   
def configurarPagina():

    st.title("ChatBot de AC⚡:")
    st.sidebar.title("Configuración de la IA")
    elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options=modelos, index=0)
    return elegirModelo

def inicializarEstado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizarHistorial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrarHistorial():
        for mensaje in st.session_state.mensajes:
                with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
                        st.markdown(mensaje["content"])

def areaChat():
        contenedorDelChat = st.container(height=400,border=True)
        with contenedorDelChat:
                mostrarHistorial()

def main():
    modeloEnUso = configurarPagina()
    clienteUsuario = crearUsuario()
    inicializarEstado()
    areaChat()
    mensaje = st.chat_input()
    chatCompleto = None
    if mensaje:
        actualizarHistorial("user", mensaje, "🧑‍💻")
        chatCompleto = configurarModelo(clienteUsuario, modeloEnUso, mensaje)
    if chatCompleto:
        with st.chat_message("assistant"):
            respuestCompleta = st.write_stream(generarRespuesta(chatCompleto))
        actualizarHistorial("assistant", respuestCompleta,"🤖")
        st.rerun()

if __name__ == "__main__":
    main()
    
    
