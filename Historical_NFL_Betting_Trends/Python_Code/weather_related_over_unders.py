import numpy as np
import matplotlib.pyplot as plt
from cs50 import SQL
from critical_functions import total_score, game_over_under

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:////workspaces/126349338/Final_Project/NFL.db")

# Has scoring gone up in the NFL per game over the years?
# Get the needed data from each game through the regular season
games = db.execute("SELECT home_score, away_score, over_under_total, season_year, weather_detail, temperature, wind_mph, humidity FROM NFL_reg_season_spreads")
years = db.execute("SELECT DISTINCT season_year FROM NFL_reg_season_spreads")

# Make a list to fill with each distinct year from the years db
season_years = []
for year in years:
    season_year = year["season_year"]
    season_years.append(season_year)

# Make a list to fill with the percentage of unders with weather effects and overs in indoor stadiums
percent_U_H_wind_games = []
percent_U_VH_wind_games = []
percent_U_H_humid_games = []
percent_U_VH_humid_games = []
percent_U_L_temp_games = []
percent_U_VL_temp_games = []
percent_U_H_temp_games = []
percent_U_VH_temp_games = []
percent_U_H_temp_and_humid = []
percent_O_indoor_games = []
percent_O_perfect_weather_games = []
# Starting in 2009 these come into play in the data
percent_U_rain_games = []
percent_U_snow_games = []
# Initialize weather type game varaibles
H_wind_games = 0
H_wind_unders = 0
VH_wind_games = 0
VH_wind_unders = 0
H_humid_games = 0
H_humid_unders = 0
VH_humid_games = 0
VH_humid_unders = 0
L_temp_games = 0
L_temp_unders = 0
VL_temp_games = 0
VL_temp_unders = 0
H_temp_games = 0
H_temp_unders = 0
VH_temp_games = 0
VH_temp_unders = 0
H_temp_and_humid_games = 0
H_temp_and_humid_unders = 0
indoor_games = 0
indoor_overs = 0
perfect_weather_overs = 0
perfect_weather_games = 0
rain_games = 0
rain_unders = 0
snow_games = 0
snow_unders = 0
# Initialize previous season variable
previous_season_year = 0

# Loop through games, determine if the weather and if they went over or under
for game in games:
    # Initialize current_season variable
    current_season_year = game["season_year"]
    # Check if the season ended
    if previous_season_year == 0 or current_season_year == previous_season_year:
        pass
    else:
        percent_O_indoor = 100 * round(indoor_overs / indoor_games, 3)
        percent_O_indoor_games.append(percent_O_indoor)
        # Temp and wind data stops after 2018 season
        if previous_season_year < 2019:
            # Calculate percentages and store them in the proper lists
            percent_U_H_wind = 100 * round(H_wind_unders / H_wind_games, 3)
            percent_U_H_wind_games.append(percent_U_H_wind)
            if VH_wind_games == 0:
                percent_U_VH_wind_games.append(previous_season_year)
            else:
                percent_U_VH_wind = 100 * round(VH_wind_unders / VH_wind_games, 3)
                percent_U_VH_wind_games.append(percent_U_VH_wind)
            percent_U_H_temp = 100 * round(H_temp_unders / H_temp_games, 3)
            percent_U_H_temp_games.append(percent_U_H_temp)
            if VH_temp_games == 0:
                percent_U_VH_temp_games.append(previous_season_year)
            else:
                percent_U_VH_temp = 100 * round(VH_temp_unders / VH_temp_games, 3)
                percent_U_VH_temp_games.append(percent_U_VH_temp)
            percent_U_L_temp = 100 * round(L_temp_unders / L_temp_games, 3)
            percent_U_L_temp_games.append(percent_U_L_temp)
            if VL_temp_games == 0:
                percent_U_VL_temp_games.append(previous_season_year)
            else:
                percent_U_VL_temp = 100 * round(VL_temp_unders / VL_temp_games, 3)
                percent_U_VL_temp_games.append(percent_U_VL_temp)
        # Data for humidity stops after 2013 season
        if previous_season_year < 2014:
            percent_U_H_humid = 100 * round(H_humid_unders / H_humid_games, 3)
            percent_U_H_humid_games.append(percent_U_H_humid)
            percent_U_VH_humid = 100 * round(VH_humid_unders / VH_humid_games, 3)
            percent_U_VH_humid_games.append(percent_U_VH_humid)
            percent_U_H_temp_humid = 100 * round(H_temp_and_humid_unders / H_temp_and_humid_games, 3)
            percent_U_H_temp_and_humid.append(percent_U_H_temp_humid)
            percent_O_perfect_weather = 100 * round(perfect_weather_overs / perfect_weather_games, 3)
            percent_O_perfect_weather_games.append(percent_O_perfect_weather)
        # If current_season_year 2009 or later (will be 2010 to trigger the else for the 2009 season)
        if current_season_year > 2009:
            if previous_season_year < 2019:
                percent_U_rain = 100 * round(rain_unders / rain_games, 3)
                percent_U_rain_games.append(percent_U_rain)
            if previous_season_year < 2018:
                percent_U_snow = 100 * round(snow_unders / snow_games, 3)
                percent_U_snow_games.append(percent_U_snow)

        # Reset season game and under counters
        H_wind_games = 0
        H_wind_unders = 0
        VH_wind_games = 0
        VH_wind_unders = 0
        H_humid_games = 0
        H_humid_unders = 0
        VH_humid_games = 0
        VH_humid_unders = 0
        L_temp_games = 0
        L_temp_unders = 0
        VL_temp_games = 0
        VL_temp_unders = 0
        H_temp_games = 0
        H_temp_unders = 0
        VH_temp_games = 0
        VH_temp_unders = 0
        H_temp_and_humid_games = 0
        H_temp_and_humid_unders = 0
        indoor_games = 0
        indoor_overs = 0
        perfect_weather_overs = 0
        perfect_weather_games = 0
        rain_games = 0
        rain_unders = 0
        snow_games = 0
        snow_unders = 0

    # Initialize the needed variables
    home_score = game["home_score"]
    away_score = game["away_score"]
    over_under_total = game["over_under_total"]
    # Calculate total and OU result
    game_total_score = total_score(home_score, away_score)
    over_under_result = game_over_under(game_total_score, over_under_total)
    # Initialize weather variables needed
    temperature = game["temperature"]
    wind_mph = game["wind_mph"]
    humidity = game["humidity"]
    weather_detail = game["weather_detail"]

    # Classify the games with the weather varaibles, store the results, and add to that game type
    # Temp and wind data stops after 2018 season
    if current_season_year < 2019:
        if wind_mph > 14:
            if over_under_result == "Under":
                H_wind_unders += 1
                H_wind_games += 1
            elif over_under_result == "Over":
                H_wind_games += 1
            else:
                pass
        if wind_mph > 24:
            if over_under_result == "Under":
                VH_wind_unders += 1
                VH_wind_games += 1
            elif over_under_result == "Over":
                VH_wind_games += 1
            else:
                pass
        if temperature > 74:
            if over_under_result == "Under":
                H_temp_unders += 1
                H_temp_games += 1
            elif over_under_result == "Over":
                H_temp_games += 1
            else:
                pass
        if temperature > 89:
            if over_under_result == "Under":
                VH_temp_unders += 1
                VH_temp_games += 1
            elif over_under_result == "Over":
                VH_temp_games += 1
            else:
                pass
        if temperature < 36:
            if over_under_result == "Under":
                L_temp_unders += 1
                L_temp_games += 1
            elif over_under_result == "Over":
                L_temp_games += 1
            else:
                pass
        if temperature < 21:
            if over_under_result == "Under":
                VL_temp_unders += 1
                VL_temp_games += 1
            elif over_under_result == "Over":
                VL_temp_games += 1
            else:
                pass
    if weather_detail == "indoor" or weather_detail == "retractable (closed roof)":
        if over_under_result == "Over":
            indoor_overs += 1
            indoor_games += 1
        elif over_under_result == "Under":
            indoor_games += 1
        else:
            pass
    # Data for humidity stops after 2013 season
    if current_season_year < 2014:
        if humidity > 59:
            if over_under_result == "Under":
                H_humid_unders += 1
                H_humid_games += 1
            elif over_under_result == "Over":
                H_humid_games += 1
            else:
                pass
        if humidity > 79:
            if over_under_result == "Under":
                VH_humid_unders += 1
                VH_humid_games += 1
            elif over_under_result == "Over":
                VH_humid_games += 1
            else:
                pass
        if temperature > 44 and temperature < 75 and humidity < 60 and wind_mph < 15 and (weather_detail == "" or weather_detail == "retractable (open roof)"):
            if over_under_result == "Over":
                perfect_weather_overs += 1
                perfect_weather_games += 1
            elif over_under_result == "Under":
                perfect_weather_games += 1
            else:
                pass
        if humidity > 59 and temperature > 74:
            if over_under_result == "Under":
                H_temp_and_humid_unders += 1
                H_temp_and_humid_games += 1
            elif over_under_result == "Over":
                H_temp_and_humid_games += 1
            else:
                pass
    # Rain and Snow games were kept track of starting in 2009 season
    if current_season_year > 2008:
        if current_season_year < 2018:
            if weather_detail == "snow" or weather_detail == "snow | fog":
                if over_under_result == "Under":
                    snow_unders += 1
                    snow_games += 1
                elif over_under_result == "Over":
                    snow_games += 1
                else:
                    pass
        if current_season_year < 2019:
            if weather_detail == "rain" or weather_detail == "rain | fog":
                if over_under_result == "Under":
                    rain_unders += 1
                    rain_games += 1
                elif over_under_result == "Over":
                    rain_games += 1
                else:
                    pass

    # Set previous_season_year for comparison
    previous_season_year = current_season_year

# Run this because it's the only thing that has data kept track through every season year we have data on
percent_O_indoor = 100 * round(indoor_overs / indoor_games, 3)
percent_O_indoor_games.append(percent_O_indoor)

# Remove any years that were stored in the list because there wasn't a value that season that fit the parameters
# Initialize empty lists to append the years that don't have any data so those years can be removed from the x-axis when charting data
remove_VH_wind_game_years = []
remove_VH_temp_game_years = []
remove_VL_temp_game_years = []
# Loop through the years to remove the years from the data where tere wasn't any and store that year so it can be removed from a special years list to be used for that data's x-axis
for year in season_years:
    if year in percent_U_VH_wind_games:
        percent_U_VH_wind_games.remove(year)
        remove_VH_wind_game_years.append(year)
    if year in percent_U_VH_temp_games:
        percent_U_VH_temp_games.remove(year)
        remove_VH_temp_game_years.append(year)
    if year in percent_U_VL_temp_games:
        percent_U_VL_temp_games.remove(year)
        remove_VL_temp_game_years.append(year)

# Make the custom years for the affected lists
H_wind_game_years = list(range(1979, 2019))
H_temp_game_years = list(range(1979, 2019))
L_temp_game_years = list(range(1979, 2019))
H_humid_game_years = list(range(1979, 2014))
VH_humid_game_years = list(range(1979, 2014))
perfect_weather_game_years = list(range(1979, 2014))
H_temp_and_humid_game_years = list(range(1979, 2014))
rain_game_years = list(range(2009, 2019))
snow_game_years = list(range(2009, 2018))
# Initialzie the lists that will be used for those charts
VH_wind_game_years = list(range(1979, 2019))
VH_temp_game_years = list(range(1979, 2019))
VL_temp_game_years = list(range(1979, 2019))
# Fill the lists for those charts
for year in remove_VH_wind_game_years:
    VH_wind_game_years.remove(year)
for year in remove_VH_temp_game_years:
    VH_temp_game_years.remove(year)
for year in remove_VL_temp_game_years:
    VL_temp_game_years.remove(year)

# Calculate the regression line for each
coefficients_H_wind = np.polyfit(H_wind_game_years, percent_U_H_wind_games, 1)
m_s = coefficients_H_wind[0]  # slope
b_s = coefficients_H_wind[1]  # y-intercept
regression_line_H_wind = np.polyval(coefficients_H_wind, H_wind_game_years)

coefficients_VH_wind = np.polyfit(VH_wind_game_years, percent_U_VH_wind_games, 1)
m_OU = coefficients_VH_wind[0]  # slope
b_OU = coefficients_VH_wind[1]  # y-intercept
regression_line_VH_wind = np.polyval(coefficients_VH_wind, VH_wind_game_years)

coefficients_H_humid = np.polyfit(H_humid_game_years, percent_U_H_humid_games, 1)
m_s = coefficients_H_humid[0]  # slope
b_s = coefficients_H_humid[1]  # y-intercept
regression_line_H_humid = np.polyval(coefficients_H_humid, H_humid_game_years)

coefficients_VH_humid = np.polyfit(VH_humid_game_years, percent_U_VH_humid_games, 1)
m_OU = coefficients_VH_humid[0]  # slope
b_OU = coefficients_VH_humid[1]  # y-intercept
regression_line_VH_humid = np.polyval(coefficients_VH_humid, VH_humid_game_years)

coefficients_H_temp = np.polyfit(H_temp_game_years, percent_U_H_temp_games, 1)
m_s = coefficients_H_temp[0]  # slope
b_s = coefficients_H_temp[1]  # y-intercept
regression_line_H_temp = np.polyval(coefficients_H_temp, H_temp_game_years)

coefficients_VH_temp = np.polyfit(VH_temp_game_years, percent_U_VH_temp_games, 1)
m_OU = coefficients_VH_temp[0]  # slope
b_OU = coefficients_VH_temp[1]  # y-intercept
regression_line_VH_temp = np.polyval(coefficients_VH_temp, VH_temp_game_years)

coefficients_L_temp = np.polyfit(L_temp_game_years, percent_U_L_temp_games, 1)
m_s = coefficients_L_temp[0]  # slope
b_s = coefficients_L_temp[1]  # y-intercept
regression_line_L_temp = np.polyval(coefficients_L_temp, L_temp_game_years)

coefficients_VL_temp = np.polyfit(VL_temp_game_years, percent_U_VL_temp_games, 1)
m_OU = coefficients_VL_temp[0]  # slope
b_OU = coefficients_VL_temp[1]  # y-intercept
regression_line_VL_temp = np.polyval(coefficients_VL_temp, VL_temp_game_years)

coefficients_H_temp_and_humid = np.polyfit(H_temp_and_humid_game_years, percent_U_H_temp_and_humid, 1)
m_s = coefficients_H_temp_and_humid[0]  # slope
b_s = coefficients_H_temp_and_humid[1]  # y-intercept
regression_line_H_temp_and_humid = np.polyval(coefficients_H_temp_and_humid, H_temp_and_humid_game_years)

coefficients_indoor = np.polyfit(season_years, percent_O_indoor_games, 1)
m_s = coefficients_indoor[0]  # slope
b_s = coefficients_indoor[1]  # y-intercept
regression_line_indoor = np.polyval(coefficients_indoor, season_years)

coefficients_perfect_weather = np.polyfit(perfect_weather_game_years, percent_O_perfect_weather_games, 1)
m_OU = coefficients_perfect_weather[0]  # slope
b_OU = coefficients_perfect_weather[1]  # y-intercept
regression_line_perfect_weather = np.polyval(coefficients_perfect_weather, perfect_weather_game_years)

coefficients_rain = np.polyfit(rain_game_years, percent_U_rain_games, 1)
m_s = coefficients_rain[0]  # slope
b_s = coefficients_rain[1]  # y-intercept
regression_line_rain = np.polyval(coefficients_rain, rain_game_years)

coefficients_snow = np.polyfit(snow_game_years, percent_U_snow_games, 1)
m_OU = coefficients_snow[0]  # slope
b_OU = coefficients_snow[1]  # y-intercept
regression_line_snow = np.polyval(coefficients_snow, snow_game_years)

# Chart both percentages of unders in high and very high wind games
plt.scatter(H_wind_game_years, percent_U_H_wind_games, color = 'red', label = 'Percent of Unders w/ Winds > 14 mph')
plt.plot(H_wind_game_years, regression_line_H_wind, color = 'red', label = 'Regression Line High Wind')
plt.scatter(VH_wind_game_years, percent_U_VH_wind_games, color = 'blue', label = 'Percent of Unders w/ Winds > 24 mph')
plt.plot(VH_wind_game_years, regression_line_VH_wind, color = 'blue', label = 'Regression Line Very High Wind')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders')
plt.title('Percent of Unders in Games w/ Windy Conditions')
plt.legend()
plt.show()

# Chart both percentages of unders in high and very high temp games
plt.scatter(H_temp_game_years, percent_U_H_temp_games, color = 'red', label = 'Percent of Unders w/ Temps > 74')
plt.plot(H_temp_game_years, regression_line_H_temp, color = 'red', label = 'Regression Line High Temps')
plt.scatter(VH_temp_game_years, percent_U_VH_temp_games, color = 'blue', label = 'Percent of Unders w/ Temps > 89')
plt.plot(VH_temp_game_years, regression_line_VH_temp, color = 'blue', label = 'Regression Line Very High Temps')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders')
plt.title('Percent of Unders in Games w/ Hot Conditions')
plt.legend()
plt.show()

# Chart both percentages of unders in high and very high humidity games
plt.scatter(H_humid_game_years, percent_U_H_humid_games, color = 'red', label = 'Percent of Unders w/ Humidity > 59')
plt.plot(H_humid_game_years, regression_line_H_humid, color = 'red', label = 'Regression Line High Humidity')
plt.scatter(VH_humid_game_years, percent_U_VH_humid_games, color = 'blue', label = 'Percent of Unders w/ Humidity > 79')
plt.plot(VH_humid_game_years, regression_line_VH_humid, color = 'blue', label = 'Regression Line Very High Humidity')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders')
plt.title('Percent of Unders in Games w/ Humid Conditions')
plt.legend()
plt.show()

# Chart both percentages of unders in high temp and humid games
plt.scatter(H_temp_and_humid_game_years, percent_U_H_temp_and_humid, color = 'red', label = 'Percent of Unders w/ High Temp/Humidity')
plt.plot(H_temp_and_humid_game_years, regression_line_H_temp_and_humid, color='red', label='Regression Line High Temp/Humidity')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders')
plt.title('Percent of Unders in Games w/ Hot and Humid Conditions')
plt.legend()
plt.show()

# Chart both percentages of unders in low temp games
plt.scatter(L_temp_game_years, percent_U_L_temp_games, color = 'red', label = 'Percent of Unders w/ Temp < 36')
plt.plot(L_temp_game_years, regression_line_L_temp, color = 'red', label = 'Regression Line Low Temp')
plt.scatter(VL_temp_game_years, percent_U_VL_temp_games, color = 'blue', label = 'Percent of Unders w/ Temp < 21')
plt.plot(VL_temp_game_years, regression_line_VL_temp, color = 'blue', label = 'Regression Line Very Low Temp')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders')
plt.title('Percent of Unders in Games w/ Cold Conditions')
plt.legend()
plt.show()

# Chart both percentages of overs in indoor games and ideal weather
plt.scatter(season_years, percent_O_indoor_games, color = 'purple', label = 'Percent of Overs Inside')
plt.plot(season_years, regression_line_indoor, color = 'purple', label = 'Regression Line Indoors')
plt.scatter(perfect_weather_game_years, percent_O_perfect_weather_games, color = 'green', label = 'Percent of Overs w/ Perfect Weather')
plt.plot(perfect_weather_game_years, regression_line_perfect_weather, color = 'green', label = 'Regression Line Perfect Weather')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Overs')
plt.title('Percent of Overs in Games Inside or w/ Ideal Weather')
plt.legend()
plt.show()

# Chart both percentages of unders in games with rain
plt.scatter(rain_game_years, percent_U_rain_games, color = 'purple', label = 'Percent of Unders w/ Rain')
plt.plot(rain_game_years, regression_line_rain, color = 'purple', label = 'Regression Line Rain')
plt.scatter(snow_game_years, percent_U_snow_games, color = 'blue', label = 'Percent of Unders w/ Snow')
plt.plot(snow_game_years, regression_line_snow, color = 'blue', label = 'Regression Line Snow')
plt.xlabel('NFL Season')
plt.ylabel('Percentage of Unders')
plt.title('Percent of Unders in Games w/ Precipitation')
plt.legend()
plt.show()