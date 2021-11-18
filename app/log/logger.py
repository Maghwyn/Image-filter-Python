from datetime import datetime
import os


def time():
    """
    Saves the current time imported from the library datetime and refine it visually.
    :return: the refined current time.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def transfer_log(string):
    """
    Saves a string of instructions inside the log file imagefilter.log.
    In case of an error loading the file, return [ERROR : FileNotFoundError].
    :param string: the string of the function waiting to be processed to the file.log.
    """

    try:
        with open("app/log/imagefilter.log", "a") as f:
            f.write(f'{time()} : {string}\n')
    except FileNotFoundError:
        print('ERROR : FileNotFoundError : Target "imagefilter.log" couldn\'t be fetched.')


def dump_log():
    """
    On call, read the log file imagefilter.log and print it to the terminal.
    In case of an error loading the file, return [ERROR : FileNotFoundError].
    """

    try:
        with open("app/log/imagefilter.log", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print('ERROR : FileNotFoundError : Target "imagefilter.log" couldn\'t be fetched.')


def clear_log():
    """
    :return:
    """

    try:
        with open("app/log/imagefilter.log", "a") as f:
            f.truncate(0)
    except FileNotFoundError:
        print('ERROR : FileNotFoundError : Target "imagefilter.log" couldn\'t be fetched.')


def throw_log(log_file):
    """
    :return:
    """
    if os.path.isfile(f'app/log/{log_file}'):
        return dump_log()

    return
