import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import DirectoryLoader
from langchain.docstore.document import Document
from streamlit import secrets
import hashlib
import os
import openai
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get the username and password from secrets.toml
username = secrets["authentication"]["username"]
password = secrets["authentication"]["password"]
# Or get the username and password hash from secrets.toml
username = secrets["authentication"]["username"]
password_hash = secrets["authentication"]["password_hash"]

# Initialize the session state variable
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Create placeholders for the login form widgets using st.empty()
user_input_placeholder = st.empty()
pass_input_placeholder = st.empty()
login_button_placeholder = st.empty()

# Fill the placeholders with the login form widgets
user_input = user_input_placeholder.text_input("Enter your username")
pass_input = pass_input_placeholder.text_input("Enter your password", type="password")
login_button = login_button_placeholder.button("Click me to Login!")


# Validate the user input against the username and password or the password hash
if login_button:
    if user_input == username and pass_input == password:
        # If successful, display a success message
        st.success("Login successful")
        # Set the session state variable to True
        st.session_state.logged_in = True
        # Clear the placeholders to remove the widgets        
    elif user_input == username and hashlib.sha256(pass_input.encode()).hexdigest() == password_hash:
        # If successful, display a success message
        st.success("Login successful")
        # Set the session state variable to True
        st.session_state.logged_in = True
        # Clear the placeholders to remove the widgets   
    else:
        # If not, display an error message
        st.error("Invalid username or password")

# Check the session state variable before displaying the app content
if st.session_state.logged_in:
    # Display your app content after the login form
    st.write("Welcome!")      
    # Continue with the rest of your app here
else:
    # Stop the app from running any further code
    st.stop()

user_input_placeholder.empty()
pass_input_placeholder.empty()
login_button_placeholder.empty()

# relevant messages for the user
st.info("When uploading new files, don't forget to refresh the browser to reset the session :smile: ")

st.header("Chat with me after uploading your files!")
st.subheader('File type supported: PDF/DOCX/TXT :city_sunrise:')

# Setting OPEN AI KEY!
openai_api_key = st.secrets["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = openai_api_key

llm = ChatOpenAI(temperature=0,max_tokens=1000, model_name="gpt-3.5-turbo",streaming=True)

def load_files():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []    
    pdf_loader = DirectoryLoader('./',glob="**/*.pdf")
    txt_loader = DirectoryLoader('./', glob="**/*.txt")
    word_loader = DirectoryLoader('./',glob="**/*.docx")
    loaders = [pdf_loader,txt_loader,word_loader]
    documents = []
    for loader in loaders:
            documents.extend(loader.load())
        
    return documents


def load_app_info():
    '''
    This function loads the app information.
    '''
    with open("app_info.txt", "r") as file:
        return file.read()
       

# else:
#     st.write("Please upload your files

if __name__ == '__main__':
    # load the already present files
    doc = load_files()
    documents=doc # read from the already present files (no need to upload!)
    if "processed_data" not in st.session_state:
        # Chunk the data, create embeddings, and save in vectorstore
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        document_chunks = text_splitter.split_documents(documents)
        # Print the number of total chunks to console
    
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(document_chunks, embeddings)

        # Store the processed data in session state for reuse
        st.session_state.processed_data = {
            "document_chunks": document_chunks,
            "vectorstore": vectorstore,
        }
    else:
        # If the processed data is already available, retrieve it from session state
        document_chunks = st.session_state.processed_data["document_chunks"]
        vectorstore = st.session_state.processed_data["vectorstore"]
    
    # logic for sidebar to upload files
    with st.sidebar:
        uploaded_files = st.file_uploader("Please upload your file here!", accept_multiple_files=True, type=None)
        # Create a container with a fixed height for the version history
        app_info_container = st.container()
        app_info_container.header("Application Information:")
        app_info_container.write(load_app_info())
        if uploaded_files:
            st.session_state.processed_data = {}
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        for uploaded_file in uploaded_files:
            # Get the full file path of the uploaded file
            file_path = os.path.join(os.getcwd(), uploaded_file.name)

            # Save the uploaded file to disk
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
                    
            if file_path.endswith((".pdf", ".docx", ".txt")):
                # Use UnstructuredFileLoader to load the PDF/DOCX/TXT file
                loader = UnstructuredFileLoader(file_path)
                loaded_documents = loader.load()
                # Extend the main documents list with the loaded documents
                documents.extend(loaded_documents)

            # Chunk the data, create embeddings, and save in vectorstore
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        document_chunks = text_splitter.split_documents(documents)
            # Print the number of total chunks to console
        
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(document_chunks, embeddings)
        
        # Store the processed data in session state for reuse
        st.session_state.processed_data = {
            "document_chunks": document_chunks,
            "vectorstore": vectorstore,
        }
        #else:
            # If the processed data is already available, retrieve it from session state
        #    document_chunks = st.session_state.processed_data["document_chunks"]
        #    vectorstore = st.session_state.processed_data["vectorstore"]

    # Initialize Langchain's QA Chain with the vectorstore
    qa = ConversationalRetrievalChain.from_llm(llm,vectorstore.as_retriever())
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
                
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])    
            
    # Accept user input
    if prompt := st.chat_input("Ask your questions?"):
    # Display chat messages from history on app rerun    
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Query the assistant using the latest chat history
        result = qa({"question": prompt, "chat_history": [(message["role"], message["content"]) for message in st.session_state.messages]})
    
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response = result["answer"]
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)    
        print(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
