from flask import Flask, escape, request
from src.config import Config


app = Flask(__name__)
app.config.from_object(Config)

from src import interface
