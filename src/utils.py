import json
from pathlib import Path

import logfire
import requests
import streamlit as st
from configs.config import Config
from PIL import Image
from requests.exceptions import Timeout


# Streamed response emulator
def response_generator(*, question: str, config: Config, prompt_type: str):
    headers = {'key': config.api_key}

    params = {
        'question': question,
        'prompt_type': prompt_type,
    }

    try:
        # DESC: Envio de requisição para a API de RAG
        response = requests.post(
            config.api_url + '/rag', headers=headers, params=params, timeout=180
        )

        if response.status_code == 200:
            decoded_response = response.content.decode('utf-8')

            response_dict = json.loads(decoded_response)

            response_dict['status'] = 200

            logfire.info('Consegui me conectar com a API de RAG!', status_code=200)

            return response_dict
        else:
            logfire.exception(
                'Perdão, não consegui me conectar com a API de RAG!', status_code=404
            )
            return {
                'status': response.status_code,
                'description': 'Perdão, a API de RAG retornou um resultado inesperado! Tente novamente mais tarde...',
            }

    except Timeout:
        logfire.exception(
            'Perdão, não consegui me conectar com a API de RAG!', status_code=408
        )
        return {
            'status': 408,
            'description': 'Perdão, não consegui me conectar com a API de RAG! Tente novamente mais tarde...',
        }


def set_title(*, title: str = 'Scientific Assistant'):
    st.title(title)


def set_title_alignment():
    title_alignment = """
    <style>
    #scientific-helper {
        text-align: center
    }
    </style>
    """
    st.markdown(title_alignment, unsafe_allow_html=True)


def set_name_page():
    icon = Image.open(Path('src/resource/research-icon.png'))
    st.set_page_config(
        page_title='Scientific Assistant',
        page_icon=icon,
    )


def hide_sidebar():
    st.markdown(
        """
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
