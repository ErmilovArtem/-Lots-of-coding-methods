import pickle
import sys
from datetime import datetime

from bitarray import bitarray

import RLE
from Haffman import HaffmanCoder
from Codec import Codec
from utils import get_signature
import struct
import os
from colorama import init, Fore, Back, Style


class Coder(Codec):
    def __init__(self):
        self.codec = Codec()
        self.archive = self.get_head_archive()

    def get_head_archive(self):
        byte_array = bytearray(get_signature().encode('utf-8'))  # изменяемый байт-список
        byte_array.extend('1'.encode('utf-8'))
        byte_array.extend('0'.encode('utf-8'))
        byte_array.extend(struct.pack("I", 19))
        date_time = str(datetime.now())[:19] \
            .replace(" ", "") \
            .replace("-", "") \
            .replace(":", "")
        for i in range(0, 7):
            byte_array.extend(bytes([int(date_time[i * 2:(i + 1) * 2])]))  # метод, что пушит больше чем append
        return byte_array

    def haffman_massage_cod(self, byte_array, data):
        print(Fore.CYAN + str(1) + Style.RESET_ALL)
        Alph_Chars = []
        for i in range(256):
            Alph_Chars.append((bytes([i])))
        huff = HaffmanCoder(message=data, alph_chars=Alph_Chars)
        sort_okets = str(huff.sorted_okets).encode("utf-8")
        data_in_compress = huff.byte_coded_message

        archive_size = self.archive[8:12]
        self.archive[8:12] = struct.pack("I",
                                         73 + len(sort_okets + data_in_compress) + struct.unpack("I", archive_size)[0])

        byte_array.extend(struct.pack("I", len(sort_okets)))
        byte_array.extend(sort_okets)
        byte_array.extend(struct.pack("I", len(data_in_compress)))
        byte_array.extend(data_in_compress)

    def rle_message_cod(self, byte_array, data):
        print(Fore.CYAN + str(0) + Style.RESET_ALL)
        data = RLE.codeste(data)
        byte_array.extend(struct.pack("I", len(data)))
        byte_array.extend(data)  # метод, что пушит больше чем append
        archive_size = self.archive[8:12]
        self.archive[8:12] = struct.pack("I", 73 + len(data) + struct.unpack("I", archive_size)[0])

    def package_file(self, file_name, file_date_time, cod_of_coder, file_data):
        byte_array = bytearray((file_name + (64 - len(file_name)) * '\x00').encode('utf-8'))
        date_time = str(file_date_time)[:19] \
            .replace(" ", "") \
            .replace("-", "") \
            .replace(":", "")
        for i in range(0, 7):
            byte_array.extend(bytes([int(date_time[i * 2:(i + 1) * 2])]))  # метод, что пушит больше чем append
        data = file_data
        coded_cod = int(cod_of_coder, 2)
        print(Fore.CYAN + str(coded_cod) + Style.RESET_ALL)

        if coded_cod == 255:
            print(Fore.CYAN + str(8) + Style.RESET_ALL)
            Alph_Chars = []
            for i in range(256):
                Alph_Chars.append((bytes([i])))
            huff = HaffmanCoder(message=data, alph_chars=Alph_Chars)
            sort_okets = str(huff.sorted_okets).encode("utf-8")
            data_in_compress = huff.byte_coded_message
            if (sys.getsizeof(sort_okets) + sys.getsizeof(data_in_compress)) < sys.getsizeof(data):
                coded_cod = 1
                if sys.getsizeof(
                        RLE.codeste(data)) < sys.getsizeof(sort_okets) + sys.getsizeof(
                                data_in_compress):
                    coded_cod = 2
            else:
                if sys.getsizeof((RLE.codeste(data)) < sys.getsizeof(data)):
                    coded_cod = 2
                coded_cod = 0

        byte_array.extend(bytes([coded_cod]))
        if coded_cod == 1:
            self.haffman_massage_cod(byte_array, data)
            self.archive.extend(byte_array)

        if coded_cod == 2:
            self.rle_message_cod(byte_array, data)
            self.archive.extend(byte_array)

        if coded_cod == 3:
            self.haffman_massage_cod(byte_array, RLE.codeste(data.decode("utf8")))
            self.archive.extend(byte_array)

        if coded_cod == 0:
            print(Fore.CYAN + str(0) + Style.RESET_ALL)
            byte_array.extend(struct.pack("I", len(data)))
            byte_array.extend(data)  # метод, что пушит больше чем append
            archive_size = self.archive[8:12]
            self.archive[8:12] = struct.pack("I", 73 + len(data) + struct.unpack("I", archive_size)[0])
            # print(struct.unpack("I", archive_size)[0])
            self.archive.extend(byte_array)
        print(byte_array)

    def archiver_files(self, files, coders):
        for file in files:
            # file_name = self.codec.get_name_file(file)
            file_name = file
            file_date_time = self.codec.get_date_file(file)
            file_data = self.codec.get_data_file(file)
            self.package_file(file_name, file_date_time, coders[files.index(file)], file_data)
            self.create_archive()
        return self.archive

    def create_archive(self, ):
        with open('archive_1', 'wb') as archive_file:
            archive_file.write(self.archive)
