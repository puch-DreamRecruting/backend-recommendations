from flask import render_template, flash, redirect
from flask_restplus import Resource, fields
from src import app, api
from src.objects import User, Recommendation, Offer
from src.database import Database


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main')


@api.route('/getRecommendations/<int:userId>')
@api.doc(params={'userId': 'an ID of a User for whom the requested Recommendations are'})
class MyRecommendations(Resource):
    def get(self, userId):
        # TODO: return Recommendations for a specified User
        return {userId: 'sample recommendation'}


@api.route('/postUser/<int:userId>/<string:tags>')
@api.doc(params={'userId': 'an ID of a User', 'tags': 'tags possessed by a User'})
class MyUsers(Resource):
    def post(self, userId, tags):
        myUser = User(userId, tags)
        Database.add(myUser)
        return {'status': f'user {userId} with tags {tags} NOT added'}


@api.route('/postOffer/<int:offerId>/<string:tags>')
@api.doc(params={'offerId': 'an ID of a new offer to add to users\' recommendations'})
class MyOffers(Resource):
    def post(self, offerId, tags):
        myOffer = Offer(offerId, tags)
        Database.add(myOffer)
        return {'status': f'offer {offerId} with tags {tags} NOT added'}
