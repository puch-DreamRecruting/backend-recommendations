from src.objects import User, Recommendation, UsersList, RecommendationsList
from typing import List, Dict
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from os import environ
import pyodbc


class Database:
    dbName = ''
    create_table_users = \
        "CREATE TABLE [dbo].[users]( " \
        "[userId] [int] NOT NULL, " \
        "[creationDate] [datetime] NULL, " \
        " CONSTRAINT [PK_users] PRIMARY KEY CLUSTERED ( " \
        " [userId] ASC " \
        ")WITH (PAD_INDEX = OFF, " \
        "STATISTICS_NORECOMPUTE = OFF, " \
        "IGNORE_DUP_KEY = OFF, " \
        "ALLOW_ROW_LOCKS = ON, " \
        "ALLOW_PAGE_LOCKS = ON) ON [PRIMARY] " \
        ") ON [PRIMARY];"
    create_table_recommendations = \
        "CREATE TABLE [dbo].[recommendations]( " \
        "[recommendationId] [int] NOT NULL, " \
        "[userId] [int] NOT NULL, " \
        "[offerId] [int] NOT NULL, " \
        "[offerTitle] [nvarchar](50) NOT NULL, " \
        "[creationDate] [datetime] NULL, " \
        " CONSTRAINT [PK_recommendations] PRIMARY KEY CLUSTERED ( " \
        "[recommendationId] ASC " \
        ")WITH (PAD_INDEX = OFF, " \
        "STATISTICS_NORECOMPUTE = OFF, " \
        "IGNORE_DUP_KEY = OFF, " \
        "ALLOW_ROW_LOCKS = ON, " \
        "ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]" \
        ") ON [PRIMARY]; "
    create_table_tags = \
        "CREATE TABLE [dbo].[tags]( " \
        "[userId] [int] NOT NULL, " \
        "[tag] [nvarchar](50) NOT NULL " \
        ") ON [PRIMARY]; "
    drop_table_users = "DROP TABLE users;"
    drop_table_recommendations = "DROP TABLE recommendations;"
    drop_table_tags = "DROP TABLE tags;"

    @staticmethod
    def get_next_recommendation_id() -> int:
        cnxn, cursor = Database.init_db()
        cursor.execute("SELECT TOP 1 recommendationId from recommendations ORDER BY recommendationId DESC")
        row = cursor.fetchone()
        while row is None:
            return 0
        return row[0] + 1

    @staticmethod
    def get_db_config(connection_string: str) -> Dict[str, str]:
        connection_string_splitted = connection_string.split(";")
        host = connection_string_splitted[1].split("=")[1]
        database = connection_string_splitted[2].split("=")[1]
        password = connection_string_splitted[4].split("=")[1]
        username = connection_string_splitted[3].split("=")[1]
        db_config = {'HOST': host,
                     'USER': username,
                     'PASSWORD': password,
                     'DB': database}
        return db_config

    @staticmethod
    def get_odbc_connection_string(db_config: Dict[str, str]) -> str:
        server = db_config['HOST']
        database = db_config['DB']
        username = db_config['USER']
        password = db_config['PASSWORD']
        odbc_connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;' \
                                 f'SERVER={server};' \
                                 f'DATABASE={database};' \
                                 f'UID={username};' \
                                 f'PWD={password};'
        return odbc_connection_string

    @staticmethod
    def get_connection_string() -> str:
        credential = DefaultAzureCredential()
        url = environ.get("KeyVaultUri")
        secret_client = SecretClient(vault_url=url,
                                    credential=credential)
        db_connection_string = secret_client.get_secret("Recommendations-Database-ConnectionString").value
        print(db_connection_string)
        db_config = Database.get_db_config(db_connection_string)
        return Database.get_odbc_connection_string(db_config)

    @staticmethod
    def init_db():
        cnxn = pyodbc.connect(Database.get_connection_string())
        cursor = cnxn.cursor()
        if not cursor.tables(table='users').fetchone():
            cursor.execute(Database.create_table_users)
            cnxn.commit()
        if not cursor.tables(table='recommendations').fetchone():
            cursor.execute(Database.create_table_recommendations)
            cnxn.commit()
        if not cursor.tables(table='tags').fetchone():
            cursor.execute(Database.create_table_tags)
            cnxn.commit()
        return cnxn, cursor

    @staticmethod
    def add(query: str) -> None:
        cnxn, cursor = Database.init_db()
        cursor.execute(query)
        cnxn.commit()

    @staticmethod
    def add_user(user):
        add_user_sql = f"INSERT INTO users(userId, creationDate) " \
                       f"VALUES({user.id}, null);"
        Database.add(add_user_sql)
        for tag in user.tags:
            add_tag_sql = f"INSERT INTO tags(userId, tag) " \
                          f"VALUES({user.id}, '{tag}');"
            Database.add(add_tag_sql)

    @staticmethod
    def get_users() -> UsersList:
        users = UsersList()
        users.clear()

        cnxn, cursor = Database.init_db()
        cursor.execute("SELECT * FROM users")
        raw_users = []
        row = cursor.fetchone()
        while row:
            raw_users.append(row)
            row = cursor.fetchone()

        for raw_user in raw_users:
            userId = raw_user[0]
            creationDate = raw_user[1]

            tags = []
            cursor.execute(f"SELECT * FROM tags WHERE userId={userId}")
            row = cursor.fetchone()
            while row:
                tag = row[1]
                tags.append(tag)
                row = cursor.fetchone()

            users.add(User(userId=userId, tags=tags))

        return users

    @staticmethod
    def add_recommendation(r):
        add_recomm_sql = f"INSERT INTO recommendations(recommendationId, userId, offerId, offerTitle, creationDate) " \
                         f"VALUES({r.id}, {r.userId}, {r.offerId}, '{r.offerTitle}', null);"
        Database.add(add_recomm_sql)

    @staticmethod
    def get_recommendations(id: int) -> RecommendationsList:
        recommendations = RecommendationsList()
        recommendations.clear()

        cnxn, cursor = Database.init_db()
        cursor.execute(f"SELECT * FROM recommendations WHERE userId={id};")

        raw_recommendations = []
        row = cursor.fetchone()
        while row:
            raw_recommendations.append(row)
            row = cursor.fetchone()

        for raw_recommendation in raw_recommendations:
            recommendationId = raw_recommendation[0]
            userId = raw_recommendation[1]
            offerId = raw_recommendation[2]
            offerTitle = raw_recommendation[3]
            creationDate = raw_recommendation[4]
            recommendation = Recommendation(recommendationId, offerId, userId, offerTitle)
            recommendations.add(recommendation)

        return recommendations

    @staticmethod
    def clear_db():
        cnxn, cursor = Database.init_db()
        cursor.execute(Database.drop_table_users)
        cursor.execute(Database.drop_table_recommendations)
        cursor.execute(Database.drop_table_tags)
        cnxn.commit()
