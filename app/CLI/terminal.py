import os
import sys
from cv2 import cv2
from PIL import Image
from app.filters_process.pipeline import pipeline as pip
from app.log.logger import transfer_log as log, clear_log, throw_log
from app.CLI.read_CLI import reading_cli as default_config
from app.Functions import get, create
from app.video import convert_video as this


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
        "filters": '',
        "extension": 'image',
    }

    for i, arg in enumerate(args):
        has_argument = i + 1

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
                  '"dilate:integer", CleanToDilate\n'
                  '"textcolor":Text-#000000", FilterZeTeam\n')
            print('Usage example : --f "blur:5|grayscale"\n')
            return sys.exit(0)

        if arg == '--config-file':
            if has_argument >= len(args):
                log("ERROR : IndexError : You did not provided a file.")
                return sys.exit(0)

            if args[has_argument] == 'cli.ini':
                content = default_config(args[has_argument])
                return content

        if arg == '--log-file':
            if has_argument >= len(args):
                log("ERROR : IndexError : You did not provided a file.")
                return sys.exit(0)

            if args[has_argument] == 'imagefilter.log':
                content['log_file'] = 'log'

        if arg == '--output-type=gif':
            content['extension'] = 'gif'
            return content

        if arg == '--video=pain.mp4':
            content['extension'] = 'mp4'
            return content

    return content


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


def default_processing(content):
    if content is None:
        return

    content = path_analyse(content)

    filter_argument = get.filters(content['filters'])
    images_list = get.images(content['input_dir'])
    filtered_directory = content['output_dir']
    origin_directory = content['input_dir']
    log_file = content['log_file']

    if len(images_list) == 0:
        return log('ERROR : IndexError : The directory returned NULL.')

    if not os.path.exists(f"{filtered_directory}"):
        log(f'Creating directory {filtered_directory}...')
        os.makedirs(f"{filtered_directory}")

    for image in images_list:
        log(f"Opening image data from = {origin_directory}/{image}")
        image_read = cv2.imread(f"{origin_directory}/{image}")
        to_directory_filter = f"{filtered_directory}/{image}"

        for filter_name, argument in filter_argument.items():
            image_read = pip(filter_name, argument, image_read)

        cv2.imwrite(to_directory_filter, image_read)
        log(f"Save result image to = {to_directory_filter}\n")

    if log_file == 'log':
        return throw_log()

    return


def gif_processing(content):
    content = path_analyse(content)

    images_list = get.images(content['input_dir'])
    filter_argument = get.filters(content['filters'])
    filtered_directory = content['output_dir']
    origin_directory = content['input_dir']
    log_file = content['log_file']

    image_filtered = []

    if len(images_list) == 0:
        return log('ERROR : IndexError : The directory returned NULL.')

    if not os.path.exists(f"{filtered_directory}"):
        log(f'Creating directory {filtered_directory}...')
        os.makedirs(f"{filtered_directory}")

    for image in images_list:
        log(f"Opening image data from = {origin_directory}/{image}")
        image_read = cv2.imread(f"{origin_directory}/{image}")

        for filter_name, argument in filter_argument.items():
            image_read = pip(filter_name, argument, image_read)

        image_filtered.append(Image.fromarray(image_read))

    create.gif(image_filtered, filtered_directory)

    if log_file == 'log':
        return throw_log()

    return


def video_processing(content):
    content = path_analyse(content)
    # Error if -i or -o missing

    filter_argument = get.filters(content['filters'])
    print(filter_argument)
    filtered_directory = content['output_dir']
    origin_directory = content['input_dir']
    log_file = content['log_file']

    if not os.path.exists(f"{filtered_directory}"):
        log(f'Creating directory {filtered_directory}...')
        os.makedirs(f"{filtered_directory}")

    gray_or_not = 0
    if 'grayscale' in filter_argument.keys():
        gray_or_not = 1

    video_size = this.fetch_video_size(origin_directory, 'pain.mp4')
    video_images_list = this.slice_video(origin_directory, 'pain.mp4')

    if filter_argument is not None:
        video_filter = this.video_apply_filters(video_images_list, filter_argument)
        this.rewrite_video(filtered_directory, video_filter, video_size, gray_or_not)
    else:
        this.rewrite_video(filtered_directory, video_images_list, video_size, gray_or_not)

    if log_file == 'log':
        return throw_log()

    return
