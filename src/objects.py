from typing import List, Dict
from abc import ABC, abstractmethod
import datetime


def parse_tags(tags: str) -> List[str]:
    return tags.split(',')


class Serializable(ABC):
    name = ''
    timeAdded = 0
    id = 0

    def __init__(self):
        self.timeAdded = datetime.datetime.now()

    @abstractmethod
    def serialize(self):
        pass


class User(Serializable):
    userId = 0
    tags = ['']

    def __init__(self, userId, tags):
        super().__init__()
        self.name = "user" + str(userId)
        self.id = userId
        self.tags = tags  # parse_tags(tags)

    def serialize(self):
        JSONed = {}
        JSONed['userId'] = self.id
        JSONed['tags'] = self.tags
        JSONed['timeAdded'] = str(self.timeAdded)
        print(f'user {self.id} has been JSONed')
        return JSONed

    @staticmethod
    def deserialize(datastore):
        user = User(datastore['userId'], '')
        user.tags = datastore['tags']
        return user


class Offer(Serializable):
    offerId = 0
    tags = ['']
    title = ''

    def __init__(self, offerId, tags, title):
        super().__init__()
        self.name = "offer" + str(offerId)
        self.id = offerId
        self.tags = tags  # parse_tags(tags)
        self.title = title

    def serialize(self):
        JSONed = {}
        JSONed['offerId'] = self.id
        JSONed['tags'] = self.tags
        JSONed['timeAdded'] = str(self.timeAdded)
        return JSONed


class Recommendation(Serializable):
    offerId = 0
    userId = 0
    offerTitle = ''

    def __init__(self, recommendationId, offerId, userId, offerTitle):
        super().__init__()
        self.name = "recommendation" + str(recommendationId)
        self.id = recommendationId
        self.userId = userId
        self.offerId = offerId
        self.offerTitle = offerTitle

    def serialize(self):
        JSONed = {}
        JSONed['recommendationId'] = self.id
        JSONed['userId'] = self.userId
        JSONed['offerId'] = self.offerId
        JSONed['offerTitle'] = self.offerTitle
        JSONed['timeAdded'] = str(self.timeAdded)
        return JSONed

    @staticmethod
    def deserialize(datastore):
        recommendation = Recommendation(0, 0, 0, '')
        recommendation.id = datastore['recommendationId']
        recommendation.userId = datastore['userId']
        recommendation.offerId = datastore['offerId']
        recommendation.offerTitle = datastore['offerTitle']
        return recommendation


class UsersList(Serializable):
    list = []

    def serialize(self):
        JSONed = {}
        JSONed['users'] = []
        for i in self.list:
            JSONed['users'].append(i.serialize())
        return JSONed

    def add(self, user: User):
        self.list.append(user)

    def clear(self):
        self.list = []


class RecommendationsList(Serializable):
    list = []

    def serialize(self):
        JSONed = {}
        JSONed['recommendations'] = []
        for i in self.list:
            JSONed['recommendations'].append(i.serialize())
        return JSONed

    def add(self, recommendation: Recommendation):
        self.list.append(recommendation)

    def clear(self):
        self.list = []
