import configparser
import os
import errno
import logging
from datetime import datetime


def init_log_file(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    f = open(filename, 'a')
    f.close()


def writeToFile(filename, date, value):
    f = open(filename, 'a')
    f.write(str(date) + ',' +
            str(value) + '\n')
    f.close()


def get_date():
    return datetime.now().strftime('%Y%m%d_%H-%M-%S')


class Logger():
    def __init__(self, raw_project_name):
        # TODO sanitize raw, if no raw or not valid use current date
        self.project_name = raw_project_name

        # load configuration
        config_input = configparser.ConfigParser()
        config_input.read(os.path.dirname(
            os.path.realpath(__file__)) + "/config.ini")

        logsDir = config_input.get('data', 'logs_directory')

        self.INTERNAL_TEMPERATURE_LOG_FILE = "%s/%s-internal-temperature.log" % (
            logsDir, self.project_name)
        self.EVENTS_LOG_FILE = "%s/%s-events.log" % (
            logsDir, self.project_name)
        self.EXTERNAL_TEMPERATURE_LOG_FILE = "%s/%s-external-temperature.log" % (
            logsDir, self.project_name)
        self.GRAVITY_LOG_FILE = "%s/%s-gravity.log" % (
            logsDir, self.project_name)
        self.ANGLE_LOG_FILE = "%s/%s-angle.log" % (
            logsDir, self.project_name)
        self.RAW_SPINDEL_LOG_FILE = "%s/%s-raw-spindel.log" % (
            logsDir, self.project_name)

        # init log files
        init_log_file(self.INTERNAL_TEMPERATURE_LOG_FILE)
        init_log_file(self.EVENTS_LOG_FILE)
        init_log_file(self.EXTERNAL_TEMPERATURE_LOG_FILE)
        init_log_file(self.GRAVITY_LOG_FILE)
        init_log_file(self.ANGLE_LOG_FILE)
        init_log_file(self.RAW_SPINDEL_LOG_FILE)

        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y%m%d_%H-%M-%S',
            filename=self.EVENTS_LOG_FILE,
            level=logging.DEBUG
        )

    def writeExternalTemperature(self, value):
        writeToFile(self.EXTERNAL_TEMPERATURE_LOG_FILE, get_date(), value)

    def writeInternalTemperature(self, value):
        writeToFile(self.INTERNAL_TEMPERATURE_LOG_FILE, get_date(), value)

    def writeAngle(self, value):
        writeToFile(self.ANGLE_LOG_FILE, get_date(), value)

    def writeRawSpindel(self, value):
        writeToFile(self.RAW_SPINDEL_LOG_FILE, get_date(), value)

    def writeGravity(self, value):
        writeToFile(self.GRAVITY_LOG_FILE, get_date(), value)

    def info(self, message):
        logging.info(message)


# if __name__ == "__main__":
#     log = Logger('hello_ben')
#     print log.project_name
#     log.info('Oh hi')
#     log.writeGravity(12)
#     log.writeInternalTemperature(28)
#     log.writeExternalTemperature(28)
