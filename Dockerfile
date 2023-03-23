FROM python:3.11-slim

LABEL name="gpt_bot" version="0.1.1"

WORKDIR /opt/bot/

# install pip requirements
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "/opt/bot/app.py" ]
