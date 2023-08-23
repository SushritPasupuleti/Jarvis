from langchain.document_loaders import WebBaseLoader
from main import hf
import torch

web_links = [
    "https://help.braggi-ems.com/", 
    "https://help.braggi-ems.com/leader_home", 
    "https://help.braggi-ems.com/modules",
    "https://help.braggi-ems.com/modules/voter_marking",
    "https://help.braggi-ems.com/modules/voter_identification",
    "https://help.braggi-ems.com/modules/house_number_marking",
    "https://help.braggi-ems.com/modules/house_number_marking_plus",
    "https://help.braggi-ems.com/modules/leader_management",
    "https://help.braggi-ems.com/modules/reports",
    "https://help.braggi-ems.com/modules/polling_day",
    # "https://help.braggi-ems.com/privacy_policy",
    # "https://help.braggi-ems.com/terms_of_service",
] 

loader = WebBaseLoader(web_links)
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
all_splits = text_splitter.split_documents(documents)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": device}

embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

# storing embeddings in the vector store
vectorstore = FAISS.from_documents(all_splits, embeddings)

from langchain.chains import ConversationalRetrievalChain

chain = ConversationalRetrievalChain.from_llm(hf, vectorstore.as_retriever(), return_source_documents=True)

chat_history = []

query = "Tell me about the modules in Braggi EMS."
result = chain({"question": query, "chat_history": chat_history})

print("Answer: ", result['answer'])
print("\n\n ============================ \n\n")
print("Source: ", result['source_documents'])
