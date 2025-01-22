import os

import logfire
import streamlit as st
from configs.config import Config
from configs.logger import Logger
from templates.singleton import Singleton
from utils import response_generator

# ----------
# DESC: config the Logger
logger = Logger().get_logger()
# ----------

# -----DESC: Logfire Config-----
logfire.configure(
    token=os.environ.get('LOGFIRE_PROJECT_TOKEN', ''),
)
# ------------------------------


class ScientificAssistantChat(Singleton):
    def __init__(self, *, subtitle: str = 'Chat', config: Config):
        self._config = config
        self._subtitle = subtitle
        self._set_subtitle()
        self._start_chat_history()
        self._set_chat_history()
        self._start_chat()

    def _set_subtitle(self):
        st.subheader(self._subtitle)

    def _start_chat_history(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def _set_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    def _start_chat(self):
        # Accept user input
        if question := st.chat_input('Olá, bom dia!'):
            # -------------------------
            # BLOCO INICIAL

            # DESC: Add user message to chat history
            st.session_state.messages.append({'role': 'user', 'content': question})

            # DESC: Display user message in chat message container
            with st.chat_message('user'):
                st.markdown(question)

            response = response_generator(
                question=question, config=self._config, prompt_type='start'
            )

            logger.info('-' * 50)
            logger.info('RESPONSE - STEP 1')
            logger.info(f'{response["response"]}')
            logger.info('-' * 50)
            logfire.info(f'response - step 1: {response["response"]}')

            # -------------------------

            # -------------------------
            # BLOCO ESPECÍFICO

            # DESC: verificação de conectividade com a API de RAG
            if response['status'] != 200:
                response = response['description']

                with st.chat_message('assistant'):
                    st.markdown(response)
            else:
                with st.chat_message('assistant'):
                    st.markdown('...')

                if (
                    response['response'].get('category')
                    == 'Computer science scientific article'
                ):
                    # DESC: Filtered response
                    response = response_generator(
                        question=question, config=self._config, prompt_type='filtered'
                    )['response']

                else:
                    # DESC: Generic response
                    response = response_generator(
                        question=question, config=self._config, prompt_type='end'
                    )['response']

                    response = f"""
                    Olá!, eu adoraria ajudar você com suas perguntas sobre este tema: {response["topic"].upper()}.
                    Infelizmente, não consigo responder a outros tópicos que não estejam contidos em minha
                    base de dados e não sejam sobre Artigos Científicos. Por favor, tente novamente realizar uma
                    pergunta sobre artigos científicos!
                    """

                with st.chat_message('assistant'):
                    st.markdown(response)

                logger.info('-' * 50)
                logger.info('RESPONSE - STEP 2')
                logger.info(f'{response}')
                logger.info('-' * 50)
                logfire.info(f'response - step 2: {response}')

            # -------------------------

            # Add assistant response to chat history
            st.session_state.messages.append({'role': 'assistant', 'content': response})
