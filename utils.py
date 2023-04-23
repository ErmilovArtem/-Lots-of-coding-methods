import configparser


def get_signature():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='ANSI')
    return config['Main']['SIGNATURE']

