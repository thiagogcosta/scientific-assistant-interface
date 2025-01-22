ARG PYTHON_IMAGE_VERSION="3.11"

FROM python:${PYTHON_IMAGE_VERSION}-slim

#------------------------------
# DESC: connect and get informations of the ChromaDB
#---------------DEVELOPMENT INFOS---------------
ARG API_URL='http://0.0.0.0:8000'
ENV API_URL=${API_URL}

ARG API_KEY='api-tok3n'
ENV API_KEY=${API_KEY}

#------------------------------

ARG LOGFIRE_PROJECT_TOKEN=''
ENV LOGFIRE_PROJECT_TOKEN=${LOGFIRE_PROJECT_TOKEN}

# Install necessary packages and clean up in a single RUN command
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /scientific-assistant-interface

RUN chmod -R 775 ./

ENV PYTHONPATH="/scientific-assistant-interface"

COPY pyproject.toml poetry.lock ./

# DESC: Install the poetry, set the env var in the project directory,
# and install the dependencies
RUN python -m pip install -q poetry==1.8.3 \
    && python -m poetry config virtualenvs.in-project true \
    && python -m poetry install --only main --no-interaction --no-ansi

COPY /src ./src

EXPOSE 8501

CMD ["python", "-m", "poetry", "run", "streamlit", "run", "src/streamlit_app.py", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]

#----------INSTRUCTIONS----------

# buildar a imagem
#docker build -t scientific_assistant_interface .

# executar o container com os containers visualizando a rede da maquina
#docker run -d --name interface_service --network host scientific_assistant_interface

# acessar o container
#docker exec -i -t interface_service bash

# finalizar a execucao do container
#docker kill interface_service

# excluir os containers finalizados
#docker rm $(docker ps -a -q)
