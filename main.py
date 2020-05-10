from src import app


def main():
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()

# TODO:
# [ ] Połączenie z lokalna db - RecommendationsDB
# [ ] uzyskiwanie userow poszukujacych pracy od serwisu Users
# [ ] poinformowac serwis Offers, ze ma strzelac do Recommendations w momencie jak jest dodawana oferta
# [ ] strzelac rekomendacja do Notifications w momencie kiedy jest dodawana rekomendacja dla danego uzytkownika
