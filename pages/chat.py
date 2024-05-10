import streamlit as st
from specklepy.api import operations
from specklepy.transports.server import ServerTransport
import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
from specklepy.api.client import SpeckleClient
from specklepy.api import operations
from dotenv import load_dotenv
import os
from specklepy.api.credentials import get_default_account, get_local_accounts

st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Page under development')

# Load the .env file
load_dotenv()


# functions
def chat_speckle(df, prompt):
    openai_api_token = os.getenv("OPENAI_API_TOKEN")
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


# containers
header = st.container()
input_container = st.container()
viewer = st.container()
report = st.container()
data_extraction = st.container()

# Inputs
with input_container:
    st.subheader('Inputs')

    speckleServer = st.text_input('Speckle Server', 'https://speckle.xyz')
    speckleToken = st.text_input('Speckle Token', '')

    commits = None  # Initialize commits variable

    if not speckleToken:
        st.error("Please enter your valid Speckle Token.")

    else:
        # Authentication
        client = SpeckleClient(host="https://speckle.xyz")
        account = get_default_account()

        try:
            client.authenticate(token=speckleToken)
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

            # Continue with the rest of the code for data extraction
        except Exception as e:
            st.error(f"Error: {e}")

# Data extraction
with data_extraction:
    st.subheader('Data Extraction')

    if commits:
        commit_data = None
        for commit in commits:
            if getattr(commit, "branchName", None) == bName:
                transport = ServerTransport(stream.id, client)
                obj_id = commit.referencedObject
                commit_data = operations.receive(obj_id, remote_transport=transport)
                if commit_data:
                    break

        if commit_data:
            selected_category = st.selectbox("Select category", commit_data.get_dynamic_member_names())

            parameters = commit_data[selected_category][0]["parameters"].get_dynamic_member_names()

            form = st.form("parameter_input")
            with form:
                selected_parameters = st.multiselect("Select Parameters",
                                                     get_parameter_names(commit_data, selected_category))
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
                st.info("How can I help you today?")
                OPENAI_API_KEY = st.text_input('OpenAI key', "sk-...vDlY")
                input_text = st.text_area('Enter your query')
                if input_text is not None:
                    if st.button("Send"):
                        st.info('Your query:' + input_text)
                        result = chat_speckle(result_DF, input_text)
                        # result = ("The manufacturer of the beam is Bamgrove")
                        st.success(result)
        else:
            st.warning("No data available for the selected branch.")

# Footer
st.markdown(
    """
    ---

    Made with ❤️ by Island Team
    """
)
