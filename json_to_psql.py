import json
from app.dbmodels.models import Team, Player, Game, GameStats, Shot

# load teams data from json file into psql
with open('raw_data/teams.json') as f:
    teamsData = json.load(f)
    for team in teamsData:
        # check if this team is already in the database
        teamObj, created = Team.objects.get_or_create(
            id=team['id'],
            defaults={'name': team['name']}
        )
        if created:
            print(f"team {team['name']} has been added.")
        else:
            print(f"team {team['name']} already exists in the database.")

# load players data from json file
with open('raw_data/players.json') as f:
    playersData = json.load(f)
    for player in playersData:
        # see if the player has a team_id in the json
        teamId = player.get('team_id', None)

        # if the player doesn't have a team_id, assign one based on their id
        if teamId is None:
            if player['id'] <= 16:
                teamId = 1  # assign to team 1
            else:
                teamId = 2  # assign to team 2

        # check if the player already exists, create if they don't
        playerObj, created = Player.objects.get_or_create(
            id=player['id'],
            defaults={'name': player['name'], 'team_id': teamId}
        )
        if created:
            print(f"player {player['name']} has been added to team {teamId}.")
        else:
            print(f"player {player['name']} is already in the database.")

# initialize a counter for unique shot ids
shotIdCounter = 1

# loop through the games data from json
with open('raw_data/games.json') as f:
    gamesData = json.load(f)
    for game in gamesData:
        # check if this game is already in the database
        gameObj, created = Game.objects.get_or_create(
            id=game['id'],
            defaults={'game_date': game['date'], 'home_team_id': game['homeTeam']['id'], 'away_team_id': game['awayTeam']['id']}
        )
        if created:
            print(f"game {game['id']} has been added.")
        else:
            print(f"game {game['id']} is already in the database.")

        # loop through players in homeTeam and create GameStats
        for player in game['homeTeam']['players']:
            gameStatsObj, created = GameStats.objects.get_or_create(
                game_id=game['id'],
                player_id=player['id'],
                defaults={
                    'is_starter': player['isStarter'],
                    'minutes': player['minutes'],
                    'points': player['points'],
                    'assists': player['assists'],
                    'offensive_rebounds': player['offensiveRebounds'],
                    'defensive_rebounds': player['defensiveRebounds'],
                    'steals': player['steals'],
                    'blocks': player['blocks'],
                    'turnovers': player['turnovers'],
                    'defensive_fouls': player['defensiveFouls'],
                    'offensive_fouls': player['offensiveFouls'],
                    'free_throws_made': player['freeThrowsMade'],
                    'free_throws_attempted': player['freeThrowsAttempted'],
                    'two_pointers_made': player['twoPointersMade'],
                    'two_pointers_attempted': player['twoPointersAttempted'],
                    'three_pointers_made': player['threePointersMade'],
                    'three_pointers_attempted': player['threePointersAttempted'],
                }
            )
            if created:
                print(f"gameStats for player {player['id']} in game {game['id']} has been added.")
            else:
                print(f"gameStats for player {player['id']} in game {game['id']} already exists.")

            # loop through each shot and create Shot instances with a unique id
            for shot in player['shots']:
                shotObj, created = Shot.objects.get_or_create(
                    id=shotIdCounter,  # assign the current value of shotIdCounter
                    defaults={
                        'game_stats_id': gameStatsObj.id,
                        'is_make': shot['isMake'],
                        'location_x': shot['locationX'],
                        'location_y': shot['locationY']
                    }
                )
                if created:
                    print(f"shot with id {shotIdCounter} for player {player['id']} has been added.")
                    shotIdCounter += 1  # increment the counter for the next shot
                else:
                    print(f"shot with id {shotIdCounter} for player {player['id']} already exists.")

        # loop through players in awayTeam and create GameStats
        for player in game['awayTeam']['players']:
            gameStatsObj, created = GameStats.objects.get_or_create(
                game_id=game['id'],
                player_id=player['id'],
                defaults={
                    'is_starter': player['isStarter'],
                    'minutes': player['minutes'],
                    'points': player['points'],
                    'assists': player['assists'],
                    'offensive_rebounds': player['offensiveRebounds'],
                    'defensive_rebounds': player['defensiveRebounds'],
                    'steals': player['steals'],
                    'blocks': player['blocks'],
                    'turnovers': player['turnovers'],
                    'defensive_fouls': player['defensiveFouls'],
                    'offensive_fouls': player['offensiveFouls'],
                    'free_throws_made': player['freeThrowsMade'],
                    'free_throws_attempted': player['freeThrowsAttempted'],
                    'two_pointers_made': player['twoPointersMade'],
                    'two_pointers_attempted': player['twoPointersAttempted'],
                    'three_pointers_made': player['threePointersMade'],
                    'three_pointers_attempted': player['threePointersAttempted'],
                }
            )
            if created:
                print(f"gameStats for player {player['id']} in game {game['id']} has been added.")
            else:
                print(f"gameStats for player {player['id']} in game {game['id']} already exists.")

            # loop through each shot and create Shot instances with a unique id
            for shot in player['shots']:
                shotObj, created = Shot.objects.get_or_create(
                    id=shotIdCounter,  # assign the current value of shotIdCounter
                    defaults={
                        'game_stats_id': gameStatsObj.id,
                        'is_make': shot['isMake'],
                        'location_x': shot['locationX'],
                        'location_y': shot['locationY']
                    }
                )
                if created:
                    print(f"shot with id {shotIdCounter} for player {player['id']} has been added.")
                    shotIdCounter += 1  # increment the counter for the next shot
                else:
                    print(f"shot with id {shotIdCounter} for player {player['id']} already exists.")
