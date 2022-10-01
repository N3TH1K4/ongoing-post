FROM python:3.8

WORKDIR /ongoing-post

COPY requirements.txt /ongoing-post/
RUN pip3 install -r requirements.txt

COPY . /ongoing-post/

CMD python3 bot.py
