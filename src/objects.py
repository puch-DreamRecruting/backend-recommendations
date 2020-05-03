from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def serialize(self):
        pass


class User(Serializable):
    userId = 0
    tags = ['']

    def __init__(self, userId, tags):
        self.userId = userId
        self.tags = tags

    def serialize(self):
        JSONed = {}
        JSONed['userID'] = self.userId
        JSONed['tags'] = self.tags
        return JSONed


class Offer(Serializable):
    offerId = 0
    tags = ['']

    def __init__(self, offerId, tags):
        self.offerId = offerId
        self.tags = tags

    def serialize(self):
        JSONed = {}
        JSONed['offerID'] = self.offerId
        JSONed['tags'] = self.tags
        return JSONed


class Recommendation(Serializable):
    recommendationId = 0
    offerId = 0
    userId = 0

    def __init__(self, recommendationId, offerId, userId):
        self.recommendationId = recommendationId
        self.offerId = offerId
        self.userId = userId

    def serialize(self):
        JSONed = {}
        JSONed['recommendationId'] = self.recommendationId
        JSONed['userId'] = self.userId
        JSONed['offerId'] = self.offerId
        return JSONed
