import streamlit as st
st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Hi I am SEPI a virtual assistant for Island Team')

def embed_powerbi_dashboard(embed_link):
    if embed_link.startswith("<iframe"):
        st.markdown(embed_link, unsafe_allow_html=True)
    else:
        st.write("Please enter a valid Power BI embed link.")

def main():
    st.title('Power BI Dashboard')
    st.write("Enter your Power BI embed link below:")
    embed_link = st.text_input("Power BI Embed Link", value='<iframe title="Island(The Body)" width="800" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiNzgzOGY4NmMtNzEyYi00NzE5LWE4NDUtOGZmZjZmZGM4MGM0IiwidCI6IjgwNjBmMmQ0LTI3NTMtNGQ2OS04NTJhLTc0NWZiYTRiNTZlOCJ9" frameborder="0" allowFullScreen="true"></iframe>', help="Paste your Power BI embed link here.")
    st.write("Here's your Power BI dashboard:")
    embed_powerbi_dashboard(embed_link)

if __name__ == "__main__":
    main()


# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team
    """
)
