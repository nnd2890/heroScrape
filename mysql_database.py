import mysql.connector

class MysqlDatabase:
    # host = "localhost"
    # user = "root"
    # passwd = ""
    # database = "live_mcx_ncdex"
    host = "sql9.freemysqlhosting.net"
    user = "sql9251662"
    passwd = "Sz5gVdAj8T"
    database = "sql9251662"

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

    def select_field(self, table, field):
        self.sql = "SELECT %s FROM %s" % (field, table)
        self.mycursor.execute(self.sql)
        self.myresult = self.mycursor.fetchall()
        return self.myresult

    def select_field_where(self, table, field, name):
        self.sql = "SELECT * FROM %s WHERE %s ='%s'" % (table, field, name)
        self.mycursor.execute(self.sql)
        self.myresult = self.mycursor.fetchone()
        return self.myresult

    def update_row(self, table, dict, id):
        set = ', '.join('{}=%s'.format(k) for k in dict)
        values = tuple(dict[key] for key in dict)
        sql = "UPDATE {0} SET {1} WHERE id = '{2}'".format(table, set, id)
        self.mycursor.execute(sql, values)
        self.mydb.commit()
        print("Updating to MySql Finished!")

    def row_existed(self, table, col, name):
        sql = "SELECT COUNT(1) FROM " + table + " WHERE " + col + " = '" + name + "'"
        self.mycursor.execute(sql)
        row_count = self.mycursor.fetchone()[0]
        if row_count:
            return True
        else:
            return False


