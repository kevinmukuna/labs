import pymysql

endpoint = "database-1.cxfenebqj5jy.eu-west-1.rds.amazonaws.com"
username = "admin"
password = "Mk369147"
database_name = "weather"

connection = pymysql.connect(endpoint, user=username, passwd=password, db=database_name)


def handler():
    cursor = connection.cursor()
    cursor.execute("SELECT * from Weather")
    rows = cursor.fetchall()

    for row in rows:
        print("{0} {1} {2}".format(row[0], row[1], row[2]))

handler()
