from flask import render_template, flash, redirect
from flask_restplus import Resource, fields
from src import app, api
from src.objects import User, Recommendation, Offer, RecommendationsList
from src.database import Database


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main')


@api.route('/getRecommendations/<int:userId>')
@api.doc(params={'userId': 'an ID of a User for whom the requested Recommendations are'})
class MyRecommendations(Resource):
    def get(self, userId):
        recommendations = Database.get_recommendations(userId)
        return recommendations.serialize()


@api.route('/postUser/<int:userId>/<string:tags>')
@api.doc(params={'userId': 'an ID of a User',
                 'tags': 'tags possessed by a User'})
class MyUsers(Resource):
    def post(self, userId, tags):
        myUser = User(userId, tags)
        Database.add(myUser)
        return {'status': f'user {userId} with tags {tags} added'}


def count_matching_tags(offer: Offer, user: User) -> int:
    counter = 0
    for offerTag in offer.tags:
        for userTag in user.tags:
            if offerTag == userTag:
                counter = counter + 1
    return counter


@api.route('/postOffer/<int:offerId>/<string:tags>/<string:offerTitle>')
@api.doc(params={'offerId': 'an ID of a new offer to add to users\' recommendations',
                 'offerTitle': 'title of the offer being added'})
class MyOffers(Resource):
    def post(self, offerId, tags, offerTitle):
        offer = Offer(offerId, tags, offerTitle)
        Database.add(offer)

        # TODO:
        # ask service Users for (id,tags) of all users that are looking for a job

        users = Database.get_users()
        for user in users:
            counter = count_matching_tags(offer, user)
            if counter > 2:
                recommendationId = Database.get_next_recommendation_id()
                print(f"adding recommendation id={recommendationId} for userId={user.id}")
                recommendation = Recommendation(recommendationId=recommendationId,
                                                offerId=offer.id,
                                                userId=user.id,
                                                offerTitle=offer.title)
                Database.add(recommendation)

        return {'status': f'offer {offerId} with tags {tags} added'}
