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
percent_over_highest_totals = []
percent_under_lowest_totals = []
total_juice_lost = []
# Initialize these so there's a nunber to be compared to at the start of a week (lowest_week_OU_total can't be 0 because it would never be stored or changed)
highest_week_OU_total = 0
lowest_week_OU_total = 100
# These are to store the number of times either goes over or under in a week throughout a season
highest_week_OU_overs = 0
lowest_week_OU_unders = 0
# Need these to reset variables or not
previous_season_year = 0
previous_game_week = 0
# Need this to calculate the prcentage of overs or unders throghout the season
high_game_counter = 0
low_game_counter = 0
# For the case of same lowest or highest OU totals in a week
multiple_highest_OU = 0
multiple_lowest_OU = 0
highest_games_overs = 0
highest_games_unders = 0
lowest_games_overs = 0
lowest_games_unders = 0
juice_lost = 0

for game in games:
    # Set the current_season_year and week_number
    current_season_year = game["season_year"]
    current_game_week = game["week_number"]

    # Check if the week number changed so you can reset variables
    if previous_game_week == 0 or current_game_week == previous_game_week:
        pass
    else:
        # If there is only one total to check
        if multiple_highest_OU < 1:
            highest_week_OU_result = game_over_under(highest_week_total_score, highest_week_OU_total)
            # Use the highest result for later calculations
            if highest_week_OU_result == "Over":
                highest_week_OU_overs += 1
                high_game_counter += 1
            elif highest_week_OU_result == "Under":
                high_game_counter += 1
                pass
            # Shouldn't affect percentage at end so nothing is done
            elif highest_week_OU_result == "Push":
                pass
        else:
            # Check every highest game and compare the results
            highest_games = db.execute("SELECT home_score, away_score, over_under_total FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND over_under_total = ?",
                                       previous_season_year, previous_game_week, highest_week_OU_total)
            # Loop through and see what the result of each is
            for highest_game in highest_games:
                home_score = highest_game["home_score"]
                away_score = highest_game["away_score"]
                temp_high_OU_total = highest_game["over_under_total"]
                temp_total_score = total_score(home_score, away_score)
                temp_OU_result = game_over_under(temp_total_score, temp_high_OU_total)
                if temp_OU_result == "Over":
                    highest_games_overs += 1
                elif temp_OU_result == "Under":
                    highest_games_unders += 1
                else:
                    pass
            # Lost the juice of the bets since they went even and amount of juice * the number of bets that washed / 2 so just use one of the variables
            if highest_games_overs == highest_games_unders:
                juice_lost += highest_games_overs
                pass
            # Add more weight to the percentage since it would be multiple wins
            elif highest_games_overs > highest_games_unders:
                highest_week_OU_overs += (1 * (highest_games_overs - highest_games_unders))
                high_game_counter += (1 * (highest_games_overs - highest_games_unders))
            # Take away more weight from the overs IF it's a difference of more than one, since the week_counter will already account one as a loss
            elif highest_games_overs < highest_games_unders:
                high_game_counter += (1 * (highest_games_unders - highest_games_overs))

        # If there is only one total to check
        if multiple_lowest_OU < 1:
            lowest_week_OU_result = game_over_under(lowest_week_total_score, lowest_week_OU_total)
            # Now do the lowest result
            if lowest_week_OU_result == "Under":
                lowest_week_OU_unders += 1
                low_game_counter += 1
            elif lowest_week_OU_result == "Over":
                low_game_counter += 1
                pass
            # Shouldn't affect percentage at end so nothing is done
            elif lowest_week_OU_result == "Push":
                pass
        else:
            # Check every highest game and compare the results
            lowest_games = db.execute("SELECT home_score, away_score, over_under_total FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND over_under_total = ?",
                                       previous_season_year, previous_game_week, lowest_week_OU_total)
            # Loop through and see what the result of each is
            for lowest_game in lowest_games:
                home_score = lowest_game["home_score"]
                away_score = lowest_game["away_score"]
                temp_low_OU_total = lowest_game["over_under_total"]
                temp_total_score = total_score(home_score, away_score)
                temp_OU_result = game_over_under(temp_total_score, temp_low_OU_total)
                if temp_OU_result == "Over":
                    lowest_games_overs += 1
                elif temp_OU_result == "Under":
                    lowest_games_unders += 1
                else:
                    pass
            # Lost the juice of the bets since they went even and amount of juice * the number of bets that washed / 2 so just use one of the variables
            if lowest_games_overs == lowest_games_unders:
                juice_lost += lowest_games_unders
                pass
            # Add more weight to the percentage since it would be multiple wins
            elif lowest_games_overs < lowest_games_unders:
                lowest_week_OU_unders += (1 * (lowest_games_unders - lowest_games_overs))
                low_game_counter += (1 * (lowest_games_unders - lowest_games_overs))
            # Take away more weight from the overs IF it's a difference of more than one, since the week_counter will already account one as a loss
            elif lowest_games_overs > lowest_games_unders:
                low_game_counter += (1 * (lowest_games_overs - lowest_games_unders))

        # Now reset the variables for the new week
        highest_week_OU_total = 0
        lowest_week_OU_total = 100
        multiple_highest_OU = 0
        multiple_lowest_OU = 0
        highest_games_overs = 0
        highest_games_unders = 0
        lowest_games_overs = 0
        lowest_games_unders = 0

    # Check if the season has changed so you can reset variables and store the averages into their lists
    if previous_season_year == 0 or current_season_year == previous_season_year:
        # Using the pass statement here because I simply want nothing to happen if one of the above conditions are met
        pass
    else:
        # When the season changes find the percentage and store it in the appropriate list and reset certain variables
        percent_over_highest_total = 100 * round(highest_week_OU_overs / high_game_counter, 3)
        percent_over_highest_totals.append(percent_over_highest_total)
        percent_under_lowest_total = 100 * round(lowest_week_OU_unders / low_game_counter, 3)
        percent_under_lowest_totals.append(percent_under_lowest_total)
        total_juice_lost.append(juice_lost)
        # Reset neccessary variables for the new season
        high_game_counter = 0
        low_game_counter = 0
        highest_week_OU_overs = 0
        lowest_week_OU_unders = 0
        juice_lost = 0

    # Set the needed variables
    home_score = game["home_score"]
    away_score = game["away_score"]
    over_under_total = game["over_under_total"]
    # Get the total_score
    store_total_score = total_score(home_score, away_score)
    # Is it the highest OU total of the week?
    if over_under_total > highest_week_OU_total:
        highest_week_OU_total = over_under_total
        highest_week_total_score = store_total_score
        # Incase there are multiple weeks with the same total that need to be looked at for the betting strategy
        multiple_highest_OU = 0
    elif over_under_total == highest_week_OU_total:
        multiple_highest_OU += 1
    # Is it the lowest OU total of the week?
    if over_under_total < lowest_week_OU_total:
        lowest_week_OU_total = over_under_total
        lowest_week_total_score = store_total_score
        # Incase there are multiple weeks with the same total that need to be looked at for the betting strategy
        multiple_lowest_OU = 0
    elif over_under_total == lowest_week_OU_total:
        multiple_lowest_OU += 1

    # Store previous for comparisons
    previous_season_year = current_season_year
    previous_game_week = current_game_week

# Run this to get the final week and 2022 season results stored in the list since the "else" isn't triggered in either if else statements for week and year
# If there is only one total to check
if multiple_highest_OU < 1:
    highest_week_OU_result = game_over_under(highest_week_total_score, highest_week_OU_total)
    # Use the highest result for later calculations
    if highest_week_OU_result == "Over":
        highest_week_OU_overs += 1
        high_game_counter += 1
    elif highest_week_OU_result == "Under":
        high_game_counter += 1
        pass
    # Remove one from the week counter because a push shouldn't affect the percentage calculated at the end of the season
    elif highest_week_OU_result == "Push":
        pass
else:
    # Check every highest game and compare the results
    highest_games = db.execute("SELECT home_score, away_score, over_under_total FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND over_under_total = ?",
                                previous_season_year, previous_game_week, highest_week_OU_total)
    # Loop through and see what the result of each is
    for highest_game in highest_games:
        home_score = highest_game["home_score"]
        away_score = highest_game["away_score"]
        temp_high_OU_total = highest_game["over_under_total"]
        temp_total_score = total_score(home_score, away_score)
        temp_OU_result = game_over_under(temp_total_score, temp_high_OU_total)
        if temp_OU_result == "Over":
            highest_games_overs += 1
        elif temp_OU_result == "Under":
            highest_games_unders += 1
        else:
            pass
    # Lost the juice of the bets since they went even and amount of juice * the number of bets that washed / 2 so just use one of the variables
    if highest_games_overs == highest_games_unders:
        juice_lost += (1 * (highest_games_overs + highest_games_unders))
        pass
    # Add more weight to the percentage since it would be multiple wins
    elif highest_games_overs > highest_games_unders:
        highest_week_OU_overs += (1 * (highest_games_overs - highest_games_unders))
        high_game_counter += (1 * (highest_games_overs - highest_games_unders))
    # Take away more weight from the overs IF it's a difference of more than one, since the week_counter will already account one as a loss
    elif highest_games_overs < highest_games_unders:
        high_game_counter += (1 * (highest_games_unders - highest_games_overs))

# If there is only one total to check
if multiple_lowest_OU < 1:
    lowest_week_OU_result = game_over_under(lowest_week_total_score, lowest_week_OU_total)
    # Now do the lowest result
    if lowest_week_OU_result == "Under":
        lowest_week_OU_unders += 1
        low_game_counter += 1
    elif lowest_week_OU_result == "Over":
        low_game_counter += 1
        pass
    # Remove one from the week counter because a push shouldn't affect the percentage calculated at the end of the season
    elif lowest_week_OU_result == "Push":
        pass
else:
    # Check every highest game and compare the results
    lowest_games = db.execute("SELECT home_score, away_score, over_under_total FROM NFL_reg_season_spreads WHERE season_year = ? AND week_number = ? AND over_under_total = ?",
                                previous_season_year, previous_game_week, lowest_week_OU_total)
    # Loop through and see what the result of each is
    for lowest_game in lowest_games:
        home_score = lowest_game["home_score"]
        away_score = lowest_game["away_score"]
        temp_low_OU_total = lowest_game["over_under_total"]
        temp_total_score = total_score(home_score, away_score)
        temp_OU_result = game_over_under(temp_total_score, temp_low_OU_total)
        if temp_OU_result == "Over":
            lowest_games_overs += 1
        elif temp_OU_result == "Under":
            lowest_games_unders += 1
        else:
            pass
    # Lost the juice of the bets since they went even and amount of juice * the number of bets that washed / 2 so just use one of the variables
    if lowest_games_overs == lowest_games_unders:
        juice_lost += (1 * (lowest_games_overs + lowest_games_unders))
        pass
    # Add more weight to the percentage since it would be multiple wins
    elif lowest_games_overs < lowest_games_unders:
        lowest_week_OU_overs += (1 * (lowest_games_unders - lowest_games_overs))
        low_game_counter += (1 * (lowest_games_unders - lowest_games_overs))
    # Take away more weight from the overs IF it's a difference of more than one, since the week_counter will already account one as a loss
    elif lowest_games_overs > lowest_games_unders:
        low_game_counter += (1 * (lowest_games_overs - lowest_games_unders))

percent_over_highest_total = 100 * round(highest_week_OU_overs / high_game_counter, 3)
percent_over_highest_totals.append(percent_over_highest_total)
percent_under_lowest_total = 100 * round(lowest_week_OU_unders / low_game_counter, 3)
percent_under_lowest_totals.append(percent_under_lowest_total)
total_juice_lost.append(juice_lost)

# Calculate the regression line for each
coefficients_highs = np.polyfit(season_years, percent_over_highest_totals, 1)
m_s = coefficients_highs[0]  # slope
b_s = coefficients_highs[1]  # y-intercept
regression_line_highs = np.polyval(coefficients_highs, season_years)

coefficients_lows = np.polyfit(season_years, percent_under_lowest_totals, 1)
m_OU = coefficients_lows[0]  # slope
b_OU = coefficients_lows[1]  # y-intercept
regression_line_lows = np.polyval(coefficients_lows, season_years)

# Chart both percentages of highest overs and lowest unders for each season
plt.scatter(season_years, percent_over_highest_totals, color = 'red', label = '% Over Highes Totals')
plt.plot(season_years, regression_line_highs, color = 'red', label = 'Regression Line Highs')
plt.scatter(season_years, percent_under_lowest_totals, color = 'blue', label = '% Under Lowest Totals')
plt.plot(season_years, regression_line_lows, color = 'blue', label = 'Regression Line Lows')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Overs or Unders')
plt.title('Do the Highest Overs Go Over and Lowest Unders Go Under?')
plt.legend()
plt.show()

# Chart the juice lost each season on pushes
plt.bar(season_years, total_juice_lost, color = 'green', label = "Juice Lost")
plt.xlabel('NFL Season')
plt.ylabel('Amount of Juice was Lost')
plt.title('How Much Juice Was Lost On Washes')
plt.legend()
plt.show()