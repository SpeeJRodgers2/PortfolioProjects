import numpy as np
import matplotlib.pyplot as plt
from cs50 import SQL
from critical_functions import total_score, game_over_under

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:////workspaces/126349338/Final_Project/NFL.db")

# Has scoring gone up in the NFL per game over the years?
# Get the needed data from each game through the regular season
games = db.execute("SELECT home_score, away_score, over_under_total, season_year, week_number FROM NFL_reg_season_spreads")
years = db.execute("SELECT DISTINCT season_year FROM NFL_reg_season_spreads")

# Make a list to fill with each distinct year from the years db
season_years = []
for year in years:
    season_year = year["season_year"]
    season_years.append(season_year)

# Make a list to fill the average total score from each season
percent_early_unders = []
percent_mid_OUs = []
percent_late_overs = []

# Initialize season_year variables
previous_season_year = 0

# Initialize variables for early, mid, and late season percentages
early_season_games = 0
mid_season_games = 0
late_season_games = 0
early_season_unders = 0
mid_season_overs = 0
late_season_overs = 0

# Go through the games and seperate the season into early, mid, and late then check and store the over under percentages in each
for game in games:
    current_season_year = game["season_year"]
    if current_season_year != previous_season_year:
        final_week_db = db.execute("SELECT week_number FROM NFL_reg_season_spreads WHERE season_year = ? ORDER BY week_number DESC",
                                current_season_year)
        final_week = final_week_db[0]["week_number"]
        # Break the season into 3rds to evaluate early, mid, and late season OU
        if final_week == 9:
            early_season_weeks = list(range(1,4))
            mid_season_weeks = list(range(4,7))
            late_season_weeks = list(range(7,10))
        elif final_week == 16:
            early_season_weeks = list(range(1,6))
            mid_season_weeks = list(range(6,11))
            late_season_weeks = list(range(11,17))
        elif final_week == 17:
            early_season_weeks = list(range(1,6))
            mid_season_weeks = list(range(6,12))
            late_season_weeks = list(range(12,18))
        elif final_week == 18:
            early_season_weeks = list(range(1,7))
            mid_season_weeks = list(range(7,13))
            late_season_weeks = list(range(13,19))

    # Determine if the season changed, if it's a new season calculate and store each over under percentage in the proper list
    if previous_season_year == 0 or current_season_year == previous_season_year:
        pass
    else:
        # Calculate the percentage and store it in the proper list
        percent_early_under = 100 * round(early_season_unders / early_season_games, 3)
        percent_early_unders.append(percent_early_under)
        percent_mid_OU = 100 * round(mid_season_overs / mid_season_games, 3)
        percent_mid_OUs.append(percent_mid_OU)
        percent_late_over = 100 * round(late_season_overs / late_season_games, 3)
        percent_late_overs.append(percent_late_over)
        # Reset the varaible for the season
        early_season_games = 0
        mid_season_games = 0
        late_season_games = 0
        early_season_unders = 0
        mid_season_overs = 0
        late_season_overs = 0

    # Initialize the needed variables from the game
    week_number = game["week_number"]
    home_score = game["home_score"]
    away_score = game["away_score"]
    over_under_total = game["over_under_total"]

    # Use functions to get the total score and the result of the game
    game_total_score = total_score(home_score, away_score)
    game_result = game_over_under(game_total_score, over_under_total)

    # Determine if the game is early, mid, or late season and increment the correct variables depending on the result
    if week_number in early_season_weeks:
        if game_result == "Under":
            early_season_unders += 1
            early_season_games += 1
        elif game_result == "Over":
            early_season_games += 1
        else:
            pass
    elif week_number in mid_season_weeks:
        if game_result == "Over":
            mid_season_overs += 1
            mid_season_games += 1
        elif game_result == "Under":
            mid_season_games += 1
        else:
            pass
    elif week_number in late_season_weeks:
        if game_result == "Over":
            late_season_overs += 1
            late_season_games += 1
        elif game_result == "Under":
            late_season_games += 1
        else:
            pass

    # Set the previous_season_year variable to be compared to in the next loop
    previous_season_year = current_season_year

# Calculate the percentage and store it in the proper list from the final season since the else statement isn't triggered for 2022 season
percent_early_under = 100 * round(early_season_unders / early_season_games, 3)
percent_early_unders.append(percent_early_under)
percent_mid_OU = 100 * round(mid_season_overs / mid_season_games, 3)
percent_mid_OUs.append(percent_mid_OU)
percent_late_over = 100 * round(late_season_overs / late_season_games, 3)
percent_late_overs.append(percent_late_over)

# Calculate the regression line for each
coefficients_early = np.polyfit(season_years, percent_early_unders, 1)
m_s = coefficients_early[0]  # slope
b_s = coefficients_early[1]  # y-intercept
regression_line_early = np.polyval(coefficients_early, season_years)

coefficients_mid = np.polyfit(season_years, percent_mid_OUs, 1)
m_OU = coefficients_mid[0]  # slope
b_OU = coefficients_mid[1]  # y-intercept
regression_line_mid = np.polyval(coefficients_mid, season_years)

coefficients_late = np.polyfit(season_years, percent_late_overs, 1)
m_OU = coefficients_late[0]  # slope
b_OU = coefficients_late[1]  # y-intercept
regression_line_late = np.polyval(coefficients_late, season_years)

# Chart both percentages of highest overs and lowest unders for each season
plt.scatter(season_years, percent_early_unders, color = 'red', label = 'Percentage of Early Season Unders')
plt.plot(season_years, regression_line_early, color = 'red', label = 'Regression Line')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders Early in Season')
plt.title('Do Unders Hit More Often Early in the Season?')
plt.legend()
plt.show()

# Chart the juice lost each season on pushes
plt.scatter(season_years, percent_mid_OUs, color = 'green', label = 'Percent of Mid Season Overs')
plt.plot(season_years, regression_line_mid, color = 'green', label = 'Regression Line')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Overs Mid Season')
plt.title('Does the Over Hit Rate Shift in the Middle of the Season?')
plt.legend()
plt.show()

plt.scatter(season_years, percent_late_overs, color = 'blue', label = 'Percent of Late Season Overs')
plt.plot(season_years, regression_line_late, color = 'blue', label = 'Regression Line')
plt.xlabel('NFL Season')
plt.ylabel('Percent of Overs Late in Season')
plt.title('Do Overs Hit More Often Late in the Season?')
plt.legend()
plt.show()