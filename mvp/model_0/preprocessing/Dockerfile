ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-slim-buster
ARG PROJECT_DIRECTORY="/usr/app"

WORKDIR ${PROJECT_DIRECTORY}

# Annoy won't work without g++
RUN apt update && apt-get install g++ -yy

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "src/main.py"]