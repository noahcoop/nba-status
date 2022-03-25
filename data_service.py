from datetime import datetime
import struct
from urllib import response
from requests import get
from json import loads
from time import sleep

class DataService():
    def __init__(self):
        self.base_url = "https://www.balldontlie.io/api"
        self.todays_games = []

    def validate_game_obj(self, game):
        return "id" in game and "home_team" in game and "visitor_team" in game and "name" in game["home_team"] and "name" in game["visitor_team"] and "home_team_score" in game and "visitor_team_score" in game and "status" in game and "period" in game and "time" in game

    def validate_stats_obj(self, stats):
        return "player" in stats and "team" in stats and "pts" in stats and "reb" in stats and "ast" in stats and "first_name" in stats["player"] and "last_name" in stats["player"] and "abbreviation" in stats["team"]

    def fetch_todays_games(self):
        """Gets the games played by a team on a given date"""
        self.todays_games = []
        today = datetime.today().strftime('%Y-%m-%d')
        response = get(
            "{}/v1/games?start_date={}&end_date={}".format(self.base_url, today, today))
        game_data = loads(response.text)["data"]
        for game in game_data:
            if not self.validate_game_obj(game):
                continue
            self.todays_games.append({
                "id": game["id"],
                "home_team": game["home_team"]["name"],
                "visitor_team": game["visitor_team"]["name"],
                "home_team_score": game["home_team_score"],
                "visitor_team_score": game["visitor_team_score"],
                "status": game["status"],
                "period": game["period"],
                "time": game["time"],
            })

    def fetch_game_stat_leaders(self, game_id):
        response = get("{}/v1/stats?game_ids[]={}".format(self.base_url, game_id))
        game_data = loads(response.text)["data"]
        message = ""
        for metric in ["pts", "reb", "ast"]:
            leader = max(game_data, key=lambda x:x[metric] if x[metric] != None else 0)
            if not self.validate_stats_obj(leader):
                continue
            message += "{} {} ({}) {}{}\n".format(leader["player"]["first_name"], leader["player"]["last_name"], leader["team"]["abbreviation"], leader[metric], metric)
        return message

    def build_morning_message(self):
        message = "\nGood Morning! Here's a look at todays NBA slate:\n\n"
        for game in self.todays_games:
            message += "{} vs. {} {}\n".format(
                game["home_team"], game["visitor_team"], game["status"])
        return message

    def build_night_message(self):
        message = "\nFinal scores are in!\n\n"
        for game in self.todays_games:
            message += "{} {} - {} {}\n".format(game["home_team"], game["home_team_score"], game["visitor_team"], game["visitor_team_score"])
            message += self.fetch_game_stat_leaders(game["id"])
            message += "-----\n"
            sleep(5)
        return message


if __name__ == "__main__":
    dataService = DataService()
    dataService.fetch_todays_games()
    print(dataService.build_morning_message())
    print(dataService.build_night_message())

