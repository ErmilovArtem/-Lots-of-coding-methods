from datetime import datetime

import RLE
from utils import get_signature
from Codec import Codec
import struct
import os
from Haffman import HaffmanCoder

class Decoder(Codec):
    def __init__(self):
        self.codec = Codec()

    def give_me_byte_file_dict(self, be):
        list_of_files = []
        counter = 0
        b = be
        end_str = " " * len(b) * 2

        while (len(b) > 25):
            dict = {}
            print(b[0:64], 8888888)
            dict["Name"] = b[0:64].decode('utf8').replace("\x00", "")
            dict["DateOfFile"] = datetime(year=int(str(b[64]) + str(b[65])),
                                          month=int(str(b[66])),
                                          day=int(str(b[67])),
                                          hour=int(str(b[68])),
                                          minute=int(str(b[69])),
                                          second=int(str(b[70])))
            dict["Coder"] = b[71]
            if dict["Coder"] == 1:
                bytearray = b[72:76]
                dict["DataSize"] = [struct.unpack("I", bytearray)[0], 0]
                sorted_okets = eval(b[76:76 + dict["DataSize"][0]].decode('utf8'))
                bytearray = b[76 + dict["DataSize"][0]:76 + dict["DataSize"][0] + 4]
                dict["DataSize"][1] = struct.unpack("I", bytearray)[0]
                byte_coded_message = b[76 + dict["DataSize"][0] + 4:76 + dict["DataSize"][0] + 4 + dict["DataSize"][1]]
                hf = HaffmanCoder()
                hafffed = hf.Haffed(sorted_okets)
                for k, v in hafffed.items():
                    if str(v) == min(list(map(str, hafffed.values()))):
                        key = k
                decoded_message = hf.DecodeThisToStr(byte_coded_message, hafffed)
                if(decoded_message.count(key[2:-1]) != sorted_okets[key]):
                    decoded_message = decoded_message[:sorted_okets[key] - decoded_message.count(key[2:-1])]
                dict["Data"] = decoded_message
                counter = counter + 76 + dict["DataSize"][0] + dict["DataSize"][1] + 4
                end_str = end_str[76 + dict["DataSize"][0] + dict["DataSize"][1] + 4:]
                b = b[76 + dict["DataSize"][0] + dict["DataSize"][1] + 4:]
                list_of_files.append(dict)
            if dict["Coder"] == 2:
                bytearray = b[72:76]
                dict["DataSize"] = struct.unpack("I", bytearray)[0]
                end_str = end_str[76:] + b[76:76 + dict["DataSize"]].decode('utf8') + end_str[76 + dict["DataSize"]:]
                dict["Data"] = b[76:76 + dict["DataSize"]]
                dict["Data"] = RLE.decodeste(dict["Data"]).decode('utf8')
                counter = counter + 76 + dict["DataSize"]
                end_str = end_str[76 + dict["DataSize"]:]
                b = b[76 + dict["DataSize"]:]
                list_of_files.append(dict)
            if dict["Coder"] == 3:
                bytearray = b[72:76]
                dict["DataSize"] = [struct.unpack("I", bytearray)[0], 0]
                sorted_okets = eval(b[76:76 + dict["DataSize"][0]].decode('utf8'))
                bytearray = b[76 + dict["DataSize"][0]:76 + dict["DataSize"][0] + 4]
                dict["DataSize"][1] = struct.unpack("I", bytearray)[0]
                byte_coded_message = b[76 + dict["DataSize"][0] + 4:76 + dict["DataSize"][0] + 4 + dict["DataSize"][1]]
                hf = HaffmanCoder()
                hafffed = hf.Haffed(sorted_okets)
                for k, v in hafffed.items():
                    if str(v) == min(list(map(str, hafffed.values()))):
                        key = k
                decoded_message = hf.DecodeThisToStr(byte_coded_message, hafffed)
                if(decoded_message.count(key[2:-1]) != sorted_okets[key]):
                    decoded_message = decoded_message[:sorted_okets[key] - decoded_message.count(key[2:-1])]
                dict["Data"] = RLE.decodeste(decoded_message)
                counter = counter + 76 + dict["DataSize"][0] + dict["DataSize"][1] + 4
                end_str = end_str[76 + dict["DataSize"][0] + dict["DataSize"][1] + 4:]
                b = b[76 + dict["DataSize"][0] + dict["DataSize"][1] + 4:]
                list_of_files.append(dict)
            if dict["Coder"] == 0:
                bytearray = b[72:76]
                dict["DataSize"] = struct.unpack("I", bytearray)[0]
                end_str = end_str[76:] + b[76:76 + dict["DataSize"]].decode('utf8') + end_str[76 + dict["DataSize"]:]
                dict["Data"] = b[76:76 + dict["DataSize"]].decode('utf8')
                counter = counter + 76 + dict["DataSize"]
                end_str = end_str[76 + dict["DataSize"]:]
                b = b[76 + dict["DataSize"]:]
                list_of_files.append(dict)
        return list_of_files

    def give_me_dict(self, path_archive):
        archive_data = self.codec.get_data_file(path_archive)
        b = bytes(archive_data)
        end_str = (b[:8] + b[4:8] + b[12:20]).decode('utf8')  # декод в строку
        dict = {}
        dict["Format"] = end_str[0:6]
        dict["Ver"] = (int(end_str[6]))
        dict["Algo"] = (int(end_str[7]))
        byte_array = b[8:12]
        dict["AllSize"] = struct.unpack("I", byte_array)[0]
        dict["Date"] = datetime(year=int(str(b[12]) + str(b[12 + 1])),
                                month=int(str(b[12 + 2])),
                                day=int(str(b[12 + 3])),
                                hour=int(str(b[12 + 4])),
                                minute=int(str(b[12 + 5])),
                                second=int(str(b[12 + 6])))
        dict["Files"] = self.give_me_byte_file_dict(b[19:])
        #print(dict['Files'])
        self.unpack_files(dict['Files'])
        return dict['Files']

    def check_signature(self, archive):
        with open(archive, 'rb') as archive_file:
            signature = archive_file.read()[:6]
        return signature == get_signature().encode()

    def unpack_files(self, file_list):
        for file in file_list:
            file['Name'] = "DIR\\" + file['Name']
            if len(file['Name'].split("\\")) > 1:
                for i in range(1, len(file['Name'].split("\\"))):  # перебираем все директории
                    dir_on_str = str(file['Name'].split("\\")[:i]) \
                        .replace("['", "") \
                        .replace("']", "") \
                        .replace("', '", "\\")  # (магия строк)
                    if not os.path.isdir(dir_on_str):  # если путя нет
                        os.mkdir(dir_on_str)  # создаем
        for file in file_list:
            #file['Name'] = "DIR\\" + file['Name']
         #   print(file['Data'])
            with open(file['Name'], 'wb') as f:
                f.write(file['Data'].encode('utf8'))  # создание файла внутри уже созданных директорий
