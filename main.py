import os.path
from datetime import datetime
from Codec import Codec
from Coder import Coder
from Decoder import Decoder
import struct

NAME_FILE = 'C:/Users/cryin/OneDrive/Рабочий стол/text.txt'
a = 2
coders = "00000000"
coders_list = []

def menu():
    print('*** Program Codec ***'
          '\nSelect an action:'
          '\n1 - Coder'
          '\n2 - Decoder'
          '\n0 - Exit'
          '\n-> ', end='')
    return input()


def save_file_path(path, file_list):
    maindir = path.split("\\")[-1]
    for root, dirs, files in os.walk(path):
        for file in files:  # бежим по файлам в директории
            file_list.append(os.path.join(root, file)[len(path) - len(maindir):])
            # сохраняем путь от верхней папки до  имени файла


def input_files():
    print('Enter the full path to the file(s)'
          '\n(End of input - 0)')
    paths = []
    while True:
        path = input('-> ')
        if path == '0':
            return paths
        else:
            if os.path.isdir(path):
                save_file_path(path, paths)
            else:
                paths.append(os.path.basename(path))
        a = 4
        while not (int(a) in [0, 1, 2, 3, 8]):
            a = input("HAFF CODING or RLE? Pls, inp 1 or 2 if yea or 3 if all of that, 0 or na. 8 for intelectual neuronetwork choises")
        if int(a) == 1:
            coders_list.append(coders[:7] + "1")
        if int(a) == 2:
            coders_list.append(coders[:6] + "10")
        if int(a) == 3:
            coders_list.append(coders[:6] + "11")
        if int(a) == 8:
            coders_list.append("1"*8)
        if int(a) == 0:
            coders_list.append(coders)


def input_archive():
    print('Enter the full path to the archive(s)'
          '\n(End of input - 0)')
    # archive = []
    # while True:
    #     path = input('-> ')
    #     if path == '0':
    #         return archive
    #     else:
    #         archive.append(path)
    return input('-> ')


if __name__ == '__main__':

    while True:
        action = menu()
        if action == '0':
            break
        elif action == '1':  # кодирование
            files = input_files()
            print(coders_list)
            if len(files) != 0:
                coder = Coder()
                print(coders)
                archive = coder.archiver_files(files, coders_list)
                print('\nSuccessful launch! Result: \n', archive)
            else:
                print('List of files empty!')
        elif action == '2':  # декодирование
            archive = input_archive()
            if len(archive) != 0:
                decoder = Decoder()
                # print(decoder.check_signature(archive))
                print(decoder.give_me_dict(archive))
            else:
                print('List of archives empty!')
        else:
            print('Something went wrong. Please try again.')
    print('The program is completed...')
