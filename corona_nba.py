import os
import sys
import csv
import datetime

GAMEIDIDX = 0
GAMEDATEIDX = 1
GAMETIMEIDX = 2
AWAYFULLTEAMNAMEIDX = 5
HOMEFULLTEAMNAMEIDX = 6

contagious_time = datetime.timedelta(days=14)
date_of_announcement = datetime.datetime.strptime('3/11/20', '%m/%d/%y')
dates_of_infection = [date_of_announcement - contagious_time, date_of_announcement - (2 * contagious_time)]
infected_team = 'Utah Jazz'

csv_file_name = "nba-full-schedule-2019-2020.csv"
with open(csv_file_name, 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	teams = dict()
	canceled_game = None
	next(csv_reader)
	for line in csv_reader:
		game_id = line[GAMEIDIDX]
		game_time = line[GAMETIMEIDX]

		game_date = datetime.datetime.strptime(line[GAMEDATEIDX], '%m/%d/%y')
		game_time = datetime.datetime.strptime("{} {}".format(line[GAMEDATEIDX], game_time), '%m/%d/%y  %I:%M %p')

		home_team = line[HOMEFULLTEAMNAMEIDX]
		away_team = line[AWAYFULLTEAMNAMEIDX]

		game = {"id": game_id, "game_time": game_time, "date": game_date, "away_team": away_team, "home_team": home_team}

		if game_date == date_of_announcement and (infected_team == game["away_team"] or infected_team == game["home_team"]):
			canceled_game = game
			break

		if home_team not in teams:
			teams[home_team] = list()
		teams[home_team].append(game)

		if away_team not in teams:
			teams[away_team] = list()
		teams[away_team].append(game)

	cancellation_time = canceled_game['game_time']
	infected_teams = set()
	infected_teams.add(infected_team)
	visited_games = set()
	stack_of_games = list()
	for root_game in reversed(teams[infected_team]):
		if dates_of_infection[0] < root_game["date"] and root_game["date"] < cancellation_time:
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
			if dates_of_infection[0] < home_team_game['date'] and home_team_game['game_time'] < cancellation_time:
				break
			stack_of_games.append(home_team_game)

		for away_team_game in reversed(teams[game['away_team']]):
			if dates_of_infection[0] < away_team_game['date'] and away_team_game['game_time'] < cancellation_time:
				break
			stack_of_games.append(away_team_game)

	print("Assuming Gobert is Patient 0")
	print("Number of infected teams: ", len(infected_teams))
	print("Infected teams: ")
	for team in infected_teams:
		print("\t- ", team)

	for team in list(infected_teams):
		stack_of_games = list()
		for root_game in reversed(teams[team]):
			if dates_of_infection[1] < root_game["date"] and root_game["date"] < cancellation_time:
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
				if dates_of_infection[1] < home_team_game['date'] and home_team_game['game_time'] < cancellation_time:
					break
				stack_of_games.append(home_team_game)

			for away_team_game in reversed(teams[game['away_team']]):
				if dates_of_infection[1] < away_team_game['date'] and away_team_game['game_time'] < cancellation_time:
					break
				stack_of_games.append(away_team_game)

	print("Assuming Gobert is not Patient 0")
	print("Number of infected teams: ", len(infected_teams))
	print("Infected teams: ")
	for team in infected_teams:
		print("\t- ", team)
