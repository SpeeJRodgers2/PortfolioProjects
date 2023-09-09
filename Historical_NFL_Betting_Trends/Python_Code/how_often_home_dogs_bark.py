import numpy as np
import matplotlib.pyplot as plt
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:////workspaces/126349338/Final_Project/NFL.db")

# How often do home underdogs cover the spread?
# Insert into a list the number of times that a home underdog has "Win" AS every season out of how many there are
# Get every season to look through in a for loop
years = db.execute("SELECT DISTINCT season_year FROM NFL_reg_season_spreads")

# Make the list to progressively store each count as the years increment
percent_win_home_dogs_list = []
season_years = []

# Loop through each season year getting the count of home underdogs and then the count of home underdogs that won
for year in years:
    season_year = year["season_year"]
    # Excluding 1978 season because there is only a single game from this season
    if season_year == 1978:
        continue
    else:
        season_years.append(season_year)

        num_home_underdogs = db.execute("SELECT COUNT(*) FROM NFL_reg_season_spreads WHERE season_year = ? AND fav_home_away = 'Away'",
                                        season_year)
        num_home_underdogs = num_home_underdogs[0]["COUNT(*)"]

        num_win_home_underdogs = db.execute("SELECT COUNT(*) FROM NFL_reg_season_spreads WHERE season_year = ? AND fav_home_away = 'Away' AND home_AS = 'Win'",
                                            season_year)
        num_win_home_underdogs = num_win_home_underdogs[0]["COUNT(*)"]

        percent_win_home_dogs = 100 * round((num_win_home_underdogs / num_home_underdogs), 3)
        percent_win_home_dogs_list.append(percent_win_home_dogs)

# Calculate the regression line
coefficients = np.polyfit(season_years, percent_win_home_dogs_list, 1)
m = coefficients[0]  # slope
b = coefficients[1]  # y-intercept
regression_line = np.polyval(coefficients, season_years)

# Chart the results using matplotlib.pyplot
plt.scatter(season_years, percent_win_home_dogs_list, color = 'red', label = 'Percent of Home-Dog Wins')
plt.plot(season_years, regression_line, color = 'red', label = 'Regression Line')
plt.xlabel('NFL Season')
plt.ylabel('Percent Home-Dogs Cover the Spread') # of Home-Dog Wins
plt.title('How Often Home-Dogs Bark Per Season')
plt.legend()
plt.show()