from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import streamlit as st
import logging
import sys

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
# response = query_engine.query("How does SRS Solar work?")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# Streamlit app
st.title("SATORI BOT")

# User input
user_input = st.text_input("Enter your message:", "")

# Button to trigger response
if st.button("Send"):
    if user_input:
        with st.spinner("Processing..."):
            try:
                # Get the response from OpenAI
                response = query_engine.query(user_input)
                st.success(response)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a message.")
# print(response)