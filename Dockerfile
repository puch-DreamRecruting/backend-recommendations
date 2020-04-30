FROM python:3.7.1

RUN mkdir /app
WORKDIR /app
COPY * /app/

RUN pip install --upgrade pip && \
	pip install pipenv

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 80
EXPOSE 443

CMD python main.py
