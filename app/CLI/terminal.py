import os
import sys
from cv2 import cv2
from app.filters_process.pipeline import pipeline as pip
from app.log.logger import transfer_log as log, clear_log, throw_log
from app.CLI.read_CLI import reading_cli as default_config
import app.filters_process.get as get


def initialisation():
    """
    :return:
    """
    log('\n----------------------\n  Running the file...\n-----------------------')

    clear_log()
    args = sys.argv
    content = {
        "input_dir": '',
        "output_dir": '',
        "log_file": '',
        "filters:": '',
    }

    for i, arg in enumerate(args):

        if arg == '--config-file':
            if i + 1 >= len(args):
                log("ERROR : IndexError : You did not provided a file.")
                return sys.exit(0)

            if args[i + 1] == 'imagefilter.log':
                content['log_file'] = args[i + 1]
            elif args[i + 1] == 'cli.ini':
                content = default_config(args[i + 1])
                return content

        if arg == "-h":
            print("\nOptions :")
            print("-h , --help\n"
                  "-i , --input_dir <directory>\n"
                  "-o , --output_dir <directory>\n"
                  "--f, --filters <-h for more help>\n")
            return sys.exit(0)

    return path_analyse(content)


def verify_submit(cmd, has_argument, default_path):
    if has_argument >= len(cmd):
        log(f"ERROR : IndexError : You did not provided an {default_path} path.")
        return sys.exit(0)

    directory = cmd[has_argument]
    if default_path == 'output':
        return directory

    if not os.path.exists(f"{directory}"):
        log("ERROR : IndexError : The path provided does not exist.")
        return sys.exit(0)
    else:
        return directory


def path_analyse(content):
    """
    :param content:
    :return:
    """
    args = sys.argv
    for i, arg in enumerate(args):

        if arg == "-i":
            content["input_dir"] = verify_submit(args, i + 1, "input")

        if arg == "-o":
            content['output_dir'] = verify_submit(args, i + 1, "output")

        if arg == '--f':
            if i + 1 >= len(args):
                log("ERROR : IndexError : You did not provided a filter.")
                return

            filters = args[i + 1]
            content['filters'] = filters

    return content


def processing(path):

    filter_argument = get.filters(path['filters'])
    images_list = get.images(path['input_dir'])
    filtered_image_directory = path['output_dir']
    log_file = path['log_file']

    if len(images_list) == 0:
        return log('ERROR : IndexError : The directory returned NULL.')

    if not os.path.exists(f"{filtered_image_directory}"):
        log(f'Creating directory {filtered_image_directory}...')
        os.makedirs(f"{filtered_image_directory}")

    for image in images_list:
        log(f"Opening image data from = {path['input_dir']}/{image}")
        image_read = cv2.imread(f"{path['input_dir']}/{image}")
        to_directory_filter = f"{path['output_dir']}/{image}"

        for filter_name, argument in filter_argument.items():
            image_read = pip(filter_name, argument, image_read)

        cv2.imwrite(to_directory_filter, image_read)
        log(f"Save result image to = {to_directory_filter}\n")

    return throw_log(log_file)
