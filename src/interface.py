from flask import render_template, flash, redirect
from flask_restplus import Resource, fields
from src import app, api


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main')


@api.route('/getRecommendations/<userId>')
@api.doc(params={'userId': 'an ID of a User for whom the requested Recommendations are'})
class MyRecommendations(Resource):
    def get(self, id):
        return {}  ## TODO: return Recommendations for a specififed User


@api.route('/postUser/<userId>')
@api.doc(params={'userId': 'an ID of a User', 'tags': 'tags possessed by a User'})
class MyUsers(Resource):
    def post(self, id):
        return  ## TODO: accept User with its tags


@api.route('/postOffer/<offerId>')
@api.doc(params={'offerId': 'an ID of a new offer to add to users\' recommendations'})
class MyOffers(Resource):
    def post(self, id):
        return  ## TODO: accept offer and tags
