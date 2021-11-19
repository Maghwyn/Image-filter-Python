import os
from app.log.logger import transfer_log as log


def images(path):
    """
    The function will pass into argument a few valid extensions and compare the extension of the file to them.
    In the case where the extension does not match, the file is removed from the list.
    :return: the list of validated images.
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
    This function will perform a set of splitting operations in case the string match
    any characters. They will then be stocked into array and sorted in the right way for
    the program to work.
    :param argument: the filter and its value.
    :return: a dict with the key as the filter and the value as the filter value.
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
