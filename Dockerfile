FROM python:3.7.7-slim-buster

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y gnupg

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/19.10/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN apt-get install -y gettext
RUN apt-get install -y g++
RUN apt-get install -y gcc

# Install ODBC driver
RUN export ACCEPT_EULA=Y && \
    apt-get install -y msodbcsql17 && \
    apt-get install -y mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> /root/.bash_profile && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> /root/.bashrc

RUN pip install --upgrade pip && \
	pip install pipenv

RUN mkdir /app
WORKDIR /app
COPY * /app/

RUN apt-get install -y unixodbc-dev && pip install -r requirements.txt

ADD . /app

EXPOSE 80
EXPOSE 443

CMD python main.py
