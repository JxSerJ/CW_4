FROM python:3.10-slim

WORKDIR /app_code
RUN python3 -m pip install --upgrade pip setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip cache purge
ENV FLASK_APP='run.py'
COPY entrypoint.sh .
COPY run.py .
COPY migrations migrations
COPY project project
COPY database database

COPY docker_config.py config.py

CMD [ "sh", "entrypoint.sh" ]
