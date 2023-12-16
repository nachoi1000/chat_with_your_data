import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
import utils
import secret_keys



def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model = "gpt-3.5-turbo",
                     openai_api_base = secret_keys.OPENAI_BASE_URL,
                     openai_api_key = secret_keys.SECONDARY_OPENAI_KEY)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            


def main():
    #load_dotenv()
    embeddings = utils.initialize_embeddings()
    
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                print(pdf_docs)
                print(type(pdf_docs))
                raw_text = utils.get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = utils.generate_chunks_2(raw_text)

                # Initiaze embeddings.
                embedding = utils.initialize_embeddings()

                # create vector store
                vectorstore = utils.generate_vectorstore(text_chunks, embeddings=embedding)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

        if st.button("Reset"):
            st.rerun()
if __name__ == '__main__':
    main()


