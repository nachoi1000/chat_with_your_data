import streamlit as st
from streamlit.web import bootstrap
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
import utils, shutil
import secret_keys
from config import gpt_model
from logging_chat import logger


def get_conversation_chain(vectorstore, gpt_model):
    llm = ChatOpenAI(model = gpt_model,
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
            logger.info(f"User question: {message.content}")
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            logger.info(f"Bot response: {message.content}")
            


def main():
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
        files = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # Initiaze embeddings.
                embedding = utils.initialize_embeddings()
                # Delete vectorstore folder information
                shutil.rmtree('db')

                for file in files:
                    # get pdf text
                    raw_text = utils.get_pdf_text(file)

                    # get the text chunks
                    text_chunks = utils.generate_chunks(raw_text)

                    # create vector store
                    vectorstore = utils.generate_vectorstore(text_chunks, embeddings=embedding)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

        if st.button("Reset"):
            st.rerun()

def execute():
    real_script = 'main.py'
    bootstrap.run(real_script, f'run.py {real_script}', [], {})

if __name__ == '__main__':
    execute()


