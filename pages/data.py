import streamlit as st

st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Page under development')



import streamlit as st
import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
from specklepy.api.client import SpeckleClient
from specklepy.api import operations
from dotenv import load_dotenv
import os
from specklepy.api.credentials import get_default_account, get_local_accounts

# Load the .env file
load_dotenv()

# functions
def chat_speckle(df, prompt):
    openai_api_token = os.getenv('OPENAI_API_TOKEN')
    llm = OpenAI(api_token=openai_api_token)
    df = SmartDataframe(df, config={"llm": llm})
    result = df.chat(prompt)
    return result


# get parameter names
def get_parameter_names(commit_data, selected_category):
    parameters = commit_data[selected_category][0]["parameters"].get_dynamic_member_names()
    parameters_names = []
    for parameter in parameters:
        parameters_names.append(commit_data[selected_category][0]["parameters"][parameter]["name"])
    parameters_names = sorted(parameters_names)
    return parameters_names


# get parameter value by parameter name
def get_parameter_by_name(element, parameter_name, dict):
    for parameter in parameters:
        key = element["parameters"][parameter]["name"]
        if key == parameter_name:
            dict[key] = element["parameters"][parameter]["value"]
    return dict

# Page configuration
# st.set_page_config(
#     page_title="Island Chatbot",
#     page_icon="🏝️",
# )

# containers
header = st.container()
input_container = st.container()
viewer = st.container()
report = st.container()
data_extraction = st.container()

# Header
with header:
    st.title('Island Chatbot')
    st.info('Page under development.')

# Inputs
with input_container:
    st.subheader('Inputs')

    speckleServer = st.text_input('Speckle Server', 'https://speckle.xyz')
    speckleToken = st.text_input('Speckle Token', '1c85ef40568298221924a2feca4e1eb2c42bf0c3a6')

    # Authentication
    client = SpeckleClient(host="https://speckle.xyz")
    account = get_default_account()
    client.authenticate(token='1c85ef40568298221924a2feca4e1eb2c42bf0c3a6')
    client.authenticate()

    streams = client.stream.list()
    streamNames = [s.name for s in streams]
    sName = st.selectbox('Select Stream', options=streamNames)

    stream = client.stream.search(sName)[0]
    branches = client.branch.list(stream.id)
    branchNames = [b.name for b in branches]

    if len(branchNames) > 1:
        bName = st.selectbox('Select Branch', options=branchNames)
    else:
        bName = branchNames[0] if branchNames else None

    commits = client.commit.list(stream.id, limit=100)

# Data extraction
with data_extraction:
    st.subheader('Data Extraction')

    if commits:
        commit_data = None
        for commit in commits:
            if getattr(commit, "branchName", None) == bName:
                obj_id = branch.commits.items[0].referencedObject
                commit_data = operations.receive(obj_id=obj_id, remote_transport=client)
                if commit_data:
                    break

        if commit_data:
            selected_category = st.selectbox("Select category", commit_data.get_dynamic_member_names())

            parameters = commit_data[selected_category][0]["parameters"].get_dynamic_member_names()

            form = st.form("parameter_input")
            with form:
                selected_parameters = st.multiselect("Select Parameters", get_parameter_names(commit_data, selected_category))
                run_button = st.form_submit_button('RUN')

            category_elements = commit_data[selected_category]

            result_data = []
            for element in category_elements:
                dict = {}
                for s_param in selected_parameters:
                    get_parameter_by_name(element, s_param, dict)
                result_data.append(dict)
            result_DF = pd.DataFrame.from_dict(result_data)

            col1, col2 = st.columns([1, 1])
            with col1:
                result = st.dataframe(result_DF)

            with col2:
                st.info("⬇️chatSpeckle⬇️")
                OPENAI_API_KEY = st.text_input('OpenAI key', "sk-...vDlY")
                input_text = st.text_area('Enter your query')
                if input_text is not None:
                    if st.button("Send"):
                        st.info('Your query:' + input_text)
                        result = chat_speckle(result_DF, input_text)
                        st.success(result)
        else:
            st.warning("No data available for the selected branch.")


# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team developed by [Ashish](https://ashu-a.github.io/ashish_ranjan/)
    """
)
