
import streamlit as st
from groq import Groq

# ─────────────────────────────────────────────────────────────
# 1. CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 Mon Assistant Code",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Mon Assistant Code IA")
st.caption("💡 Posez vos questions en Python, JavaScript, HTML, CSS, etc.")

# ─────────────────────────────────────────────────────────────
# 2. SIDEBAR & CONFIGURATION
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Gestion de la clé API
    if "groq_api_key" in st.secrets:
        groq_key = st.secrets["groq_api_key"]
        st.success("✅ Clé API chargée")
    else:
        groq_key = st.text_input("🔑 Clé API Groq", type="password", placeholder="gsk_...")
        if groq_key and groq_key.startswith("gsk_"):
            st.success("✅ Clé valide")
    
    st.markdown("[Obtenir une clé gratuite](https://console.groq.com/keys)")
    
    st.divider()

    
    # Bouton Nouveau Chat
    if st.button("🗑️ Nouveau Chat", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": "Tu es un expert en code Python."}]
        st.rerun()
    
    # Sélecteur de modèle
    model_choice = st.selectbox(
        "🧠 Modèle IA",
        ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"],
        help="8b: Rapide | 70b: Plus intelligent"
    )
    st.divider()
    if st.button("🔥 RÉINITIALISER COMPLÈT", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ─────────────────────────────────────────────────────────────
# 3. GESTION DE L'HISTORIQUE
# ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Tu es un expert en code Python."}]

# ─────────────────────────────────────────────────────────────
# 4. AFFICHAGE DES MESSAGES
# ─────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────────
# 5. TRAITEMENT DE LA REQUÊTE UTILISATEUR
# ─────────────────────────────────────────────────────────────
if prompt := st.chat_input("Pose ta question de code..."):
    
    # Vérification de la clé API
    if not groq_key or not groq_key.startswith("gsk_"):
        st.error("⚠️ Clé Groq requise (commençant par gsk_)")
        st.stop()
    
    # 1. Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Générer la réponse de l'IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # ✅ Placeholder pour mise à jour fluide
        full_response = ""  # ✅ Variable pour accumuler le texte
        
        try:
            client = Groq(api_key=groq_key, timeout=30)
            
            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True  # ✅ Streaming activé
            )
            
            # ✅ BOUCLE MANUELLE : Capture propre du texte chunk par chunk
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")  # Curseur animé
            
            # ✅ Affichage final sans curseur
            message_placeholder.markdown(full_response)
            
            # ✅ Sauvegarder UNIQUEMENT le texte (pas d'objet JSON)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)[:200]}")
