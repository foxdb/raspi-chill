# import MySQLdb
import ConfigParser
import os


def init_log_file(file):
    f = open(file, 'w')
    f.close()


def writeToFile(file, date, temperature):
    f = open(file, 'a')
    f.write(str(date) + ',' +
            str(temperature) + '\n')
    f.close()
