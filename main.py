from src import app
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def main():
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()
