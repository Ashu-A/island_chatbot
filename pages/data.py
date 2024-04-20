import streamlit as st

st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)

header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Page under development')


# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team
    """
)
