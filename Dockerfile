FROM python:3.11.1

WORKDIR /usr/connecto

COPY requirements.txt ./requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY connecto ./connecto
CMD ["python3", "connecto/discord_bot.py"]