import streamlit as st
# from PIL import Image
# import cv2

st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Hi I am ..... and I am developed by team Island to extract and interact with the data from the revit model.')

st.sidebar.success('select a page above.')



# img = cv2.imread('team.jpeg')
# st.image(
#     img,
#     caption='Team Island 2024',
#     width=600,
#     channels='BGR'
# )
