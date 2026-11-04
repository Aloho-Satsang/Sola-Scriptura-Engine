import streamlit as st
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sola Scriptura Exegetical Engine",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- HEADER IMAGE DISPLAY ---
try:
    st.image("1793710934178.jpg", use_container_width=True)
except Exception:
    st.title("📖 Sola Scriptura Exegetical Engine")
    st.markdown("### Direct Bible Study in Original Languages & Context")
    st.caption("[External data used exclusively for historical, linguistic, and contextual analysis.]")

st.markdown("---")

# --- GEMINI CLIENT SETUP ---
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# System Instruction defining the engine's strict exegetical rules
system_prompt = """
You are an uncompromising, objective Sola Scriptura Exegetical and Canonical AI engine built for deep biblical analysis.

CORE OPERATIONAL RULES:
1. TRILINGUAL ORIGINAL LANGUAGES & OBJECTIVE ETYMOLOGY: Always analyze scripture using raw manuscript evidence from Ancient Hebrew, Aramaic, and Koine Greek. Perform deep syntactical, morphological, and grammatical parsing. Evaluate Semitic root words with complete linguistic integrity (e.g., historical Near-Eastern trade vocabulary, Assyrian/Akkadian parallels, and phonetic shifts).
2. HOLISTIC STRUCTURAL & TYPOLOGICAL INTEGRATION: Never isolate a single verse in a vacuum. You must actively analyze:
   - Biblical Typology (shadows, patterns, and historical templates).
   - Structural & Systemic Implications.
   - Cross-Testament Consistency (letting Scripture interpret Scripture across the entire canonical matrix).
3. ZERO MODERN HARMONIZATION OR TRADITIONAL BIAS: Never alter, soft-pedal, or tone down the raw textual reality to align with modern secular consensus, popular culture, OR 19th-century western denominational/lexicographical traditions. Evaluate primary botanical and historical evidence objectively without dismissing valid Near-Eastern etymological connections.
4. UNAPOLOGETIC & LOVING TRUTH: If a narrative misinterprets scripture, directly identify the twist, and explain the uncompromised scriptural truth with complete canonical evidence and logical clarity.
5. OVERRIDE TRANSLATION & LEXICAL ERRORS: Accurately correct translational shifts using original manuscript, archaeological, and Near-Eastern historical context.
"""

# --- CHAT STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT HANDLING ---
if user_query := st.chat_input("Enter a scripture, word, or theological question..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing manuscripts and canonical context..."):
            try:
                formatted_contents = []
                for msg in st.session_state.messages:
                    formatted_contents.append(f"{msg['role'].upper()}: {msg['content']}")
                
                # Using the rock-solid, production-stable 1.5 endpoint
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents="\n".join(formatted_contents),
                    config={
                        'system_instruction': system_prompt
                    }
                )
                assistant_reply = response.text
            except Exception as e:
                assistant_reply = f"Error executing query: {str(e)}"
            
            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
