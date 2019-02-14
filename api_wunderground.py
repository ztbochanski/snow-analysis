# Zachary Bochanski
# 2017/10/31
# BACKCOUNTRY SNOW REPORT

# out of class early? where's the best place to ski..?

# Program uses the Weather Underground API(application programming interface)
# (this project uses json data format)
# in order to gather real time data from personal weather stations. Wunderground
# is available in most countries around the world and updates are collected every
# 15 minutes.

# Weather Underground API KEY: fe28925cdd8b3578

# This program is intended to be used as a featherwieght tool in order to gain a
# baseline for weather conditions before heading out on an adventure with snow involved
# (skiing, biking, hiking).

# program also analyzes historical weather data in order for the user
# to make a prediction on the optimal time to recreate safley and stay off dangerous snow conditions.
# The historical trend may also
# be used to observe change in climate conditions

# history:
# http://api.wunderground.com/api/SECURITYKEY/history_20060405/q/VT/Underhill.json

# url import to access weather information using wunderground API
# to get data use following address
# http://api.wunderground.com/api/fe28925cdd8b3578/your_request/q/VT/Underhill.json

# autoip to give data nearest you

# using requests instead of urllib because it includes functinos to format json
import requests
# date and time used for gathering historical weather data
import datetime


def main():

    print('\n--------------------------------------------------------------------')
    print('***This program takes the current and past weather data from remote personal' +
          '\nand commercial weather stations in order to deliver a weather report for' +
          '\nlocation specific Backcountry Snow Conditions***')
    print('--------------------------------------------------------------------')

    # initialize loop to ask for state location
    state = 'initialize'
    while state != '':
        state = input('\nEnter US State(hit enter to exit): ')

        state = state.upper()

        us_states = {'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
                     'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
                     'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
                     'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE',
                     'nevada': 'NV', 'new hampshire': 'NH', 'new jersey': 'NJ', 'new Mexico': 'NM', 'new York': 'NY', 'north carolina': 'NC', 'north dakota': 'ND',
                     'Ohio': 'OH', 'oklahoma': 'OK', 'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC', 'south dakota': 'SD',
                     'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 'wisconsin': 'WI',
                     'wyoming': 'WY', }

        # deal with user entries not using state code
        if len(state) > 2:
            try:
                state = state.lower()
                state = us_states[state]
                if state in us_states:
                    print('Check the location you entered: ', '\'', state, '\'', sep='')
                    continue
            except KeyError:
                print('Check the location you Entered: ', '\'', state, '\'', sep='')
                continue

        # deal with incorrect state codes
        elif len(state) <= 2 and state != '':
            try:
                state = state.upper()
                if state not in us_states.values():
                    print('Check the location you entered: ', '\'', state, '\'', sep='')
                    continue

            except KeyError:
                print('Check the location you entered: ', '\'', state, '\'', sep='')
                continue

        elif state == '':
            print('\nThank you for exploring the BACKCOUNTRY SNOW REPORT, recreate safely\n')
            break
        print('The location you entered: ', state)

        city = 'initialize'
        while city != '':
            try:
                city = input('Enter US City(hit enter to exit): ')
                if city == '':
                    print('\nThank you for exploring the BACKCOUNTRY SNOW REPORT, recreate safely\n')
                    exit()

                else:
                    city = city.lower()
                    city = city[0].upper() + city[1:].lower()
                    test_city = requests.get(
                        'http://api.wunderground.com/api/fe28925cdd8b3578/geolookup/q/' + state + '/' + city + '.json')
                    lookup = test_city.json()
                    lookup = lookup['location']
                    break

            except KeyError:
                print('\nCould not find a weather station in ', state,
                      ' near this location: \'', city, '\'', sep='')
                continue

        print('The weather station you entered: ', city)
        print('Searching for weather information in ', city, ', ', state, '...', sep='')

        # header: display if weather alert, station info and season snow total
        weather_alert(state, city)
        current_conditions(state, city)
        history(state, city)

        # display option menu
        snow_list = ['snow', 's', 'snowpack', 'snow conditions', 'pack']
        forecast_list = ['f', 'forecast', 'overview']
        hourly_list = ['h', 'hourly', 'hour']
        location_list = ['n', 'close', 'near', 'by']
        new_list = ['l', 'new', 'different']
        module = 'initialize'
        while module != '':
            display_menu()
            module = input('\n\tEnter your menu choice: ')
            module = module.lower()
            print()
            if module in snow_list:
                snowpack(state, city)
            elif module in forecast_list:
                forecast_4day(state, city)
            elif module in hourly_list:
                hourly_forecast(state, city)
            elif module in location_list:
                nearby_locations(state, city)
            elif module in new_list:
                state = 'new location'
                break
        if module == '':
            print('\nThank you for exploring the BACKCOUNTRY SNOW REPORT, recreate safely\n')
            break
        else:
            continue


def display_menu():
    print(
        '\n\t\'s\' for Snowpack'
        '\n\t\'f\' for Forecast'
        '\n\t\'h\' for Hourly'
        '\n\t\'n\' for Nearby Stations'
        '\n\t\'l\' for New Location'
        '\n\n\t**hit enter to quit**')


def nearby_locations(st, cty):
    print('----------------------------------------------------------------------------')
    print(' \'City\'\t\t\t Station\t\t\t\t  Km    Mi')
    next_city = requests.get(
        'http://api.wunderground.com/api/fe28925cdd8b3578/geolookup/q/' + st + '/' + cty + '.json')
    near_station = next_city.json()
    print
    for loc in near_station['location']['nearby_weather_stations']['pws']['station']:
        print('|', '{0:20} | {1:40}|{2:3}km|{3:3}mi'.format(
            loc['city'], loc['neighborhood'], loc['distance_km'], loc['distance_mi']))
    print('----------------------------------------------------------------------------')
    print('Use a nearby \'City\' in a \'New Location\' search')
    print('----------------------------------------------------------------------------')


def weather_alert(st, cty):
    print('--------------------------------------------------------------------')
    print('Weather Alerts: ')
    weather_alert = requests.get(
        'http://api.wunderground.com/api/fe28925cdd8b3578/alerts/q/' + st + '/' + cty + '.json')
    alert = weather_alert.json()
    alert = alert['alerts']

    if alert == []:
        print('**currently no weather alerts in your area**')
    else:
        for i in alert:
            print(i['message'])


def current_conditions(st, cty):

    # current conditions url
    forecast_conditions = requests.get(
        'http://api.wunderground.com/api/fe28925cdd8b3578/conditions/q/' + st + '/' + cty + '.json')
    data_conditions = forecast_conditions.json()

    # Station/location header information
    print('--------------------------------------------------------------------')
    print('Station ID: ', data_conditions['current_observation']['station_id'])
    print('--------------------------------------------------------------------')
    print('Location: ', data_conditions['current_observation']['observation_location']['full'])
    print('\t  ' + ' - - ' * 10)
    print('           *', data_conditions['current_observation']['observation_time'], '*')
    print('--------------------------------------------------------------------')

    # Current Weather Conditions
    print('\nCurrent Conditions: ', data_conditions['current_observation']['weather'])
    print('Temperature:', data_conditions['current_observation']['temperature_string'])
    print('Feels Like:', data_conditions['current_observation']['feelslike_string'])
    print('Wind Speed:', data_conditions['current_observation']['wind_mph'], 'mph',
          '|| Direction:', data_conditions['current_observation']['wind_dir'])
    print('Precipitation Today:', data_conditions['current_observation']['precip_today_string'])
    print('\n--------------------------------------------------------------------')


def history(st, cty):

    historical_data = requests.get(
        'http://api.wunderground.com/api/fe28925cdd8b3578/history_20171120/q/' + st + '/' + cty + '.json')
    history = historical_data.json()
    # print(historical_data.text)
    print('--------------------------------------------------------------------')
    for i in history['history']['dailysummary']:
        if i['since1julsnowfalli'] == '':
            print('Snow! Season running total (in): \n**No history: This station does not record snow depth**')
        else:
            print('Snow! Season running total (in):', i['since1julsnowfalli'], 'in')
            print('Current Depth (in):', i['snowdepthi'], 'in')
    print('--------------------------------------------------------------------')


def snowpack(st, cty):

    # determine snowpack using historical weather data
    cur_date = datetime.datetime.now().strftime('%Y%m%d')
    cur_date_int = int(cur_date)
    start_date = cur_date_int - 4

    # loop through history 4 days back from current date and store in dict
    # key = date, value = data
    min_dew_point = {}
    max_dew_point = {}
    min_temp = {}
    max_temp = {}
    snow_fall = {}
    snow_depth = {}

    count = 0
    for i in range(4):
        start_date = str(start_date)
        address = 'http://api.wunderground.com/api/fe28925cdd8b3578/history_' + \
            start_date + '/q/' + st + '/' + cty + '.json'
        historical_data = requests.get(address)
        history = historical_data.json()
        start_date = int(start_date)
        # loop through dict from wunder and retrieve data: store in dict
        for i in history['history']['dailysummary']:
            min_dew_point[count] = i['mindewpti']
            max_dew_point[count] = i['maxdewpti']
            min_temp[count] = i['mintempi']
            max_temp[count] = i['maxtempi']
            snow_fall[count] = i['snow']
            snow_depth[count] = i['snowdepthi']
        start_date += 1
        count += 1

    if snow_depth[0] == '':
        print('**Cannot analyze snowpack: this station does not record snow depth**')
    else:
        # Uses temperature change from prior 4 days to estimate snowpack conditions
        # count for days of min_temp above 45 degrees
        temp_count = 0
        for num in min_temp.values():
            num = int(num)
            if num > 40:
                temp_count += 1
        # highs
        high_temp_count = 0
        for num in max_temp.values():
            num = int(num)
            if num > 40:
                high_temp_count += 1
        # count number of days there is snow fall over 2"
        # if count > 0 than there was a day with more than 2"
        snow_count = 0
        for num in snow_fall.values():
            num = float(num)
            if num > 2:
                if num > 8:
                    snow_count += 10
                snow_count += 1

        # previous day of highs/lows
        temp_high = max_temp[3]
        temp_high = int(temp_high)
        temp_low = min_temp[3]
        temp_low = float(temp_low)

        snow_depth_int = snow_depth[3]
        snow_depth_int = float(snow_depth_int)

        print('--------------------------------------------------------------------')
        print('Current Snowpack Conditions:')
        # first check if there is snow
        if snow_depth_int > 1:
            # morning crust = 2 days or more above min above 45, and 4th day ONLY MIN below 32
            if snow_count > 10:
                print('Pow Dump')
            # temp_low and temp_high are LAST day only
            elif temp_low < 32 and temp_high > 32 and temp_count >= 2:
                print('Morning Crust, afternoon corn')
            # crust all day = 2 day or more above min above 45 and 4th day MIN and MAX below 32
            elif temp_high < 32 and temp_count >= 2:
                print('Crust all day')
            # corn snow = temp min and max ABOVE 32
            elif temp_low > 32 and temp_high > 32 and temp_count >= 1:
                print('Corn Snow')
            # transformed snow if tem max above 32 and 1 days above 32
            elif temp_low < 32 and temp_high < 32 and temp_count >= 1 or high_temp_count >= 1:
                print('Transformed Snow')
            # old powder if no new snow or only dustings
            elif temp_low <= 32 and temp_high <= 32 and snow_count == 0 and temp_count == 0:
                print('Old Powder, or dusting under 2in')
            # new snow within last 3 days:
            elif temp_low <= 32 and temp_high <= 32 and snow_count >= 1 and temp_count == 0:
                print('Fresh Powder')
        else:
            print('**not enough snow to ski!! Cross your fingers!!**')
        print('--------------------------------------------------------------------')

        # Hoarfrost is an indicator of snowpack stability in avalach terrain:
        # it forms when water vapor freezes directly onto surfaces
        # the temperature of the surface must fall below the frost / dew point
        # and the frost point must be below freezing
        min_frost = min_dew_point[3]
        max_frost = max_dew_point[3]
        min_frost = int(min_frost)
        max_frost = int(max_frost)

        if temp_low < 32 and temp_low <= min_frost:
            if min_frost < 32:
                print(
                    '** Warning ** there was a hoarfrost yesterday make note before recreating in avalanch terrain')


def hourly_forecast(st, cty):

    # hourly forcast, temp, percip, etc
    forecast_hourly = requests.get(
        'http://api.wunderground.com/api/fe28925cdd8b3578/hourly/q/' + st + '/' + cty + '.json')
    data_hourly = forecast_hourly.json()

    print('\nTIME' + '\tTemperature (F)' + '\tSnow (in)')
    print('--------------------------------------------')
    for hour in data_hourly['hourly_forecast']:
        print(hour['FCTTIME']['hour_padded'] + ':' + hour['FCTTIME']
              ['min'] + '\t' + hour['temp']['english'] + 'F' + '\t\t' +
              hour['snow']['english'] + 'in')


def forecast_4day(st, cty):

    forecast_day = requests.get(
        'http://api.wunderground.com/api/fe28925cdd8b3578/forecast/q/' + st + '/' + cty + '.json')
    data_4day = forecast_day.json()

    # 4 Day forecast from 'forecast' in api
    print('--------------------------------------------------------------------')
    print('4 day general forcast:')
    for day in data_4day['forecast']['simpleforecast']['forecastday']:
        print('\n' + day['date']['pretty'])
        print('Conditions: ', day['conditions'])
        print("High: ", day['high']['fahrenheit'] + "F",
              "Low: ", day['low']['fahrenheit'] + "F", '')
        print('--------------------------------------------------------------------')

    print('--------------------------------------------------------------------')


main()

# data_dict['Min_Dew_Point'] = i['mindewpti']
# data_dict['Max_Dew_Point'] = i['maxdewpti']
# data_dict['Min_Temp'] = i['mintempi']
# data_dict['Max_Temp'] = i['maxtempi']
