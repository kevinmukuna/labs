import json
import json.decoder
import mysql.connector
import pymysql
from socket import *
cnx = mysql.connector.connect(host='weather.cxfenebqj5jy.eu-west-1.rds.amazonaws.com',
                              user='admin',
                              passwd='Mk369147',
                              database='weather'
                              )
cursor = cnx.cursor()


s = socket()
s.bind(('', 80)) # <-- Since the GET request will be sent to port 80 most likely
s.listen(4)
ns, na = s.accept()

while 1:
    try:
        data = ns.recv(8192) # <-- Get the browser data
    except:
        ns.close()
        s.close()
        break

    ## ---------- NOTE ------------ ##
    ## "data" by default contains a bunch of HTTP headers
    ## You need to get rid of those and parse the HTML data,
    ## the best way is to either just "print data" and see
    ## what it contains, or just try to find a HTTP parser lib (server side)

    data = json.loads(data)
    print(data)