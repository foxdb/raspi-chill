# import MySQLdb
import ConfigParser
import os


config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")

OUTPUT_FILE = config.get('data', 'output_file')

f = open(OUTPUT_FILE, 'w')
f.close()

# class Database:

#     host =
#     user =
#     password =
#     db =

#     def __init__(self):
#         self.connection = MySQLdb.connect(
#             self.host, self.user, self.password, self.db)
#         self.cursor = self.connection.cursor()

#     def insert(self, query):
#         try:
#             self.cursor.execute(query)
#             self.connection.commit()
#         except:
#             self.connection.rollback()

#     def query(self, query):
#         cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(query)

#         return cursor.fetchall()

#     def __del__(self):
#         self.connection.close()


# def insert(temperature):
#     db = Database()

#     # Data Insert into the table
#     query = """
#         INSERT INTO measurements
#         (`type`, `value`)
#         VALUES
#         ('moisture', """ + str(temperature) + """)
#         """

#     db.insert(query)
#     return

def writeToFile(date, temperature):
    f = open(OUTPUT_FILE, 'a')
    f.write(str(date) + ',' +
            str(temperature) + '\n')
    f.close()
