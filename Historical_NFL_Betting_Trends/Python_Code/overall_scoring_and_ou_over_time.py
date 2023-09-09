import numpy as np
import matplotlib.pyplot as plt
from cs50 import SQL
from critical_functions import total_score

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:////workspaces/126349338/Final_Project/NFL.db")

# Has scoring gone up in the NFL per game over the years?
# Get the needed data from each game through the regular season
games = db.execute("SELECT home_score, away_score, over_under_total, season_year FROM NFL_reg_season_spreads")
years = db.execute("SELECT DISTINCT season_year FROM NFL_reg_season_spreads")

# Make a list to fill with each distinct year from the years db
season_years = []
for year in years:
    season_year = year["season_year"]
    season_years.append(season_year)

# Make a list to fill the average total score from each season
average_total_scores = []
average_over_under_totals = []
previous_season_year = 0
total_total_score = 0
total_over_under_total = 0
game_counter = 0

for game in games:
    # Set the current_season_year
    current_season_year = game["season_year"]
    # Check if the season has changed so you can reset variables and store the averages into their lists
    if previous_season_year == 0 or current_season_year == previous_season_year:
        # Using the pass statement here because I simply want nothing to happen if one of the above conditions are met
        pass
    else:
        average_total_score = round((total_total_score / game_counter), 1)
        average_total_scores.append(average_total_score)
        average_over_under_total = round((total_over_under_total / game_counter), 1)
        average_over_under_totals.append(average_over_under_total)
        total_total_score = 0
        total_over_under_total = 0
        game_counter = 0

    # Set the needed variables
    home_score = game["home_score"]
    away_score = game["away_score"]
    over_under_total = game["over_under_total"]
    # Get the total_score
    store_total_score = total_score(home_score, away_score)
    # Add to the totals
    total_total_score += store_total_score
    total_over_under_total += over_under_total
    # Increment the game_counter
    game_counter += 1

    # Store previous_season_year for comparison
    previous_season_year = current_season_year

# Run this to get the final 2022 season results stored in the list since the "else" isn't triggered
average_total_score = round((total_total_score / game_counter), 1)
average_total_scores.append(average_total_score)
average_over_under_total = round((total_over_under_total / game_counter), 1)
average_over_under_totals.append(average_over_under_total)

# Calculate the regression line for each
coefficients_scores = np.polyfit(season_years, average_total_scores, 1)
m_s = coefficients_scores[0]  # slope
b_s = coefficients_scores[1]  # y-intercept
regression_line_scores = np.polyval(coefficients_scores, season_years)

coefficients_OU = np.polyfit(season_years, average_over_under_totals, 1)
m_OU = coefficients_OU[0]  # slope
b_OU = coefficients_OU[1]  # y-intercept
regression_line_OU = np.polyval(coefficients_OU, season_years)

# Chart the both average toals over each season
plt.scatter(season_years, average_total_scores, color = 'red', label = 'Average Total Points Scored')
plt.plot(season_years, regression_line_scores, color = 'red', label = 'Regression Line Scores')
plt.scatter(season_years, average_over_under_totals, color = 'blue', label = 'Average Over/Under Line')
plt.plot(season_years, regression_line_OU, color = 'blue', label = 'Regression Line Over/Under')
plt.xlabel('NFL Season')
plt.ylabel('Points') # of Home-Dog Wins
plt.title('Have Over/Under Lines Risen w/ Overall Scoring?')
plt.legend()
plt.show()