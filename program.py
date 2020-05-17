import requests
from datetime import datetime
import psycopg2


class CallTwitchAPI:
    def __init__(self, client_id, url):
        self.url = url
        self.client_id = client_id

    def get_headers(self):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
        }
        # client_secret = 'wgtnu7zkeetu7x9nxi9h6efmlkgzk4'
        return headers

    def get_requests_json(self):
        response = requests.get(self.url, headers=self.get_headers())
        # text_response = response.text
        return response.json()


class InsertGamesDataToDB:
    def __init__(self, json):
        self.json = json

    def create_ranking_list(self):
        now = datetime.now()
        ranking = [((self.json['top'][i]['game']['name']), i + 1,
                    (self.json['top'][i]['viewers']),
                    (self.json['top'][i]['channels']),
                    now.strftime("%m/%d/%Y %H:%M:%S")) for i in range(10)]
        return ranking

    def insert_game_data(self, dbname, user):
        conn = psycopg2.connect(dbname=dbname, user=user)
        cur = conn.cursor()

        insert_function = """
        INSERT INTO twitch_data_analytics (game_name, ranking, viewers, channels, time)
        VALUES (%(game_name)s, %(ranking)s, %(viewers)s, %(channels)s, %(time)s);
        """

        for i in range(10):
            cur.execute(insert_function, (
                {
                    'game_name': self.create_ranking_list()[i][0],
                    'ranking': self.create_ranking_list()[i][1],
                    'viewers': self.create_ranking_list()[i][2],
                    'channels': self.create_ranking_list()[i][3],
                    'time': self.create_ranking_list()[i][4]}))

        conn.commit()
        cur.close()
        conn.close()


top_10_games_json = CallTwitchAPI(client_id='7zilk1vqpgww0f2nwsgm5gmwhmgnar',
                                  url='https://api.twitch.tv/kraken/games/top').get_requests_json()

InsertGamesDataToDB(json=top_10_games_json).insert_game_data(
    dbname="gaming_analytics", user="postgres")


# Records by Kenneth Reitz
# SQL Alchemy
# Chron Job to run every 6 hours
