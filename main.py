from src import app


def main():
    print("hello world")
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()
