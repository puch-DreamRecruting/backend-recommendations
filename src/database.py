import json
from src.objects import User, Recommendation, RecommendationsList
from typing import List
from os import path


def user_filename(i: int) -> str:
    return 'mockDb/user' + str(i) + '.txt'


def recommendation_filename(i: int) -> str:
    return 'mockDb/recommendation' + str(i) + '.txt'


class Database:
    dbName = ''
    id = 0

    @staticmethod
    def get_next_recommendation_id() -> int:
        Database.id = Database.id + 1
        return Database.id - 1

    @staticmethod
    def add(serializable) -> None:
        filename = "mockDb/" + serializable.name + ".txt"
        with open(filename, 'w') as outfile:
            json.dump(serializable.serialize(), outfile)

    @staticmethod
    def get_recommendations(id: int) -> RecommendationsList:
        recommendations = RecommendationsList()
        recommendations.clear()
        # load all recommendations from JSONs
        for i in range(0, 150):
            filename = recommendation_filename(i)
            if path.exists(filename):
                with open(filename, 'r') as f:
                    datastore = json.load(f)
                try:
                    recommendation = Recommendation.deserialize(datastore)
                    if recommendation.userId == id:
                        recommendations.add(recommendation)
                except Exception:
                    pass
        return recommendations

    @staticmethod
    def get_user(id: int) -> User:
        return User(id, '')

    @staticmethod
    def get_users() -> List[User]:
        users = []
        # load all users from JSONs and put them into list
        for i in range(1, 100):
            filename = user_filename(i)
            if path.exists(filename):
                with open(filename, 'r') as f:
                    datastore = json.load(f)
                user = User.deserialize(datastore)
                users.append(user)
        return users
