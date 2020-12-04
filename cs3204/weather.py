import urllib.request
import json
import mysql.connector
import pymysql
from datetime import date, datetime, timedelta

BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'

ApiKey = 'AIzaSyA38CVVRT0o30ILa8HrCiQN50Gfxc8tauY'

UnitGroup = 'us'

Locations = 'Washington,DC'

QueryType = 'FORECAST'

AggregateHours = '24'

StartDate = ''

EndDate = ''


if QueryType == 'FORECAST':
    print(' - Fetching forecast data')
    QueryParams = 'forecast?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&shortColumnNames=true'
else:
    print(' - Fetching history for date: ', DateParam)

    # History requests require a date.  We use the same date for start and end since we only want to query a single
    # date in this example
    QueryParams = 'history?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup +'&startDateTime=' + StartDate \
                  + 'T00%3A00%3A00&endDateTime=' + EndDate + 'T00%3A00%3A00'

Locations='&locations='+Locations

ApiKey='&key='+ApiKey

# Build the entire query
# URL = BaseURL + QueryParams + Locations + ApiKey+"&contentType=json"
URL = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json?fuel_type=E85," \
      "ELEC&state=CA&limit=2&api_key=Hb0SygVWOa3rp6LPU6o3J58mlDCtOcz6b8OiS1PA"
print(' - Running query URL: ', URL)
print()

response = urllib.request.urlopen(URL)
data = response.read()
print(data)
weatherData = json.loads(data.decode('utf-8'))

print("Connecting to mysql database")
# connect to the database. Enter your host, username and password
cnx = pymysql.connect(host='weather.cxfenebqj5jy.eu-west-1.rds.amazonaws.com',
                      user='admin',
                      passwd='Mk369147',
                      database='weather')

cursor = cnx.cursor()

# In this simple example, clear out the existing data in the table

# delete_weather_data=("TRUNCATE TABLE 'weather'.'weather_data'")
# cursor.execute(delete_weather_data)
cnx.commit()

insert_weather_data = ("INSERT INTO 'weather_data_schema'.'weather_data'"
                       "('address','latitude','longitude','datetime','maxt','mint','temp','precip','wspd','wdir',"
                       "'wgust','pressure') "
                       "VALUES (%(address)s, %(latitude)s, %(longitude)s, %(datetime)s, %(maxt)s,%(mint)s, %(temp)s, "
                       "%(precip)s, %(wspd)s, %(wdir)s, %(wgust)s, %(pressure)s)")

# Iterate through the locations
locations = weatherData["locations"]
for locationid in locations:
    location = locations[locationid]
    # Iterate through the values (values are the time periods in the weather data)
    for value in location["values"]:
        data_wx = {
            'address': location["address"],
            'latitude': location["latitude"],
            'longitude': location["longitude"],
            'datetime': datetime.utcfromtimestamp(value["datetime"] / 1000.),
            'maxt': value["maxt"] if 'maxt' in value else 0,
            'mint': value["mint"] if 'mint' in value else 0,
            'temp': value["temp"],
            'precip': value["precip"],
            'wspd': value["wspd"],
            'wdir': value["wdir"],
            'wgust': value["wgust"],
            'pressure': value["sealevelpressure"]
        }
        cursor.execute(insert_weather_data, data_wx)
        cnx.commit()

cursor.close()
cnx.close()
print("Database connection closed")

print("Done")