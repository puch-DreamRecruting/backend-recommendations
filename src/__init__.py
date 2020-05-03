from flask import Flask, escape, request
from src.config import Config
from flask_restplus import Api


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app, version='1.0', title='Recommendations',
          description='Recommendations microservice')

from src import interface
