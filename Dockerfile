FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt quotes.txt bot.py /usr/src/app/
RUN pip install -r requirements.txt
CMD ["python", "bot_buzzwords.py"]

