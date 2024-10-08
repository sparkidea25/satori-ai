from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import streamlit as st
# from fastapi import FastAPI, Form, Depends, Request
from flask import Flask, request, jsonify
import logging
import sys
from twilio.rest import Client
# from decouple import config
import os

# app = FastAPI()
app = Flask(__name__)


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# config("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
# config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.environ.get("TWILIO_NUMBER")
# config('TWILIO_NUMBER')

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
# response = query_engine.query("How does SRS Solar work?")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'


# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")
        
        
@app.route('/message', methods=['POST'])
def bot():
    incoming_msg = request.values['Body']
    phone_number = (request.values['WaId'])

    if incoming_msg:
        chat_log = session.get('chat_log')
        answer = query_engine.query(incoming_msg)
        session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        sendMessage(answer, phone_number)
        print(answer)
    else:
        sendMessage("Message Cannot Be Empty!")
        print("Message Is Empty")
    r = MessagingResponse()
    r.message("")        
    return str(r)


host="0.0.0.0"
port=8002
app_name="app.ma:app"

# if __name__ == '__starter__':
#     uvicorn.run(app_name, host=host, port=port)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


# if __name__ == '__main__':
#     app.run()
        

# # Streamlit app
# st.title("SATORI BOT")

# # User input
# user_input = st.text_input("Enter your message:", "")

# # Button to trigger response
# if st.button("Send"):
#     if user_input:
#         with st.spinner("Processing..."):
#             try:
#                 # Get the response from OpenAI
#                 response = query_engine.query(user_input)
#                 st.success(response)
#             except Exception as e:
#                 st.error(f"Error: {e}")
#     else:
#         st.warning("Please enter a message.")
# print(response)