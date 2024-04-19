import streamlit as st
import specklepy
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
from specklepy.api.wrapper import StreamWrapper
from dotenv import load_dotenv
from specklepy.api import operations

st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)

st.title('Island Chatbot')
st.sidebar.success('select a page above.')
