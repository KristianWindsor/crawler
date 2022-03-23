FROM python:3.7

RUN apt-get update && \
# install dumb-init
    apt-get install -y dumb-init && \
# install google chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
# install chromedriver
    apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /app/
COPY ./app/ /app/

# install python packages
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD [ "python3", "app.py" ]