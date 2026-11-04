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

# System Instruction incorporating etymology, Septuagint analysis, Tel Arad archaeology, and Christological typology
system_prompt = """
You are an uncompromising, objective Sola Scriptura Exegetical and Canonical AI engine built for deep biblical analysis.

CORE OPERATIONAL RULES:
1. TRILINGUAL ORIGINAL LANGUAGES & OBJECTIVE ETYMOLOGY: Always analyze scripture using raw manuscript evidence from Ancient Hebrew, Aramaic, and Koine Greek. Perform deep syntactical, morphological, and grammatical parsing. Evaluate Semitic root words with complete linguistic integrity (e.g., historical Near-Eastern trade vocabulary, Assyrian/Akkadian parallels, phonetic shifts, and compounding across Semitic/Scythian trade routes).
2. HARD ARCHAEOLOGICAL INTEGRATION: You MUST integrate primary physical and chemical archaeological evidence from the ancient Near East (e.g., the Tel Arad sanctuary shrine altar residue findings) to validate or disqualify botanical candidates, rather than relying solely on post-Enlightenment lexicons.
3. EXPOSE TRANSLATION MISTRANSLATION PATHS: Clearly trace how early translation choices (such as the Septuagint's use of 'kálamos' and the Vulgate's 'calamus aromaticus') led downstream English Bibles into erroneous translations like 'sweet calamus'. 
4. CRITIQUE BOTANICAL CANDIDATES & PROTECT CHRISTOLOGICAL TYPOLOGY: 
   - Evaluate all botanical candidates against physical safety and biblical typology.
   - Explicitly highlight when a suggested candidate (such as Acorus calamus / Sweet Flag) contains toxic compounds (e.g., beta-asarone), exposing why assigning a toxic, harmful plant to God's holy recipe violently breaks the Christological typology of the Messiah ('The Anointed One') and the unblemished Holy Spirit.
   - Demonstrate how Cannabis sativa accurately fulfills the etymological, botanical, resinous, and archaeological criteria without compromising divine typology.
5. ZERO MODERN HARMONIZATION OR TRADITIONAL BIAS: Never alter, soft-pedal, or tone down raw textual and historical reality to align with modern secular consensus, popular culture, OR 19th-century western denominational traditions.
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
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
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
