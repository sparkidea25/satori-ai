from flask import Flask, request
import requests
import os
import openai
from twilio.twiml.messaging_response import MessagingResponse
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from twilio.rest import Client
from pypdf import PdfReader
# from PyPDF2 import PdfReader

app = Flask(__name__)

load_dotenv() 
PDF_FILE_PATH = 'Satori AI - SRS Solar Knowledgebase v0.3 Combined with Pricing.pdf'

# Flag to check if PDF exists
pdf_exists = False
VectorStore = None


# @app.route('/message', methods=['POST'])
# def whatsapp():
#     load_dotenv()
    
#     # Load API keys and credentials from environment variables
#     OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#     account_sid = os.getenv('TWILIO_ACCOUNT_SID')
#     auth_token = os.getenv('TWILIO_AUTH_TOKEN')
#     client = Client(account_sid, auth_token)
#     twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
#     sender_phone_number = os.getenv('TWILIO_SEND_NUMBER')
    
#     media_content_type = request.values.get('MediaContentType0')
#     response = MessagingResponse()

#     # Check if the PDF file is available or if it's being uploaded via WhatsApp
#     if media_content_type == 'application/pdf' or os.path.exists(PDF_FILE_PATH):
#         global pdf_exists, VectorStore
#         pdf_exists = True
#         with open(PDF_FILE_PATH, 'rb') as pdf_file:
#             pdf = PdfReader(pdf_file)
#             text = ""
#             for page in pdf.pages:
#                 text += page.extract_text()
            
#             # Split the text into manageable chunks
#             text_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=1000,
#                 chunk_overlap=200,
#                 length_function=len
#             )
#             chunks = text_splitter.split_text(text=text)

#             # Generate embeddings for the text
#             embeddings = OpenAIEmbeddings()
#             VectorStore = FAISS.from_texts(chunks, embedding=embeddings)

#     elif pdf_exists:
#         question = request.values.get('Body', '').lower()
#         if question:
#             # Perform similarity search and question-answering
#             docs = VectorStore.similarity_search(query=question, k=3)
#             llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.4)
#             chain = load_qa_chain(llm, chain_type="stuff")
#             answer = chain.run(input_documents=docs, question=question)
            
#             # Respond with the answer
#             response.message(answer)
#         else:
#             response.message("Please ask a question related to the PDF.")
#     else:
#         response.message("The media content type is not application/pdf or the PDF file is not found.")
    
#     return str(response)



@app.route('/message', methods=['POST'])
def whatsapp():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    response = None
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    sender_phone_number = os.getenv('TWILIO_SEND_NUMBER')
    # sender_phone_number = request.values.get('From', '')
    media_content_type = request.values.get('MediaContentType0')
    
    # Check if the PDF file is available
    if media_content_type == 'application/pdf' or os.path.exists(PDF_FILE_PATH):
        global pdf_exists, VectorStore
        pdf_exists = True
        with open(PDF_FILE_PATH, 'rb') as pdf_file:
            pdf = PdfReader(pdf_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    elif pdf_exists:
        # question = request.values.get('Body').lower()
        question = request.values.get('Body', '').lower()
        # incoming_que = request.values.get('Body', '').lower()
        # question = Body
        if pdf_exists:
            docs = VectorStore.similarity_search(query=question, k=3)
            llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.4)
            chain = load_qa_chain(llm, chain_type="stuff")
            answer = chain.run(input_documents=docs, question=question)
            print(answer, 'confirm answer')
            
            bot_resp = MessagingResponse(answer)
            msg = bot_resp.message()
            
            # msg.body(answer)
            
            # return str(msg)
            return msg

    else:
        response = "The media content type is not application/pdf or PDF file not found."

    message = client.messages.create(
        body=response,
        from_=twilio_phone_number,
        to=sender_phone_number
    )


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    # return str(resp)


if __name__ == '__main__':
    app.run(port=4000)