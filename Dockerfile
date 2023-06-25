FROM python:3.10-slim-buster 

#RUN apt-get update && apt-get install -y \
#    build-essential \
#    software-properties-common \
#    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir streamlit
RUN python -m pip install -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "rdf_data_converter_and_beautifier.py", "--server.port=8501", "--server.address=0.0.0.0"]