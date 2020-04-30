from flask import render_template, flash, redirect
from src import app
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main')
