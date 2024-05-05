import streamlit as st


st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Hi I am SEPI a virtual assistant for Island Team')
st.image('team.jpeg', caption='Team Island 2024', width=600)
# st.sidebar.success('select a page above.')


# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team
    """
)
