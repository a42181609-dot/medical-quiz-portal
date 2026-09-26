import streamlit as st
import pandas as pd
import os

# Session States ko shuru karna navigation aur features ke liye
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0

st.title("🩺 Medical MCQs Big Data Portal (400 MCQs Framework)")
st.write("Excel/CSV Data Bank se automatic load hone wali advanced test app with Voice Features.")

# CSV file read karne ka logic
csv_file = "medical_data.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file, on_bad_lines='skip')
else:
    st.error("⚠️ Error: 'medical_data.csv' file nahi mili! Pehle CSV file banayein.")
    st.stop()

# --- SEARCH & VOICE SYSTEM ---
st.markdown("### 🔍 Search Panel")
col_src, col_mic = st.columns([4, 1])

with col_src:
    search_query = st.text_input("Subject Search (anatomy, physiology, pharmacology, pharmaceutics):", key="search_input").lower().strip()

with col_mic:
    st.write("") # Spacing adjustment
    voice_trigger = st.button("🎤 Voice Search Active")

# Voice feature trigger ka system logic alert
if voice_trigger:
    st.info("🎙️ Voice search simulator active: Apne browser settings mein 'Microphone Access' allow karein ya 'Windows Key + H' daba kar direct text box mein bolein.")

# Voice text processing logic settings matching
if "pharmaceutics" in search_query:
    st.session_state.page = 4
    st.session_state.q_index = 0
elif search_query == "anatomy":
    st.session_state.page = 1
    st.session_state.q_index = 0
elif search_query == "physiology":
    st.session_state.page = 2
    st.session_state.q_index = 0
elif search_query == "pharmacology":
    st.session_state.page = 3
    st.session_state.q_index = 0

# Page Routing setup for 4 subjects
if st.session_state.page == 1:
    current_subject = "anatomy"
    display_title = "🦴 Page 1: Anatomy (Insani Jism)"
elif st.session_state.page == 2:
    current_subject = "physiology"
    display_title = "🫁 Page 2: Physiology (Afaal-e-Aza)"
elif st.session_state.page == 3:
    current_subject = "pharmacology"
    display_title = "💊 Page 3: Pharmacology (Adviyat)"
else:
    current_subject = "pharmaceutics"
    display_title = "🧪 Page 4: Pharmaceutics (Dawa Sazi)"

st.header(display_title)

# Filter questions based on current subject
filtered_df = df[df['subject'].str.lower().str.strip() == current_subject]
total_questions = len(filtered_df)

if total_questions == 0:
    st.warning(f"Is subject '{current_subject}' ke liye abhi CSV file mein koi sawalat nahi hain. Meharbani karke CSV file check karein.")
else:
    # --- VIEW MODE SYSTEM ---
    view_mode = st.radio("🧐 Dikhane ka Tareeqa (View Mode):", ["Ikhtay (Saare sawal ek sath)", "Aik Aik Sawal (Single Mode)"], horizontal=True)

    # Convert rows to list format for active processing
    mcqs_list = []
    for index, row in filtered_df.iterrows():
        mcqs_list.append({
            "q": row['question'],
            "o": [str(row['option1']), str(row['option2']), str(row['option3']), str(row['option4'])],
            "a": str(row['answer'])
        })

    # --- MODE 1: IKHTAY (ALL MCQS TOGETHER) ---
    if view_mode == "Ikhtay (Saare sawal ek sath)":
        score = 0
        user_answers = {}
        for i, mcq in enumerate(mcqs_list):
            st.markdown(f"--- \n**Q{i+1}: {mcq['q']}**")
            user_answers[i] = st.radio(f"Options for Q{i+1}", mcq['o'], key=f"all_{current_subject}_{i}", label_visibility="collapsed")
            if user_answers[i] == mcq['a']:
                score += 1
                
        st.markdown("---")
        if st.button("Submit This Page Test 🎯", key="submit_all"):
            st.balloons()
            st.success(f"Aapne is page par {total_questions} mein se **{score}/{total_questions}** sawal sahi kiye!")

    # --- MODE 2: AIK AIK SAWAL (SINGLE MCQ MODE) ---
    else:
        q_idx = st.session_state.q_index
        if q_idx >= total_questions:
            st.session_state.q_index = 0
            q_idx = 0
            
        mcq = mcqs_list[q_idx]
        
        st.markdown(f"--- \n### Sawal {q_idx + 1} of {total_questions}")
        st.subheader(mcq['q'])
        
        user_choice = st.radio("Sahi jawab chunein:", mcq['o'], key=f"single_{current_subject}_{q_idx}")
        
        if st.button("Jawab Check Karein ✔️"):
            if user_choice == mcq['a']:
                st.success("🎉 Bilkul Sahi Jawab!")
            else:
                st.error(f"❌ Galat Jawab! Sahi jawab yeh tha: **{mcq['a']}**")
                
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if q_idx > 0:
                if st.button("⬅️ Pichla Sawal"):
                    st.session_state.q_index -= 1
                    st.rerun()
        with col_q2:
            if q_idx < (total_questions - 1):
                if st.button("Agla Sawal ➡️"):
                    st.session_state.q_index += 1
                    st.rerun()
            else:
                st.info("Aapne is subject ke saare sawal dekh liye hain! Niche se agla page badlein.")

# --- MAIN PAGE NAVIGATION BUTTONS ---
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.session_state.page > 1:
        if st.button("⬅️ Go to Previous Subject Page", key="prev_page"):
            st.session_state.page -= 1
            st.session_state.q_index = 0
            st.rerun()

with col2:
    if st.session_state.page < 4:
        if st.button("Go to Next Subject Page ➡️", key="next_page"):
            st.session_state.page += 1
            st.session_state.q_index = 0
            st.rerun()