from src import app
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def main():
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    credential = DefaultAzureCredential()

    # secret_client = SecretClient(vault_url="https://dr-dev-euw-kv-common01.vault.azure.net/",
    #                             credential=credential)
    secret_client = SecretClient(vault_url="https://dr-prod-euw-kv01.vault.azure.net/",
                                credential=credential)

    secret_properties = secret_client.list_properties_of_secrets()
    for secret_property in secret_properties:
        print(secret_property.name)

    # secret = secret_client.get_secret("Notifications-SqlDb-ConnectionString")
    # secret = secret_client.get_secret("Recommendations-Database-ConnectionString")
    # print(secret.name)
    # print(secret.value)

    main()
