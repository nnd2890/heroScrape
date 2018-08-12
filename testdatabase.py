from mysql_database import MysqlDatabase

live_database = MysqlDatabase()
table = "live"
col = "Commodity"
id = 2
dict = {'Price': '4000', 'High': '4679', 'POS': 1.54, 'Commodity': 'ZINC', 'Chg': '71', 'Time': '23:30:01', 'Open': '4608', 'perChg': '1.54', 'NEG': 0.02, 'Low': '4564'}
live_database.update_row(table,dict, id)