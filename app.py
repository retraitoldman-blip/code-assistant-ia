import streamlit as st
from groq import Groq

st.set_page_config(page_title="🤖 Mon Assistant Code", page_icon="🤖", layout="wide")
st.title("🤖 Mon Assistant Code IA")

with st.sidebar:
    groq_key = st.text_input("Clé API Groq", type="password", placeholder="gsk_...")
    if groq_key and groq_key.startswith("gsk_"):
        st.success("✅ Clé valide")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Tu es un expert en code Python."}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Pose ta question..."):
    if "groq_api_key" in st.secrets:
        groq_key = st.secrets["groq_api_key"]
        st.success("✅ Clé API chargée automatiquement")
     else:
         groq_key = st.text_input("Clé API Groq", type="password", placeholder="gsk_...")
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Réflexion... ⚡"):
            try:
                client = Groq(api_key=groq_key)
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:

                st.error(f"❌ Erreur: {str(e)[:150]}")
