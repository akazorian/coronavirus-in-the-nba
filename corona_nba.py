import os
import sys
import csv
import datetime

GAMEIDIDX = 0
GAMEDATEIDX = 1
AWAYFULLTEAMNAMEIDX = 5
HOMEFULLTEAMNAMEIDX = 6

median_day_of_infection = datetime.datetime.strptime('3/6/20', '%m/%d/%y')
date_of_announcement = datetime.datetime.strptime('3/11/20', '%m/%d/%y')
infected_team = 'Utah Jazz'

csv_file_name = "nba-full-schedule-2019-2020.csv"
with open(csv_file_name, 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	teams = dict()
	root = None
	next(csv_reader)
	for line in csv_reader:
		game_id = line[GAMEIDIDX]

		game_date = datetime.datetime.strptime(line[GAMEDATEIDX], '%m/%d/%y')
		if game_date > date_of_announcement:
			break

		home_team = line[HOMEFULLTEAMNAMEIDX]
		away_team = line[AWAYFULLTEAMNAMEIDX]

		game = {"id": game_id, "date": game_date, "away_team": away_team, "home_team": home_team}

		if home_team not in teams:
			teams[home_team] = list()
		teams[home_team].append(game)

		if away_team not in teams:
			teams[away_team] = list()
		teams[away_team].append(game)

		if game_date == date_of_announcement and (infected_team == game["away_team"] or infected_team == game["home_team"]):
			root = game

	infected_teams = set()
	infected_teams.add(infected_team)
	visited_games = set()
	stack_of_games = list()
	for root_game in reversed(teams[infected_team]):
		if root_game["date"] >= median_day_of_infection:
			stack_of_games.append(root_game)
	 
	while len(stack_of_games) > 0:
		game = stack_of_games.pop()
		if game['id'] in visited_games:
			continue

		visited_games.add(game['id'])
		if game['home_team'] not in infected_teams:
			infected_teams.add(game['home_team'])
		if game['away_team'] not in infected_teams:
			infected_teams.add(game['away_team'])

		for home_team_game in reversed(teams[game['home_team']]):
			if home_team_game['date'] < median_day_of_infection:
				break
			stack_of_games.append(home_team_game)

		for away_team_game in reversed(teams[game['away_team']]):
			if away_team_game['date'] < median_day_of_infection:
				break
			stack_of_games.append(away_team_game)

	print("Number of infected teams: ", len(infected_teams))
	print("Infected teams: ")
	for team in infected_teams:
		print("\t- ", team)

















