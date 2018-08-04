import mysql.connector

class MysqlDatabase:
    host = "localhost"
    user = "root"
    passwd = ""
    database = "key2drive"

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        self.mycursor = self.mydb.cursor()

    def insertRow(self, table, data):
        placeholders = ', '.join(['%s'] * len(data))
        cols = data.keys()
        values = tuple(data[key] for key in data)
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, ",".join(cols), placeholders)
        self.mycursor.execute(sql, values)
        self.mydb.commit()
        print("Inserting to MySql Finished!")

    def insertPool(self, table, scraped_data):
        for datas in scraped_data:
            for data in datas:
                placeholders = ', '.join(['%s'] * len(data))
                cols = data.keys()
                values = tuple(data[key] for key in data)
                sql = "INSERT INTO %s (%s) VALUES (%s)" %(table, ",".join(cols), placeholders)
                self.mycursor.execute(sql, values)
                self.mydb.commit()
        print("Inserting to MySql Finished!")

    def selectField(self, table, field):
        self.sql = "SELECT %s FROM %s" % (field, table)
        self.mycursor.execute(self.sql)
        self.myresult = self.mycursor.fetchall()
        return self.myresult

