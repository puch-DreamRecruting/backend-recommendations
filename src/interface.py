from flask import render_template, request
from flask_restplus import Resource
from src import app, api
from src.objects import User, Recommendation, Offer
from src.database import Database
import requests


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


@api.route('/getUsers')
class MyUsersList(Resource):
    def get(self):
        users = Database.get_users()
        return users.serialize()


def count_matching_tags(offer: Offer, user: User) -> int:
    counter = 0
    for offerTag in offer.tags:
        for userTag in user.tags:
            if offerTag == userTag:
                counter = counter + 1
    return counter


def post_to_notifications(json):
    print("sending recommendation...")
    url = "https://dr-prod-euw-app-backend-notifications01.azurewebsites.net/api/v1/addRecommendationNotification/"
    res = requests.post(url,
                        json=json)
    if res.status_code == 200:
        print(res.text)


@api.route('/postUser/')
class MyUsers(Resource):
    def post(self):
        data = request.get_json()
        userId = data["id"]
        tags = data["tags"]

        myUser = User(userId, tags)
        Database.add_user(myUser)
        return {'status': f'user {userId} with tags {tags} added'}


@api.route('/postOffer/')
class MyOffers(Resource):
    def post(self):
        data_f = request.get_json()
        data = data_f["payload"]

        offerId = data["id"]
        tags = data["tags"]
        offerTitle = data["title"]
        offer = Offer(offerId, tags, offerTitle)

        # TODO:
        # ask service Users for (id,tags) of all users that are looking for a job?

        users = Database.get_users().list
        for user in users:
            counter = count_matching_tags(offer, user)
            if counter > 2:
                recommendationId = Database.get_next_recommendation_id()
                print(f"adding recommendation id={recommendationId} for userId={user.id}")
                recommendation = Recommendation(recommendationId=recommendationId,
                                                offerId=offer.id,
                                                userId=user.id,
                                                offerTitle=offer.title)
                Database.add_recommendation(recommendation)
                post_to_notifications(recommendation.serialize())

        return {'status': f'offer id={data["id"]} (title= {data["title"]}) with tags {data["tags"]} added'}

    # @api.route('/clearRecommendationsDb/')
    # class ClearRecommendations(Resource):
    #     def post(self):
    #         Database.clear_db()
    #         return {'status': 'tables and data removed'}
