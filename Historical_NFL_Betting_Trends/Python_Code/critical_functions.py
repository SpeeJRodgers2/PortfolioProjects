from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:////workspaces/126349338/Final_Project/NFL.db")

def det_fav_home_away(team_home, team_away, team_favorite_id):

    # use the team_favorite_id from the db to searchthe NFL_teams table and get the full team names
    favorite_team_name_db = db.execute("SELECT team_name FROM NFL_teams WHERE team_id = ?", (team_favorite_id,))
    # have an empty list to fill with the teams name or names to compare to
    favorite_team_names = []
    # fill the empty list with the team name or name to compare to
    for favorite_team_name in favorite_team_name_db:
        favorite_team_names.append(favorite_team_name["team_name"])

    # compare the team name or names in the favorite_team_names list to the home and away team names to see if the favorite is the home or away team
    if team_home in favorite_team_names:
        return "Home"
    elif team_away in favorite_team_names:
        return "Away"
    # had to add after debugging my code and seeing that "PICK" was a team_favorite_id I did not account for if the game was a "Pick Em"
    elif 'Pick Em' in favorite_team_names:
        return "None"
    else:
        raise ValueError("The favorite team ID does not match either the home team or the away team.")

def det_team_record_su(team_name):
    # Initialize variables for counting wins and losses
    season_wins = 0
    season_losses = 0
    season_ties = 0
    current_season_year = 0
    previous_season_year = 0

    # Get the columns needed where the team being looked at played
    games = db.execute("SELECT team_home, team_away, home_score, away_score, fav_home_away, season_year, week_number FROM NFL_reg_season_spreads WHERE team_home = ? OR team_away = ?",
                        team_name, team_name)

    # Iterate through all the games and tally the wins and losses
    for game in games:
        # Set the week_number, team_home, and team_away to their current varioables in this row for exact insertion of new data in the table at the bottom
        week_number = game["week_number"]
        team_home = game["team_home"]
        team_away = game["team_away"]

        # Set the current_season_year variable at the start of each loop to make sure wins and losses are only added for the same season
        current_season_year = game["season_year"]

        # Check if the season has changed, and if it has reset the wins, losses, and ties
        if previous_season_year == 0 or current_season_year == previous_season_year:
            # Using the pass statement here because I simply want nothing to happen if one of the above conditions are met
            pass
        else:
            season_wins = 0
            season_losses = 0
            season_ties = 0

        # If the team is home
        if game["team_home"] == team_name:

            # Store the season recod as a string to be input into the table before the wins, losses, or ties are added so the record doesn't count the current week
            season_record = str(season_wins) + "-" + str(season_losses) + "-" + str(season_ties)

            # Fill only the HT (home team) columns in the table
            # Store the teams current record in the proper column and row of the table
            db.execute("UPDATE NFL_reg_season_spreads SET HT_season_wins_SU = ?, HT_season_losses_SU = ?, HT_season_ties_SU = ?, HT_season_record_SU = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                        season_wins, season_losses, season_ties, season_record, current_season_year, week_number, team_home, team_away)

            # Determine whether the team won or lost the game
            # Initialize useful variables
            home_score = game["home_score"]
            away_score = game["away_score"]
            # If home team won
            if home_score > away_score:
                season_wins += 1
                home_SU = "Win"
            # If away team won
            elif home_score < away_score:
                season_losses += 1
                home_SU = "Loss"
            else:
                season_ties += 1
                home_SU = "Tie"

            # Store the result of the game for that week
            db.execute("UPDATE NFL_reg_season_spreads SET home_SU = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                       home_SU, current_season_year, week_number, team_home, team_away)

        # If the team is away
        elif game["team_away"] == team_name:

            # Store the season recod as a string to be input into the table before the wins, losses, or ties are added so the record doesn't count the current week
            season_record = str(season_wins) + "-" + str(season_losses) + "-" + str(season_ties)

            # Fill only the AT (away team) columns in the table
            db.execute("UPDATE NFL_reg_season_spreads SET AT_season_wins_SU = ?, AT_season_losses_SU = ?, AT_season_ties_SU = ?, AT_season_record_SU = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                        season_wins, season_losses, season_ties, season_record, current_season_year, week_number, team_home, team_away)

            # Determine whether the team won or lost the game
            # Initialize useful variables
            home_score = game["home_score"]
            away_score = game["away_score"]
            # If away team won
            if home_score < away_score:
                season_wins += 1
                away_SU = "Win"
            # If home team won
            elif home_score > away_score:
                season_losses += 1
                away_SU = "Loss"
            else:
                season_ties += 1
                away_SU = "Tie"

            # Store the result of the game for that week
            db.execute("UPDATE NFL_reg_season_spreads SET away_SU = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                       away_SU, current_season_year, week_number, team_home, team_away)

        # Update the previous_season_year variable to be compared to next loop
        previous_season_year = current_season_year

    return

def det_team_record_as(team_name):
    # Initialize variables for counting wins and losses
    season_wins_AS = 0
    season_losses_AS = 0
    season_pushes_AS = 0
    current_season_year = 0
    previous_season_year = 0

    # Get the columns needed where the team being looked at played
    games = db.execute("SELECT team_home, team_away, home_score, away_score, season_year, week_number, favorite_spread, fav_home_away FROM NFL_reg_season_spreads WHERE team_home = ? OR team_away = ?",
                        team_name, team_name)

    # Iterate through all the games and tally the wins and losses
    for game in games:
        # Set all relevant data from table as a usable variable
        week_number = game["week_number"]
        team_home = game["team_home"]
        team_away = game["team_away"]
        current_season_year = game["season_year"]
        fav_home_away = game["fav_home_away"]
        favorite_spread = game["favorite_spread"]
        home_score = game["home_score"]
        away_score = game["away_score"]

        # Adjust the score of the favorite with the spread
        if fav_home_away == "Home":
            home_score = home_score + favorite_spread
        elif fav_home_away == "Away":
            away_score = away_score + favorite_spread

        # Check if the season has changed, and if it has reset the wins, losses, and ties
        if previous_season_year == 0 or current_season_year == previous_season_year:
            # Using the pass statement here because I simply want nothing to happen if one of the above conditions are met
            pass
        else:
            season_wins_AS = 0
            season_losses_AS = 0
            season_pushes_AS = 0

        # If the team is home
        if game["team_home"] == team_name:

            # Store the season recod as a string to be input into the table
            season_record_AS = str(season_wins_AS) + "-" + str(season_losses_AS) + "-" + str(season_pushes_AS)

            # Fill only the HT (home team) columns in the table
            # Store the teams current record in the proper column and row of the table before the win, loss, or, push is recorded
            db.execute("UPDATE NFL_reg_season_spreads SET HT_season_wins_AS = ?, HT_season_losses_AS = ?, HT_season_pushes_AS = ?, HT_season_record_AS = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                        season_wins_AS, season_losses_AS, season_pushes_AS, season_record_AS, current_season_year, week_number, team_home, team_away)

            # Determine whether the team won or lost the game
            # If home team won
            if home_score > away_score:
                season_wins_AS += 1
                home_AS = "Win"
            # If away team won
            elif home_score < away_score:
                season_losses_AS += 1
                home_AS = "Loss"
            else:
                season_pushes_AS += 1
                home_AS = "Push"

            # Store the result of the game for that week
            db.execute("UPDATE NFL_reg_season_spreads SET home_AS = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                       home_AS, current_season_year, week_number, team_home, team_away)

        # If the team is away
        elif game["team_away"] == team_name:

            # Store the season recod as a string to be input into the table
            season_record_AS = str(season_wins_AS) + "-" + str(season_losses_AS) + "-" + str(season_pushes_AS)

            # Fill only the AT (away team) columns in the table
            # Store the teams current record in the proper column and row of the table before the win, loss, or push is recorded
            db.execute("UPDATE NFL_reg_season_spreads SET AT_season_wins_AS = ?, AT_season_losses_AS = ?, AT_season_pushes_AS = ?, AT_season_record_AS = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                        season_wins_AS, season_losses_AS, season_pushes_AS, season_record_AS, current_season_year, week_number, team_home, team_away)

            # Determine whether the team won or lost the game
            # If away team won
            if home_score < away_score:
                season_wins_AS += 1
                away_AS = "Win"
            # If home team won
            elif home_score > away_score:
                season_losses_AS += 1
                away_AS = "Loss"
            else:
                season_pushes_AS += 1
                away_AS = "Push"

            # Store the result of the game for that week
            db.execute("UPDATE NFL_reg_season_spreads SET away_AS = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                       away_AS, current_season_year, week_number, team_home, team_away)

        # Update the previous_season_year variable to be compared to next loop
        previous_season_year = current_season_year

    return

def total_score(home_score, away_score):
    # Get the total score of a game
    total_points = home_score + away_score
    return total_points

def game_over_under(total_points, over_under_total):
    if over_under_total == 0:
        return "None"
    elif over_under_total < total_points:
        return "Over"
    elif over_under_total > total_points:
        return "Under"
    else:
        return "Push"

def det_over_under_record(team_name):
    # Initialize variables for counting wins and losses
    season_overs = 0
    season_unders = 0
    season_pushes_OU = 0
    current_season_year = 0
    previous_season_year = 0

    # Get the columns needed where the team being looked at played
    games = db.execute("SELECT team_home, team_away, home_score, away_score, over_under_total, season_year, week_number FROM NFL_reg_season_spreads WHERE team_home = ? OR team_away = ?",
                        team_name, team_name)

    # Iterate through all the games and tally the wins and losses
    for game in games:
        # Set the week_number, team_home, and team_away to their current varioables in this row for exact insertion of new data in the table at the bottom
        week_number = game["week_number"]
        team_home = game["team_home"]
        team_away = game["team_away"]

        # Set the current_season_year variable at the start of each loop to make sure wins and losses are only added for the same season
        current_season_year = game["season_year"]

        # Check if the season has changed, and if it has reset the wins, losses, and ties
        if previous_season_year == 0 or current_season_year == previous_season_year:
            # Using the pass statement here because I simply want nothing to happen if one of the above conditions are met
            pass
        else:
            season_overs = 0
            season_unders = 0
            season_pushes_OU = 0

        # Initialize variables from the table and use them to get the total_score and whether it was over, under, or psuhed
        home_score = game["home_score"]
        away_score = game["away_score"]
        total_points = total_score(home_score, away_score)
        over_under_total = game["over_under_total"]
        OU_result = game_over_under(total_points, over_under_total)

        # If the team is home
        if game["team_home"] == team_name:

            # Store the season recod as a string to be input into the table before the over_under_result is recorded
            OU_season_record = str(season_overs) + "-" + str(season_unders) + "-" + str(season_pushes_OU)

            # Fill only the HT (home team) columns in the table
            # Store the teams current record in the proper column and row of the table
            db.execute("UPDATE NFL_reg_season_spreads SET HT_season_overs = ?, HT_season_unders = ?, HT_season_pushes_OU = ?, HT_season_record_OU = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                       season_overs, season_unders, season_pushes_OU, OU_season_record, current_season_year, week_number, team_home, team_away)

            # Determine whether over_under_result is "OVER", "UNDER", "PUSH", or "NONE"
            if OU_result == "Over":
                season_overs += 1
            elif OU_result == "Under":
                season_unders += 1
            elif OU_result == "Push":
                season_pushes += 1
            elif OU_result == "None":
                pass

        # If the team is away
        elif game["team_away"] == team_name:

            # Store the season recod as a string to be input into the table before the over_under_result is recorded
            OU_season_record = str(season_overs) + "-" + str(season_unders) + "-" + str(season_pushes_OU)

            # Fill only the AT (away team) columns in the table
            # Store the teams current record in the proper column and row of the table
            db.execute("UPDATE NFL_reg_season_spreads SET AT_season_overs = ?, AT_season_unders = ?, AT_season_pushes_OU = ?, AT_season_record_OU = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                        season_overs, season_unders, season_pushes_OU, OU_season_record, current_season_year, week_number, team_home, team_away)

            # Determine whether over_under_result is "OVER", "UNDER", "PUSH", or "NONE"
            if OU_result == "Over":
                season_overs += 1
            elif OU_result == "Under":
                season_unders += 1
            elif OU_result == "Push":
                season_pushes += 1
            elif OU_result == "None":
                pass

        # Update the over_under_result for that weeks game
        db.execute("UPDATE NFL_reg_season_spreads SET OU_result = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
                   OU_result, current_season_year, week_number, team_home, team_away)

        # Update the previous_season_year variable to be compared to next loop
        previous_season_year = current_season_year

    return