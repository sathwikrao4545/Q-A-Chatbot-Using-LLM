import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print("API Token Loaded Successfully:", api_token[:5] + "..." + api_token[-5:])

# Ensure the OpenAI API key is loaded correctly
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is missing. Please check your .env file or environment variables.")
    st.stop() 
    
  
     # Stop execution if the API key is not found

# Initialize the OpenAI model
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.6)

# Streamlit UI Setup
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat!")

# Initialize session state if not already set
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [SystemMessage(content="You are a helpful AI assistant")]

# Function to get a response from the OpenAI model
def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = llm(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

# Streamlit input and button
user_input = st.text_input("Enter your message:", key="input")
submit = st.button("Ask")

# Display the response when the button is clicked
if submit:
    if user_input:
        response = get_chatmodel_response(user_input)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please enter a message.")
