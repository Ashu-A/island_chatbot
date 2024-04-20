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
st.image('team.jpeg', caption='Team Island 2024', width=600)
st.sidebar.success('select a page above.')


# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team developed by [Ashish](https://ashu-a.github.io/ashish_ranjan/)
    """
)
