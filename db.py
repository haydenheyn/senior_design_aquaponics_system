import psycopg2
from configparser import ConfigParser
import time
config = ConfigParser()
config.read("config.ini")


# Use the actual IP address of the server and the database credentials
db_host = config["database"]["host"]  
db_name = config["database"]["name"]
db_user = config["database"]["user"]
db_password = config["database"]["password"]

try:
    # Establish connection
    connection = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("Connection successful!")
    while True:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nodes;")
        rows = cursor.fetchall()
        print("Nodes:", rows)
        time.sleep(5)
    
except Exception as e:
    print("Error:", e)

finally:
    if connection:
        connection.close()
