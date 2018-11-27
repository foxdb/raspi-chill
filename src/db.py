import ConfigParser
import os


def init_log_file(file):
    f = open(file, 'a')
    f.close()


def writeToFile(file, date, temperature):
    f = open(file, 'a')
    f.write(str(date) + ',' +
            str(temperature) + '\n')
    f.close()
