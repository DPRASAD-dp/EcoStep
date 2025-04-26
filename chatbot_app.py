import streamlit as st
from chatbot.llm_utils import get_llm_response, get_decision_from_llm, parse_llm_decision, run_sql, format_sql_results
import sqlite3

# Database settings
DB_PATH = "ocr_results.db"

# --- Connect to SQLite ---
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# --- Streamlit App ---
st.title("EcoStep Chatbot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display conversation history
for msg in st.session_state['messages']:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get raw LLM decision
            llm_response = get_decision_from_llm(prompt)
            
            # Parse the response
            mode, payload = parse_llm_decision(llm_response)
            
            # Process according to mode
            if mode == "SQL":
                try:
                    # Run SQL but don't show it to user
                    sql_results = run_sql(payload, cursor)
                    
                    # Pass results back to LLM for formatting
                    content = format_sql_results(prompt, sql_results)
                except Exception as e:
                    content = f"I'm having trouble accessing that information right now."
            else:
                content = payload
            
            # Display and store response
            st.markdown(content)
            st.session_state['messages'].append({"role": "assistant", "content": content})
