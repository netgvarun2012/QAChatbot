# Document Annalyzer

Upload a document and the app let's you ask questions related to it.

# DOCUMENT ANALYZER GEN-AI APP - *INTELLIGENT DOCUMENT ANALYZER CHATBOT*

Check out the app at [https://questionansweringbot.streamlit.app/](https://questionansweringbot.streamlit.app/)

**UserName: admin**

**Password: admin**

# Table of Contents
  * [Introduction](#introduction)
  * [Demo Videos](#demos)
  * [Setup and Requirements](#installation)
  * [Features](#features)
  * [Architectural considerations](#architecture)
  * [Highlights](#highlight)

# Introduction <a id="introduction"></a>

This repository details the technical and functional aspects of *'Document Analyzer'* app - an Intelligent chatbot ssistant that allows users to upload documents in *pdf,txt and doc* format and then ask questions based on them!
By default, it answers questions pertaining to Topical Chat dataset from Amazon! It consists of over 8000 conversations and over 184000 messages.

Under the hood this app utilized state of the art models - Langchain and Language Models (LLMs) to create a chat interface where users can ask questions and receive responses. 


# Recorded Demos <a id="demos"></a>


# Setup and Requirements <a id="installation"></a>

For a list of required python packages see the *requirements.txt*
or just install them all at once using pip:
```
pip install -r requirements.txt
```

# Features <a id="features"></a>:
- **Vector Database and Langchain**:

Langchain is a library that deals with natural language processing and AI model integration.
It uses a Vector Database (referred to as vectorstore) to store and manage embeddings (numerical representations) of text data. This database allows for efficient retrieval of similar documents or responses based on the input question.

- **Initialization**:

When the application starts, it initializes the Langchain components, including a conversational retrieval chain (qa) and a Language Model (LLM) using GPT-3.5 Turbo.

- **Loading Files**:

The code loads text data files (e.g., PDFs, DOCX, TXT) either from the current directory or from files uploaded by the user.
It preprocesses the text data by splitting it into chunks and creating embeddings for each chunk.
The processed data, including the document chunks and embeddings, is stored in the processed_data session state variable for reuse. This optimization avoids reprocessing files on every interaction.

- **Chat Interface**:

The application provides a chat-like interface where users can input questions or messages.
When the user enters a question, it appends the question to the chat history and displays it in the chat interface.

- **Querying the Assistant**:

The code uses the qa (ConversationalRetrievalChain) to query the assistant with the user's question.
It constructs a query that includes the current question and the chat history (messages exchanged so far) to maintain context.
The assistant uses GPT-3.5 Turbo to generate a response based on the query.

- **Displaying the Response**:

The assistant's response is obtained from the qa query result.
It appends the response to the chat history and displays it in the chat interface.
The response is also displayed in the Streamlit app's main content.

# Architectural considerations <a id="architecture"></a>:
The provided app follows a web application architecture that combines client-side and server-side components. Below, I'll outline the key architectural components and their technical specifications:

1. **Client-Side (Frontend)**:
   - **Framework**: Streamlit, a Python library for building web applications, is used for the frontend.
   - **User Interface**: The user interface is created using Streamlit widgets, which include text inputs, buttons, and chat message displays.
   - **Real-Time Interaction**: Streamlit's reactivity allows for real-time updates in the user interface as users interact with the app.
   - **Browser Compatibility**: The app runs in a web browser, and it is compatible with modern web browsers.

2. **Server-Side (Backend)**:
   - **Python**: The backend is developed in Python, and it hosts the core application logic.
   - **Web Server**: Streamlit includes an integrated web server, so there's no need for a separate web server software.
   - **Session State Management**: Streamlit's session state management is used to preserve user data and interactions between different sessions.
   - **Concurrency**: Streamlit handles concurrency automatically, allowing multiple users to interact with the app simultaneously.
   - **File Handling**: Python is used for file handling, including reading, saving, and processing text data files.
   - **External Service Integration**: The app integrates with external services such as the OpenAI API for natural language processing.

3. **Authentication and Security**:
   - **User Authentication**: The app features basic user authentication where users must enter a username and password to access it.
   - **Secured Secrets**: Sensitive information, such as API keys and user credentials, is managed securely,  through Streamlit's `secrets.toml` configuration file.

4. **Data Processing**:
   - **Text Preprocessing**: The app processes text data, including PDF, DOCX, and TXT files, by splitting them into chunks and creating embeddings.
   - **Vector Database**: Langchain's Vector Database (`vectorstore`) efficiently manages embeddings and allows for efficient document retrieval.

5. **External API Integration**:
   - **OpenAI Integration**: The app integrates with the OpenAI API, using an API key for access. It leverages the GPT-3.5 Turbo model for natural language understanding and generation.

6. **SOTA Models**:
   - **GPT 3.5**: GPT-3.5 Turbo excels in understanding natural language input from users. It can interpret questions, requests, and messages provided by users in conversational contexts.
   - **LangChain**: LangChain is a framework designed to simplify the creation of applications using large language models (LLMs)1. It offers a suite of tools, components, and interfaces that allow developers to build LLM applications. 

7. **Scalability and Efficiency**:
   - **File Upload Handling**: The app can efficiently handle multiple uploaded files and process them, making it scalable for larger datasets.
   - **Caching**: Processed data is cached in session state to reduce redundant processing and improve efficiency.

At a highlevel, the architecture of the app combines modern web technologies, Python, Streamlit, and external API integration to provide a user-friendly and efficient platform for chat-based interactions and document analysis.


# Highlights <a id="highlights"></a>:

1. **Deployment**:
   - **Streamlit**: The code is built using Streamlit, a popular Python library for creating web applications. Streamlit simplifies deployment by allowing you to turn data scripts into shareable web apps with minimal effort.

2. **Security**:
   - **User Authentication**: The code includes a basic user authentication mechanism where users need to enter a username and password to access the application. This adds a layer of security to restrict access to authorized users.

3. **Efficiency**:
   - **Preprocessing and Caching**: The code efficiently preprocesses text data files, splits them into chunks, and creates embeddings. It also caches processed data in the session state, reducing the need for repeated processing and improving application efficiency.

4. **Performance**:
   - **Langchain and Vector Database**: Langchain and the Vector Database (referred to as `vectorstore`) contribute to efficient document retrieval and chatbot responses. The use of embeddings and document chunks can improve the performance of similarity searches and text retrieval.

5. **Scalability**:
   - The code can handle multiple uploaded files and process them efficiently, making it scalable for larger datasets.

6. **User Experience**:
   - The chat-like interface provides a user-friendly experience, allowing users to interact with the AI model in a conversational manner.

7. **Maintenance and Extensibility**:
   - The code is organized into functions and follows best practices, making it easier to maintain and extend with additional features in the future.

8. **Integration with Language Models**:
   - The code integrates with OpenAI's GPT-3.5 Turbo, a powerful language model, for generating responses to user questions. This integration leverages the model's capabilities for natural language understanding and generation.

9. **Flexibility**:
   - Users can upload various types of text files (PDFs, DOCX, TXT), increasing the application's flexibility and usability.

10. **Information Security**:
    - The code accesses sensitive information (secrets) from a `secrets.toml` file and manages user credentials. Ensuring that this file is appropriately secured is essential for information security.

11. **Browser Refresh Mechanism**:
    - The code provides guidance to users to refresh the browser after uploading new files. This mechanism helps reset the session state and ensures that the latest uploaded files are processed correctly.

12. **Authentication and Authorization**:
    - The code performs user authentication but does not appear to have an authorization mechanism in place. Depending on your application's requirements, you may want to implement authorization to restrict access to specific functionalities or data.

13. **OpenAI API Integration**:
    - The code integrates with the OpenAI API using an API key. API keys should be kept secure and managed properly to ensure the security of API interactions.

14. **Optimization Opportunities**:
    - Depending on the expected usage patterns and user load, there may be optimization opportunities in terms of caching, response times, and resource utilization.




 Note: Please note that this is a prototype. Model's capabilities can be improved with more time and resources.

