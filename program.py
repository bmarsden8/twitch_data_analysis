import requests
from datetime import datetime
import psycopg2


class TwitchData:
    def __init__(self, client_id):
        self.client_id = client_id

    def get_headers(self):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.client_id
        }
        # client_secret = 'wgtnu7zkeetu7x9nxi9h6efmlkgzk4'
        return headers

    def get_top_games_list(self, base_url="https://api.twitch.tv/kraken"):
        url = base_url + '/games/top'
        response = requests.get(url, headers=self.get_headers())
        # text_response = response.text
        json = response.json()
        now = datetime.now()
        ranking = [((json['top'][i]['game']['name']),
                    i + 1,
                    (json['top'][i]['viewers']),
                    (json['top'][i]['channels']),
                    now.strftime("%m/%d/%Y %H:%M:%S")) for i in range(10)]
        return ranking


class Database:
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user

    def insert_top_games_list(self, game_list):
        conn = psycopg2.connect(dbname=self.dbname, user=self.user)
        cur = conn.cursor()

        insert_function = """
        INSERT INTO twitch_data_analytics (game_name, ranking, viewers, channels, time)
        VALUES (%(game_name)s, %(ranking)s, %(viewers)s, %(channels)s, %(time)s);
        """

        for i in range(10):
            cur.execute(insert_function, (
                {
                    'game_name': game_list[i][0],
                    'ranking': game_list[i][1],
                    'viewers': game_list[i][2],
                    'channels': game_list[i][3],
                    'time': game_list[i][4]}))

        conn.commit()
        cur.close()
        conn.close()


twitch_client = TwitchData(client_id='7zilk1vqpgww0f2nwsgm5gmwhmgnar')
db = Database(dbname="gaming_analytics", user="postgres")
db.insert_top_games_list(twitch_client.get_top_games_list())
# db.insert_top_games_list(twitch_client.create_ranking_list(twitch_client.get_top_games_list()))

# Records by Kenneth Reitz
# SQL Alchemy

# Making an update
# If I want to make updates to git, VCS -> Commit, VCS-> Push

# Chron Job Info
# 6 * * * * /Users/billymarsden/PycharmProjects/twitch_data_analysis/program.py
# /Users/billymarsden/PycharmProjects/twitch_data_analysis/program.py

# To run cron, edit in crontab with 'crontab-e', i, edit the text, and then Esc, ':wq'
# Errors encountered with cron not running same version of python as interpreter in Pycharm
# Fixed with PYTHONPATH=/Library/Frameworks/Python.framework/Versions/3.8/bin/python3 /Users/billymarsden/PycharmProjects/twitch_data_analysis/program.py
