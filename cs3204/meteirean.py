import json
import json.decoder
import mysql.connector
import pymysql

cnx = mysql.connector.connect(host='weather.cxfenebqj5jy.eu-west-1.rds.amazonaws.com',
                              user='admin',
                              passwd='Mk369147',
                              database='weather'
                              )
cursor = cnx.cursor()
with open('MetEirean.json', 'r', encoding='utf-8', errors='ignore') as json_file:
    stations = json.load(json_file)

station_id = 1
total_rainfall_id = 1
mean_temperature_id = 1
soil_temperature_id = 1
solar_radiation_id = 1
potential_eva_id = 1
evaporation_id = 1
degree_id = 1
stationList = []


for data in stations:
    for station in stations[data]:
        sql = "INSERT INTO weather.mean_temperature (mean_temperature.station_id, stationName, up_to, total_rainfall, \
              mean_temperature_id,soil_temperature_id,solar_radiation_id,potential_eva_id, \
              evaporation_id, degree_id)  VALUES (%s , %s, %s , %s,%s , %s, %s , %s,%s , %s)"

        val = (
                station_id,
                station["station"],
                station["up_to"],
                total_rainfall_id,
                mean_temperature_id,
                soil_temperature_id,
                solar_radiation_id,
                potential_eva_id,
                evaporation_id,
                degree_id
        )

        cursor.execute(sql, val)
        cnx.commit()
        for each_entry in station:
            if each_entry == "station" or each_entry == "up_to":
                pass
            else:
                for eachValue in station[each_entry]:
                    for report in station[each_entry]["report"]:
                        year = station[each_entry]["report"][report]
                        #     print(year[month])
                        #     print(month)
                        #     print(report)
                        print(station["station"],each_entry,report,year)
                        print()
                        if report != "mean":
                            sql = "INSERT INTO weather.report (" "reportId, " "typeId, " "year_, " "january, february, " \
                                  "mar,apr,may,june," "july,august,september,october,november," \
                                  "december)  VALUES (%s , %s, %s , %s,%s , %s, %s ,%s,%s , %s,%s,%s , %s,%s,%s)"

                            val = (
                                station_id,
                                each_entry,
                                report,
                                year["january"],year["february"],
                                year["mar"],year["apr"],year["may"],year["june"],
                                year["july"],year["august"],year["september"],year["october"],
                                year["november"],year["december"]

                            )

                            cursor.execute(sql, val)
                            cnx.commit()
        station_id += 1
        total_rainfall_id += 1
        mean_temperature_id += 1
        soil_temperature_id += 1
        solar_radiation_id += 1
        potential_eva_id += 1
        evaporation_id += 1
        degree_id += 1
