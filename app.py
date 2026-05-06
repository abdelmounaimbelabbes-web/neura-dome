import streamlit as st
import google.generativeai as genai
import hashlib
import time
from datetime import datetime

# --- 1. الإعدادات الأساسية (ضع بياناتك هنا) ---
AD_LINK = "https://www.profitablecpmratenetwork.com/qmq78q88?key=974975a2c04a76658c6fe18ce3f7190e"
GEMINI_API_KEY = "AIzaSyBNLGRry2FCzHJQoG9AIFKmSkWf50PZiZ0"
SECURITY_SALT = "GLOBAL_SECURE_77"

# إعداد الصفحة لتكون متوافقة مع الجوال والحواسيب
st.set_page_config(page_title="NEURA DOME AI", layout="centered", page_icon="🧠")

# --- 2. نظام اكتشاف اللغة وإدارة الجلسة ---
if 'authorized' not in st.session_state:
    st.session_state.authorized = False

# اختيار اللغة (يمكن إضافة المزيد)
lang = st.sidebar.selectbox("🌐 Language / اللغة", ["English", "العربية", "Français", "Español"])

# نصوص الواجهة حسب اللغة المختارة
texts = {
    "English": {
        "title": "🔓 UNLOCK NEURA DOME",
        "desc": "To use AI for free, please support us by clicking the button below.",
        "btn": "⚡ ACTIVATE ACCESS ⚡",
        "confirm": "🚀 I have clicked, Enter Now",
        "status": "✅ Access Granted!",
        "input": "Ask NEURA anything..."
    },
    "العربية": {
        "title": "🔓 فتح القبة العصبية",
        "desc": "لاستخدام الذكاء الاصطناعي مجاناً، يرجى دعمنا بالضغط على الزر أدناه.",
        "btn": "⚡ تفعيل الوصول الآن ⚡",
        "confirm": "🚀 أكدتُ النقر، دخول",
        "status": "✅ تم فتح الوصول!",
        "input": "اسأل NEURA عن أي شيء..."
    },
    "Français": {
        "title": "🔓 DÉVERROUILLER NEURA DOME",
        "desc": "Pour utiliser l'IA gratuitement, veuillez nous soutenir en cliquant ci-dessous.",
        "btn": "⚡ ACTIVER L'ACCÈS ⚡",
        "confirm": "🚀 J'ai cliqué, Entrer",
        "status": "✅ Accès Autorisé!",
        "input": "Demandez n'importe quoi..."
    },
    "Español": {
        "title": "🔓 DESBLOQUEAR NEURA DOME",
        "desc": "Para usar la IA gratis, apóyanos haciendo clic en el botón de abajo.",
        "btn": "⚡ ACTIVAR ACCESO ⚡",
        "confirm": "🚀 He hecho clic, Entrar",
        "status": "✅ ¡Acceso Concedido!",
        "input": "Pregunta lo que sea..."
    }
}

t = texts[lang]

# --- 3. جدار الحماية (الإعلان الإجباري) ---
if not st.session_state.authorized:
    st.markdown(f"""
        <div style="background:#0f172a; padding:40px; border-radius:20px; border:2px solid #00f2fe; text-align:center; box-shadow: 0 0 40px rgba(0,242,254,0.15);">
            <h1 style="color:#00f2fe; font-family: sans-serif; letter-spacing: 2px;">{t['title']}</h1>
            <p style="color:#cbd5e1; font-size:1.1rem;">{t['desc']}</p>
            <br>
            <a href="{AD_LINK}" target="_blank" onclick="return true;">
                <button style="background:linear-gradient(45deg, #00f2fe, #4facfe); color:#000; padding:18px 40px; border-radius:12px; font-weight:bold; border:none; cursor:pointer; font-size:20px; transition: 0.3s;">
                    {t['btn']}
                </button>
            </a>
            <p style="color:#475569; margin-top:25px; font-size:0.9rem;">Protected by NEURA Shield v4.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button(t['confirm'], use_container_width=True):
        st.session_state.authorized = True
        st.rerun()
    st.stop() # 🛡️ حماية: يمنع تحميل المحرك قبل الضغط

# --- 4. تشغيل محرك الذكاء الاصطناعي العالمي ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # البحث التلقائي عن الموديل لتجنب أخطاء 404 في أي دولة
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available else available[0]
    model = genai.GenerativeModel(model_name)

    st.title(f"🧠 NEURA DOME AI ({lang})")
    st.success(t['status'])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # مدخل الدردشة
    if prompt := st.chat_input(t['input']):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # نظام الردود العالمي
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Error: Please check your API Key. ({e})")
