import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.chat_models import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is loaded
if not openai_api_key:
    st.error("API key not found. Please set OPENAI_API_KEY in your .env file.")
    st.stop()

# Initialize OpenAI model
llm = ChatOpenAI(api_key=openai_api_key, temperature=0.6)

# Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat!")

# Initialize session state
if "flowmessages" not in st.session_state:
    st.session_state["flowmessages"] = [SystemMessage(content="You are a helpful AI assistant.")]

# Function to get chatbot response
def get_chatmodel_response(question):
    st.session_state["flowmessages"].append(HumanMessage(content=question))
    answer = llm.invoke(st.session_state["flowmessages"])
    st.session_state["flowmessages"].append(AIMessage(content=answer.content))
    return answer.content

# User input
user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask")

# Display response
if submit and user_input:
    response = get_chatmodel_response(user_input)
    st.subheader("Response:")
    st.write(response)
