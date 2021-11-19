import os
from app.log.logger import transfer_log as log


def images(path):
    """
    :param path:
    :return:
    """
    images_list = []
    for image in os.listdir(path):
        if image.endswith('.jpeg' or '.png' or '.jpg' or '.svg'):
            images_list.append(image)
        else:
            log(f'ValueError : Invalid Format => {image} was ignored.\n')

    return images_list


def filters(argument):
    """
    :param argument:
    :return:
    """
    if argument == '':
        return None

    filter_argument = {}
    if '|' in argument:
        separated_argument = argument.split('|')
        for arg in separated_argument:
            if ':' in arg:
                temp_filter_argument = arg.split(':')
                filter_argument[str(temp_filter_argument[0])] = str(temp_filter_argument[1])
            else:
                filter_argument[str(arg)] = str(arg)
    else:
        if ':' in argument:
            temp_filter_argument = argument.split(':')
            filter_argument[str(temp_filter_argument[0])] = str(temp_filter_argument[1])
        else:
            filter_argument[str(argument)] = str(argument)

    log(f"Filters extracted and waiting to be applied : {filter_argument}\n")
    return filter_argument
