import mysql.connector

class Database:
    host = "localhost"
    user = "root"
    passwd = ""
    database = "tripadvisor"

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        self.mycursor = self.mydb.cursor()

    def mySql(self, scraped_data):
        table = "hotels"
        for datas in scraped_data:
            for data in datas:
                placeholders = ', '.join(['%s'] * len(data))
                cols = data.keys()
                values = tuple(data[key] for key in data)
                sql = "INSERT INTO %s (%s) VALUES (%s)" %(table, ",".join(cols), placeholders)
                self.mycursor.execute(sql, values)
                self.mydb.commit()
        print("Inserting to MySql Finished!")

