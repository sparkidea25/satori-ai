import os
import tempfile
import requests
from dotenv import load_dotenv
from twilio.rest import Client
from pypdf import PdfReader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from flask import Flask, request
# from flask import request

app = Flask(__name__)

# Define the path to the specific PDF file
PDF_FILE_PATH = 'Satori AI - SRS Solar Knowledgebase v0.3 Combined with Pricing.pdf'

# Flag to check if PDF exists
pdf_exists = False
VectorStore = None


@app.route('/message', methods=['POST'])
def whatsapp():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    response = None
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    sender_phone_number = request.values.get('From', '')
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
        question = request.values.get('Body')
        if pdf_exists:
            docs = VectorStore.similarity_search(query=question, k=3)
            llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.4)
            chain = load_qa_chain(llm, chain_type="stuff")
            answer = chain.run(input_documents=docs, question=question)
            message = client.messages.create(
                body=answer,
                from_=twilio_phone_number,
                to=sender_phone_number
            )
            return str(message.sid)

    else:
        response = "The media content type is not application/pdf or PDF file not found."

    message = client.messages.create(
        body=response,
        from_=twilio_phone_number,
        to=sender_phone_number
    )

    return str(message.sid)


if __name__ == '__main__':
    app.run(debug=True)