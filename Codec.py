from datetime import datetime
import struct
import os

# SIGNATURE = utils.get_signature()
SIGNATURE_INDEX = 5
VERSION = 0
LENGTH = ''
DATETIME = ''
ALGORITHM = 0


class Codec:
    def get_name_file(self, file_name):
        return os.path.basename(file_name)

    def get_date_file(self, file_name):
        date_time = datetime.fromtimestamp(os.path.getctime(file_name)).strftime('%Y-%m-%d %H:%M:%S')
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return date_time

    def get_len_file(self, file_name):
        return os.path.getsize(file_name)

    def get_data_file(self, file_name):
        with open(file_name, 'rb') as file:
            data = file.read()
        return data
