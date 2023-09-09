from cs50 import SQL

from critical_functions import det_fav_home_away, det_team_record_su, det_team_record_as, det_over_under_record

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:////workspaces/126349338/Final_Project/NFL.db")

# get the needed columns from NFL_reg_season_spreads table into python as games
# then changed to NFL_post_season_spreads table and changed week_number to Playoff_round and ran again to fill that table as-well
games = db.execute("SELECT team_home, team_away, team_favorite_id, season_year, week_number FROM NFL_reg_season_spreads")

# loop through each row of the table and fill the new fav_home_away column
for game in games:
    # define the variables needed to input into the function that we get from the rows of the table we just grabbed from sql
    team_home = game["team_home"]
    team_away = game["team_away"]
    team_favorite_id = game["team_favorite_id"]
    # define these variable so we can enter the data back into the sql table at the proper location
    season_year = game["season_year"]
    week_number = game["week_number"]
    # call the function and store it's output as what will be entered into the sql table
    fav_home_away = det_fav_home_away(team_home, team_away, team_favorite_id)
    # enter the data returned by the funtion and stored in fav_home_away into the proper location of the sql table
    db.execute("UPDATE NFL_reg_season_spreads SET fav_home_away = ? WHERE season_year = ? AND week_number = ? AND team_home = ? AND team_away = ?",
               fav_home_away, season_year, week_number, team_home, team_away)

# Get the team_name for all teams in our NFL teams table into a a table
nfl_teams = db.execute("SELECT DISTINCT team_name FROM NFL_teams")

# loop through each row of the teams table and fill the wins, losses, ties, and record for each team through every season STRAGHT UP
for nfl_team in nfl_teams:
    team_name = nfl_team["team_name"]
    det_team_record_su(team_name)

# loop through each row of the teams table and fill the wns, losses, pushes, and record for each team through every season AGAINST THE SPREAD
for nfl_team in nfl_teams:
    team_name = nfl_team["team_name"]
    det_team_record_as(team_name)

# Loop through each team and fill in the columns of NFL_reg_season_spreads table wih each teams overs, unders, pushes, and record_OU
for nfl_team in nfl_teams:
    team_name = nfl_team["team_name"]
    det_over_under_record(team_name)

# Insert the data from the NFL_reg_season_spreads table into the NFL_post_season_spreads table so it can be used for analysis and predictions
# Get the needed data from the NFL_post_season_spreads table
playoff_games = db.execute("SELECT season_year, team_home, team_away FROM NFL_post_season_spreads")

# loop through each row of the playoff_games table and fill the wins, losses, ties, pushes, and record from the regular season for each team through every season
for playoff_game in playoff_games:
    # Initialize variables needed to insert data back into correct spot in post_season table and search need data from reg_season table
    # This is all you need to insert the data because the same teams can never play twice in the same year because the playoffs are single elimination
    season_year = playoff_game["season_year"]
    team_home = playoff_game["team_home"]
    team_away = playoff_game["team_away"]

    # No spread data on regular season games before 1979 so only do this for post season games from 1979 and on
    if season_year < 1979:
        continue
    else:
        # Use the season_year and determine what is the week_number of the last game of the regular season
        final_week_db = db.execute("SELECT week_number FROM NFL_reg_season_spreads WHERE season_year = ? ORDER BY week_number DESC", season_year)
        final_week = final_week_db[0]["week_number"]

        # Search reg_season table for the final regular season game for each team playing in the playoff game and get the neccessary data
        # to enter into the post_season table

        # First do the home team
        team_home_game = db.execute("SELECT team_home, team_away FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND (team_home = ? OR team_away = ?)",
                                    season_year, final_week, team_home, team_home)

        # Determine if the home playoff team is the home team or way team in their final regular season game being looked at to get the correct data
        if team_home == team_home_game[0]["team_home"]:
            team_home_data = db.execute("SELECT HT_season_wins_SU, HT_season_losses_SU, HT_season_ties_SU, HT_season_wins_AS, HT_season_losses_AS, HT_season_pushes_AS, HT_season_overs, HT_season_unders, HT_season_pushes_OU, home_SU, home_AS, OU_result FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND team_home = ?",
                                        season_year, final_week, team_home)
            # Initialize needed variables for the new records
            HT_season_wins_SU = team_home_data[0]["HT_season_wins_SU"]
            HT_season_losses_SU = team_home_data[0]["HT_season_losses_SU"]
            HT_season_ties_SU = team_home_data[0]["HT_season_ties_SU"]
            HT_season_wins_AS = team_home_data[0]["HT_season_wins_AS"]
            HT_season_losses_AS = team_home_data[0]["HT_season_losses_AS"]
            HT_season_pushes_AS = team_home_data[0]["HT_season_pushes_AS"]
            HT_season_overs = team_home_data[0]["HT_season_overs"]
            HT_season_unders = team_home_data[0]["HT_season_unders"]
            HT_season_pushes_OU = team_home_data[0]["HT_season_pushes_OU"]

            # Initialize variables to calculate the new record after the final week of the regular season
            home_team_SU = team_home_data[0]["home_SU"]
            home_team_AS = team_home_data[0]["home_AS"]

        elif team_home == team_home_game[0]["team_away"]:
            team_home_data = db.execute("SELECT AT_season_wins_SU, AT_season_losses_SU, AT_season_ties_SU, AT_season_wins_AS, AT_season_losses_AS, AT_season_pushes_AS, AT_season_overs, AT_season_unders, AT_season_pushes_OU, away_SU, away_AS, OU_result FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND team_away = ?",
                                        season_year, final_week, team_home)
            HT_season_wins_SU = team_home_data[0]["AT_season_wins_SU"]
            HT_season_losses_SU = team_home_data[0]["AT_season_losses_SU"]
            HT_season_ties_SU = team_home_data[0]["AT_season_ties_SU"]
            HT_season_wins_AS = team_home_data[0]["AT_season_wins_AS"]
            HT_season_losses_AS = team_home_data[0]["AT_season_losses_AS"]
            HT_season_pushes_AS = team_home_data[0]["AT_season_pushes_AS"]
            HT_season_overs = team_home_data[0]["AT_season_overs"]
            HT_season_unders = team_home_data[0]["AT_season_unders"]
            HT_season_pushes_OU = team_home_data[0]["AT_season_pushes_OU"]

            # Initialize variables to calculate the new record after the final week of the regular season
            home_team_SU = team_home_data[0]["away_SU"]
            home_team_AS = team_home_data[0]["away_AS"]

        # Initialize the final weeks over under data for the new record calculations
        OU_result = team_home_data[0]["OU_result"]

        # Make the new records to be stored for each playoff team by adding the result of the final week SU, AS, and OU to a new string to be stored
        # Straight up season record
        if home_team_SU == "Win":
            HT_season_wins_SU = (HT_season_wins_SU + 1)
            HT_season_record_SU = str(HT_season_wins_SU) + "-" + str(HT_season_losses_SU) + "-" + str(HT_season_ties_SU)
        elif home_team_SU == "Loss":
            HT_season_losses_SU = (HT_season_losses_SU + 1)
            HT_season_record_SU = str(HT_season_wins_SU) + "-" + str(HT_season_losses_SU) + "-" + str(HT_season_ties_SU)
        elif home_team_SU == "Tie":
            HT_season_ties_SU = (HT_season_ties_SU + 1)
            HT_season_record_SU = str(HT_season_wins_SU) + "-" + str(HT_season_losses_SU) + "-" + str(HT_season_ties_SU)
        # Against the spread season record
        if home_team_AS == "Win":
            HT_season_wins_AS = (HT_season_wins_AS + 1)
            HT_season_record_AS = str(HT_season_wins_AS) + "-" + str(HT_season_losses_AS) + "-" + str(HT_season_pushes_AS)
        elif home_team_AS == "Loss":
            HT_season_losses_AS = (HT_season_losses_AS + 1)
            HT_season_record_AS = str(HT_season_wins_AS) + "-" + str(HT_season_losses_AS) + "-" + str(HT_season_pushes_AS)
        elif home_team_AS == "Push":
            HT_season_pushes_AS = (HT_season_pushes_AS + 1)
            HT_season_record_AS = str(HT_season_wins_AS) + "-" + str(HT_season_losses_AS) + "-" + str(HT_season_pushes_AS)
        # Over-Under season record
        if OU_result == "None":
            HT_season_record_OU = str(HT_season_overs) + "-" + str(HT_season_unders) + "-" + str(HT_season_pushes_OU)
        elif OU_result == "Over":
            HT_season_overs = (HT_season_overs + 1)
            HT_season_record_OU = str(HT_season_overs) + "-" + str(HT_season_unders) + "-" + str(HT_season_pushes_OU)
        elif OU_result == "Under":
            HT_season_unders = (HT_season_unders + 1)
            HT_season_record_OU = str(HT_season_overs) + "-" + str(HT_season_unders) + "-" + str(HT_season_pushes_OU)
        elif OU_result == "Push":
            HT_season_pushes_OU = (HT_season_pushes_OU + 1)
            HT_season_record_OU = str(HT_season_overs) + "-" + str(HT_season_unders) + "-" + str(HT_season_pushes_OU)

        # Insert the data into the NFL_post_season_spreads table
        db.execute("UPDATE NFL_post_season_spreads SET HT_reg_season_wins_SU = ?, HT_reg_season_losses_SU = ?, HT_reg_season_ties_SU = ?, HT_reg_season_record_SU = ?, HT_reg_season_wins_AS = ?, HT_reg_season_losses_AS = ?, HT_reg_season_pushes_AS = ?, HT_reg_season_record_AS = ?, HT_reg_season_overs = ?, HT_reg_season_unders = ?, HT_reg_season_pushes_OU = ?, HT_reg_season_record_OU = ? WHERE season_year = ? AND team_home = ? AND team_away = ?",
                   HT_season_wins_SU, HT_season_losses_SU, HT_season_ties_SU, HT_season_record_SU, HT_season_wins_AS, HT_season_losses_AS, HT_season_pushes_AS, HT_season_record_AS, HT_season_overs, HT_season_unders, HT_season_pushes_OU, HT_season_record_OU, season_year, team_home, team_away)

        # Now do the away team
        team_away_game = db.execute("SELECT team_home, team_away FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND (team_home = ? OR team_away = ?)",
                                    season_year, final_week, team_away, team_away)

        # Determine if the away playoff team is the home team or way team in their final regular season game being looked at to get the correct data
        if team_away == team_away_game[0]["team_home"]:
            team_away_data = db.execute("SELECT HT_season_wins_SU, HT_season_losses_SU, HT_season_ties_SU, HT_season_wins_AS, HT_season_losses_AS, HT_season_pushes_AS, HT_season_overs, HT_season_unders, HT_season_pushes_OU, home_SU, home_AS, OU_result FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND team_home = ?",
                                        season_year, final_week, team_away)
            AT_season_wins_SU = team_away_data[0]["HT_season_wins_SU"]
            AT_season_losses_SU = team_away_data[0]["HT_season_losses_SU"]
            AT_season_ties_SU = team_away_data[0]["HT_season_ties_SU"]
            AT_season_wins_AS = team_away_data[0]["HT_season_wins_AS"]
            AT_season_losses_AS = team_away_data[0]["HT_season_losses_AS"]
            AT_season_pushes_spread = team_away_data[0]["HT_season_pushes_AS"]
            AT_season_overs = team_away_data[0]["HT_season_overs"]
            AT_season_unders = team_away_data[0]["HT_season_unders"]
            AT_season_pushes_OU = team_away_data[0]["HT_season_pushes_OU"]

            # Initialize variables to calculate the new record after the final week of the regular season
            away_team_SU = team_away_data[0]["home_SU"]
            away_team_AS = team_away_data[0]["home_AS"]

        elif team_away == team_away_game[0]["team_away"]:
            team_away_data = db.execute("SELECT AT_season_wins_SU, AT_season_losses_SU, AT_season_ties_SU, AT_season_wins_AS, AT_season_losses_AS, AT_season_pushes_AS, AT_season_overs, AT_season_unders, AT_season_pushes_OU, away_SU, away_AS, OU_result FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND team_away = ?",
                                        season_year, final_week, team_away)
            AT_season_wins_SU = team_away_data[0]["AT_season_wins_SU"]
            AT_season_losses_SU = team_away_data[0]["AT_season_losses_SU"]
            AT_season_ties_SU = team_away_data[0]["AT_season_ties_SU"]
            AT_season_wins_AS = team_away_data[0]["AT_season_wins_AS"]
            AT_season_losses_AS = team_away_data[0]["AT_season_losses_AS"]
            AT_season_pushes_AS = team_away_data[0]["AT_season_pushes_AS"]
            AT_season_overs = team_away_data[0]["AT_season_overs"]
            AT_season_unders = team_away_data[0]["AT_season_unders"]
            AT_season_pushes_OU = team_away_data[0]["AT_season_pushes_OU"]

            # Initialize variables to calculate the new record after the final week of the regular season
            away_team_SU = team_away_data[0]["away_SU"]
            away_team_AS = team_away_data[0]["away_AS"]

        # Initialize the final weeks over under data for the new record calculations
        OU_result = team_away_data[0]["OU_result"]

        # Make the new records to be stored for each playoff team by adding the result of the final week SU, AS, and OU to a new string to be stored
        # Straight up season record
        if away_team_SU == "Win":
            AT_season_wins_SU = (AT_season_wins_SU + 1)
            AT_season_record_SU = str(AT_season_wins_SU) + "-" + str(AT_season_losses_SU) + "-" + str(AT_season_ties_SU)
        elif away_team_SU == "Loss":
            AT_season_losses_SU = (AT_season_losses_SU + 1)
            AT_season_record_SU = str(AT_season_wins_SU) + "-" + str(AT_season_losses_SU) + "-" + str(AT_season_ties_SU)
        elif away_team_SU == "Tie":
            AT_season_ties_SU = (AT_season_ties_SU + 1)
            AT_season_record_SU = str(AT_season_wins_SU) + "-" + str(AT_season_losses_SU) + "-" + str(AT_season_ties_SU)
        # Against the spread season record
        if away_team_AS == "Win":
            AT_season_wins_AS = (AT_season_wins_AS + 1)
            AT_season_record_AS = str(AT_season_wins_AS) + "-" + str(AT_season_losses_AS) + "-" + str(AT_season_pushes_AS)
        elif away_team_AS == "Loss":
            AT_season_losses_AS = (AT_season_losses_AS + 1)
            AT_season_record_AS = str(AT_season_wins_AS) + "-" + str(AT_season_losses_AS) + "-" + str(AT_season_pushes_AS)
        elif away_team_AS == "Push":
            AT_season_pushes_AS = (AT_season_pushes_AS + 1)
            AT_season_record_AS = str(AT_season_wins_AS) + "-" + str(AT_season_losses_AS) + "-" + str(AT_season_pushes_AS)
        # Over-Under season record
        if OU_result == "None":
            AT_season_record_OU = str(AT_season_overs) + "-" + str(AT_season_unders) + "-" + str(AT_season_pushes_OU)
        elif OU_result == "Over":
            AT_season_overs = (AT_season_overs + 1)
            AT_season_record_OU = str(AT_season_overs) + "-" + str(AT_season_unders) + "-" + str(AT_season_pushes_OU)
        elif OU_result == "Under":
            AT_season_unders = (AT_season_unders + 1)
            AT_season_record_OU = str(AT_season_overs) + "-" + str(AT_season_unders) + "-" + str(AT_season_pushes_OU)
        elif OU_result == "Push":
            AT_season_pushes_OU = (AT_season_pushes_OU + 1)
            AT_season_record_OU = str(AT_season_overs) + "-" + str(AT_season_unders) + "-" + str(AT_season_pushes_OU)

        # Insert the data into the NFL_post_season_spreads table
        db.execute("UPDATE NFL_post_season_spreads SET AT_reg_season_wins_SU = ?, AT_reg_season_losses_SU = ?, AT_reg_season_ties_SU = ?, AT_reg_season_record_SU = ?, AT_reg_season_wins_AS = ?, AT_reg_season_losses_AS = ?, AT_reg_season_pushes_AS = ?, AT_reg_season_record_AS = ?, AT_reg_season_overs = ?, AT_reg_season_unders = ?, AT_reg_season_pushes_OU = ?, AT_reg_season_record_OU = ? WHERE season_year = ? AND team_home = ? AND team_away = ?",
                   AT_season_wins_SU, AT_season_losses_SU, AT_season_ties_SU, AT_season_record_SU, AT_season_wins_AS, AT_season_losses_AS, AT_season_pushes_AS, AT_season_record_AS, AT_season_overs, AT_season_unders, AT_season_pushes_OU, AT_season_record_OU, season_year, team_home, team_away)

# Insert the result of each playoff game SU, AS, and OU for every season
# Get the needed data from the NFL_post_season_spreads table
playoff_games = db.execute("SELECT season_year, team_home, team_away, home_score, away_score, fav_home_away, favorite_spread, over_under_total FROM NFL_post_season_spreads")

# loop through each row of the playoff_games table and fill the results of each game SU, AS, and OU for each team through every playoff game
for playoff_game in playoff_games:
    # Initialize variables needed to insert data back into correct spot in post_season table and search need data from reg_season table
    # This is all you need to insert the data because the same teams can never play twice in the same year because the playoffs are single elimination
    season_year = playoff_game["season_year"]
    team_home = playoff_game["team_home"]
    team_away = playoff_game["team_away"]

    # Determine who won the game SU
    # Initialize useful variables
    home_score = playoff_game["home_score"]
    away_score = playoff_game["away_score"]

    # Get the total score before it's changed by the spread for use w/ the over-under
    total_score = (home_score + away_score)

    # If the home team wins
    if home_score > away_score:
        home_SU = "Win"
        away_SU = "Loss"
    # If the away team wins
    elif home_score < away_score:
        home_SU = "Loss"
        away_SU = "Win"

    # Determine who won the game AS
    # Initialize useful variables
    fav_home_away = playoff_game["fav_home_away"]
    favorite_spread = playoff_game["favorite_spread"]
    # Add the spread to the favorite's score before comparing
    if fav_home_away == "Home":
        home_score = (home_score + favorite_spread)
    elif fav_home_away == "Away":
        away_score = (away_score + favorite_spread)
    # Determine who won the game AS
    if home_score > away_score:
        home_AS = "Win"
        away_AS = "Loss"
    # If the away team wins
    elif home_score < away_score:
        home_AS = "Loss"
        away_AS = "Win"
    else:
        home_AS = "Push"
        away_AS = "Push"

    # Determine if the game went over or under the total
    # Initialize useful variables
    over_under_total = playoff_game["over_under_total"]
    # Determine if the total score was over, under, or a push compared to the over-under line
    if over_under_total == 0:
        OU_result = "None"
    elif total_score > over_under_total:
        OU_result = "Over"
    elif total_score < over_under_total:
        OU_result = "Under"
    else:
        OU_result = "Push"

    # Update the NFL_post_season_spreads table with the result of each game
    db.execute("UPDATE NFL_post_season_spreads SET home_SU = ?, home_AS = ?, away_SU = ?, away_AS = ?, OU_result = ? WHERE season_year = ? AND team_home = ? AND team_away = ?",
               home_SU, home_AS, away_SU, away_AS, OU_result, season_year, team_home, team_away)