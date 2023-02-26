FROM python:3.11-slim

LABEL name="gpt3_bot" version="0.1.0"

WORKDIR /opt/bot/

# install pip requirements
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "/opt/bot/gpt3_bot.py" ]
