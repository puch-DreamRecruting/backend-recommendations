import json


class Database:
    dbName = ''

    @staticmethod
    def add(serializable):
        with open('data.txt', 'w') as outfile:
            json.dump(serializable.serialize(), outfile)

    @staticmethod
    def get(recommendationId):
        pass
