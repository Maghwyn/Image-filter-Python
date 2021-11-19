import os
import sys
from cv2 import cv2
from PIL import Image
from app.filters_process.pipeline import pipeline as pip
from app.log.logger import transfer_log as log, clear_log, throw_log
from app.CLI.read_CLI import reading_cli as default_config
from app.Functions import get, create


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
        "extension": '',
    }

    for i, arg in enumerate(args):
        has_argument = i + 1

        if arg == '--config-file':
            if has_argument >= len(args):
                log("ERROR : IndexError : You did not provided a file.")
                return sys.exit(0)

            if args[has_argument] == 'imagefilter.log':
                content['log_file'] = args[has_argument]
            elif args[has_argument] == 'cli.ini':
                content = default_config(args[has_argument])
                return content

        if arg == "-h":
            print("\nOptions :")
            print("-h , --help\n"
                  "-i , --input_dir <directory>\n"
                  "-o , --output_dir <directory>\n"
                  "--f, --filters <-h for more help>\n"
                  "--config-file cli.ini\n"
                  "--list-filters\n")
            return sys.exit(0)

        if arg == '--list-filters':
            print("\nFilters options :")
            print('"grayscale", ColorToGray\n'
                  '"blur:integer_odd", CleanToBlur\n'
                  '"dilate:integer", CleanToDilate\n')
            print('Usage example : --f "blur:5|grayscale"\n')
            return sys.exit(0)

        if arg == '--output-type':
            if has_argument >= len(args):
                log("ERROR : IndexError : You did not provided an extension.")

            if args[has_argument] == 'gif':
                content['extension'] = args[has_argument]

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

    filtered_directory = path['output_dir']
    extension_file = path['extension']
    log_file = path['log_file']
    image_filtered = []

    if len(images_list) == 0:
        return log('ERROR : IndexError : The directory returned NULL.')

    if not os.path.exists(f"{filtered_directory}"):
        log(f'Creating directory {filtered_directory}...')
        os.makedirs(f"{filtered_directory}")

    for image in images_list:
        log(f"Opening image data from = {path['input_dir']}/{image}")
        image_read = cv2.imread(f"{path['input_dir']}/{image}")
        to_directory_filter = f"{path['output_dir']}/{image}"

        for filter_name, argument in filter_argument.items():
            image_read = pip(filter_name, argument, image_read)

        # gif
        # image_filtered.append(Image.fromarray(image_read))

        cv2.imwrite(to_directory_filter, image_read)
        log(f"Save result image to = {to_directory_filter}\n")

    # gif
    if extension_file == 'gif':
        create.gif(image_filtered, filtered_directory)

    return throw_log(log_file)
