import streamlit as st
import json
import os
import sys
from streamlit_mic_recorder import mic_recorder

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YugmaCare", page_icon="🏥", layout="wide")

# --- 2. PATHS ---
BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.append(BASE)

from logic.intent_engine import analyze_problem, map_support

# --- 3. CSS INJECTION ---
CSS_PATH = os.path.join(BASE, "static", "style.css")
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'desc_text' not in st.session_state:
    st.session_state.desc_text = ""
if 'show_reset' not in st.session_state:
    st.session_state.show_reset = False

def do_reset():
    st.session_state.clear()
    st.rerun()

# --- 5. CALLBACK ---
def voice_callback():
    if st.session_state.my_recorder_output:
        st.session_state.desc_text = st.session_state.my_recorder_output['text']

# --- 6. DATA LOADING ---
def load_data():
    try:
        with open(os.path.join(BASE, "data", "emergency_data.json"), "r", encoding="utf-8") as f:
            e = json.load(f)
        with open(os.path.join(BASE, "data", "support_resources.json"), "r", encoding="utf-8") as f:
            s = json.load(f)
        with open(os.path.join(BASE, "data", "emergency_texts.json"), "r", encoding="utf-8") as f:
            t = json.load(f)
        return e, s, t
    except Exception as ex:
        st.error(f"File Error: {ex}")
        st.stop()

e_data, s_data, t_data = load_data()
# Map codes to display names
lang_map = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi"
}

# format_func shows the full name, but 'lang' still captures "en", "hi", or "mr"
lang = st.sidebar.selectbox(
    "Language", 
    options=list(lang_map.keys()), 
    format_func=lambda x: lang_map[x]
)

texts = t_data[lang]

# --- 7. UI HEADER ---
st.title("YugmaCare")

if st.session_state.show_reset:
    with st.container(border=True):
        st.warning("Reset Application?")
        c1, c2 = st.columns(2)
        if c1.button("Yes", use_container_width=True, type="primary"): do_reset()
        if c2.button("No", use_container_width=True): 
            st.session_state.show_reset = False
            st.rerun()

# --- 8. FORM WITH "INVISIBLE" BUTTON ---
with st.form("main_form"):
    
    # 95% Label | 5% Icon (Tight Layout)
    col_label, col_mic = st.columns([0.95, 0.05])
    
    with col_label:
        st.write(texts['placeholder'])
    
    with col_mic:
        # Just the Emoji. CSS removes the button box.
        mic_recorder(
            key='my_recorder_output', 
            callback=voice_callback,
            start_prompt="🎙️", 
            stop_prompt="⏹️"
        )

    # Text Area
    description = st.text_area(
        "Desc", 
        label_visibility="collapsed",
        value=st.session_state.desc_text,
        height=120,
        key="desc_input_area"
    )

    loc = st.text_input("Location", key="loc_input")
    h_pref = st.radio("Hospitals", ["All", "Government", "Private"], horizontal=True)
    
    submit = st.form_submit_button(texts['get_help'], use_container_width=True)

# Minimal Reset
if st.button("Reset", use_container_width=True):
    st.session_state.show_reset = True
    st.rerun()

# --- 9. RESULTS ---
if submit and description:
    # Sync manual typing
    st.session_state.desc_text = description
    intent = analyze_problem(description)
    
    st.subheader("🚨 Emergency Contacts")
    d1, d2, d3, d4 = st.columns(4)
    d1.markdown('<div class="dial-box"><a href="tel:108" class="call-link">🚑 108</a></div>', unsafe_allow_html=True)
    d2.markdown('<div class="dial-box"><a href="tel:9343180000" class="call-link">🚑 Private</a></div>', unsafe_allow_html=True)
    d3.markdown('<div class="dial-box"><a href="tel:112" class="call-link">📞 112</a></div>', unsafe_allow_html=True)
    d4.markdown('<div class="dial-box"><a href="tel:102" class="call-link">👶 102</a></div>', unsafe_allow_html=True)

    st.divider()
    res_map, res_aid = st.columns([1.5, 1])

    with res_aid:
        st.subheader("🩺 First Aid")
        
        for key in intent["emergencies"]:
            target = key if key in e_data else "general"
            for card in e_data[target]["cards"]:
                with st.expander(card['title'], expanded=True):
                    for step in card['steps']:
                        st.write(f"• {step}")

    with res_map:
        pref = h_pref.lower() if h_pref != "All" else intent["hospital_type"]
        st.subheader(f"{pref.capitalize()} Hospitals Nearby")
        m_query = f"{pref if pref != 'all' else ''} hospitals in {loc if loc else 'me'}"
        url = f"https://www.google.com/maps?q={m_query.replace(' ', '+')}&output=embed"
        st.components.v1.iframe(url, height=400)

    st.divider()
    support = map_support(intent, s_data)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.info("Government Schemes")
        for s in support.get("schemes", []): st.write(f"**{s['name']}**")
    with sc2:
        st.success("Verified NGOs")
        for n in support.get("ngos", []): st.write(f"**{n['name']}** - {n['contact']}")
