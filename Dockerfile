FROM python:3.7.1

RUN mkdir /app
WORKDIR /app
COPY * /app/

RUN pip install --upgrade pip && \
	pip install pipenv

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 4444

CMD python main.py
