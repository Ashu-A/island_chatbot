import streamlit as st
import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
from specklepy.api.wrapper import StreamWrapper
from specklepy.api.client import SpeckleClient
from specklepy.api import operations
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Functions
def chat_speckle(df, prompt):
    openai_api_token = os.getenv('OPENAI_API_TOKEN')
    llm = OpenAI(api_token=openai_api_token)
    df = SmartDataframe(df, config={"llm": llm})
    result = df.chat(prompt)
    return result

def get_parameter_names(commit_data, selected_category):
    parameters = commit_data[selected_category][0]["parameters"].get_dynamic_member_names()
    parameters_names = [commit_data[selected_category][0]["parameters"][parameter]["name"] for parameter in parameters]
    return sorted(parameters_names)

def get_parameter_by_name(element, parameter_name, dict):
    for parameter in parameters:
        key = element["parameters"][parameter]["name"]
        if key == parameter_name:
            dict[key] = element["parameters"][parameter]["value"]
    return dict

# Containers
header = st.container()
input = st.container()
data = st.container()

# Header
with header:
    st.title('chatSpeckle 🗣️')
    st.info('This web app allows you to chat with your AEC data using Speckle and OpenAI')

# Inputs
with input:
    st.subheader('Inputs 📁')
    commit_url = st.text_input('Commit URL', "https://speckle.xyz/streams/06564bda95/commits/f308ed526e")

# Wrapper
wrapper = StreamWrapper(commit_url)
# Client
client = wrapper.get_client()
# Transport
transport = wrapper.get_transport()

# Get Speckle commit
try:
    commit = client.commit.get(wrapper.stream_id, wrapper.commit_id)
    obj_id = commit.referencedObject
    commit_data = operations.receive(obj_id, transport)
except Exception as e:
    st.error(f"Error retrieving commit data: {e}")
    commit_data = None

if commit_data:
    with input:
        selected_category = st.selectbox("Select category", commit_data.get_dynamic_member_names())

    # Parameters
    parameters = commit_data[selected_category][0]["parameters"].get_dynamic_member_names()

    with input:
        form = st.form("parameter_input")
        with form:
            selected_parameters = st.multiselect("Select Parameters", get_parameter_names(commit_data, selected_category))
            run_button = st.form_submit_button('RUN')

    category_elements = commit_data[selected_category]

    with data:
        st.subheader("Data 📚")
        result_data = []
        for element in category_elements:
            data_dict = {}
            for selected_param in selected_parameters:
                get_parameter_by_name(element, selected_param, data_dict)
            result_data.append(data_dict)
        result_DF = pd.DataFrame.from_dict(result_data)

        # Show dataframe and add chatSpeckle feature
        col1, col2 = st.columns([1, 1])
        with col1:
            st.dataframe(result_DF)

        with col2:
            st.info("⬇️chatSpeckle⬇️")
            openai_api_key = st.text_input('OpenAI key', "sk-...vDlY")

            input_text = st.text_area('Enter your query')
            if st.button("Send"):
                st.info('Your query:' + input_text)
                result = chat_speckle(result_DF, input_text)
                st.success(result)
