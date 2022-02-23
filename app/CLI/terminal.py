<<<<<<< HEAD
import cv2 as cv2
=======
>>>>>>> Christopher
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
    Firstly, clear the log file from the previous use.
    Then for each arguments, we are gonna stock them and catch a main command.
    Then it will create a dictionary used for the entire execution of the file.
    For each arguments, if one march a specific command, do something.
    :return: the dictionary depending on the arguments submitted.
    """
    log('\n----------------------\n  Running the file...\n-----------------------')

    clear_log()
    args = sys.argv
    content = {
        "input_dir": '',
        "output_dir": '',
        "log_file": '',
        "filters": '',
        "extension": '',
    }

    for i, arg in enumerate(args):
        has_argument = i + 1

        if arg == "-h":
            print("\nOptions :")
            print("\n ------------------------HELP---------------------------\n"
                  "|-h  --help                                             |\n"
                  "|-------------------------------------------------------|\n"
                  "|-i  --input_dir <directory>                            |\n"
                  "|-------------------------------------------------------|\n"
                  "|-o  --output_dir <directory>                           |\n"
                  "|-------------------------------------------------------|\n"
                  "|--f  --filters                                         |\n"
                  "|-------------------------------------------------------|\n"
                  "|--config-file cli.ini                                  |\n"
                  "|-------------------------------------------------------|\n"
                  "|--list-filters  <list of all available filters>        |\n"
                  "|-------------------------------------------------------|\n"
                  "|--log-file imagefilter.log                             |\n"
                  " ------------------------------------------------------- \n")
            print(" ---------------------------------------------------------- \n"
                  '|  Usage example : -i data/input -o data/output <filters>  |\n'
                  " ---------------------------------------------------------- ")

            return sys.exit(0)

        if arg == '--list-filters':
            print("\nOptions :")
            print('\n --------------------FILTERS------------------- \n'
                  '|"grayscale"  <Color to Gray>                  |\n'
                  '|----------------------------------------------|\n'
                  '|"blur:integer_odd"  <Clean to Blur>           |\n'
                  '|----------------------------------------------|\n'
                  '|"dilate:integer"  <Clean to Dilate>           |\n'
                  '|----------------------------------------------|\n'
                  '|"textcolor:your_text-#000000"  <FilterZeTeam> |\n'
                  ' ---------------------------------------------- \n')
            print(' ------------------------------------------------------------------ \n'
                  '|  Usage example : --f "blur:5|grayscale|textcolor:Hello-#2678df"  |\n'
                  ' ------------------------------------------------------------------ ')
            return sys.exit(0)

        if arg == '--config-file':
            if has_argument >= len(args):
                log("ERROR : IndexError : You did not provided a file.")
                return sys.exit(0)

            if args[has_argument] == 'cli.ini':
                content = default_config(args[has_argument])

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
            if has_argument >= len(args):
                log("ERROR : IndexError : You did not provided a path.")
                return sys.exit(0)

            content['extension'] = 'mp4'
            return content

    return content


def verify_submit(cmd, has_argument, default_path):
    """
    This function will verify if the command match any known command, and if it's preceded
    of a directory path. If not, it will log and error in the log file.
    :param cmd: The command fetched from the user input.
    :param has_argument: Is the command followed with an argument ?
    :param default_path: Either the input or the output path.
    :return: return a system.exist or the validated directory path.
    """
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
    This function will analyse the command and execute a function if the condition is met.
    :param content: The dictionary content used for execution of the program.
    :return: The dictionary content.
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
    """
    This function will process a default option which is basically all files in a specific
    dictionary and send them to an output dictionary with some filters if they were defined
    in the options.
    Some errors will be catched, but not all.
    :param content: The dictionary content used for execution of the program.
    :return: Either a log or nothing.
    """

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
    """
    This function will process a gif option, it will use X amout of specified image, filter
    them and send them back to the gif maker function with the desired filters.
    Some errors will be catched, but not all.
    :param content: The dictionary content used for execution of the program.
    :return: Either a log or nothing.
    """
    content = path_analyse(content)
    content = path_analyse(content)
    # Error if -i or -o missing, not fixed.

<<<<<<< HEAD
    if path is None:
        return
    """
    
    If the path is empty : nothing happened
    """
    args = sys.argv
    for i, arg in enumerate(args):
        if arg == '--f':

            if i + 1 >= len(args):
                log("ERROR : IndexError : You did not provided a filter.")
                return
            """
            
            If the filter is unknown then an error message appears
            """

            images_list = os.listdir(path['input_dir'])
            if len(images_list) == 0:
                return log('ERROR : IndexError : The directory returned NULL.')
            """
            
            If there is no image then an error message appears
            """
=======
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
>>>>>>> Christopher

        for filter_name, argument in filter_argument.items():
            image_read = pip(filter_name, argument, image_read)

<<<<<<< HEAD
            filtered_image_directory = path['output_dir']
            if not os.path.exists(f"{filtered_image_directory}"):
                log(f'Creating directory {filtered_image_directory}...')
                os.makedirs(f"{filtered_image_directory}")
                """
                
                Tidy the filtered images in "output", if "output" doesn't exist then an "output" is created
                """
=======
        image_filtered.append(Image.fromarray(image_read))
>>>>>>> Christopher

    create.gif(image_filtered, filtered_directory)

<<<<<<< HEAD
            for image in images_list:
                log(f"Opening image data from = {path['input_dir']}/{image}")
                image_read = cv2.imread(f"{path['input_dir']}/{image}")
                to_directory_filter = f"{path['output_dir']}/{image}"
                """
                
                Filter confirmation
                """
=======
    if log_file == 'log':
        return throw_log()
>>>>>>> Christopher

    return


def video_processing(content):
    """
    This function will process a video option, it will read the file, open it, save a frame,
    get the size (px) of the file, filter the frames and process the video back to its original
    extension file. This doesn't apply for anything else than .mp4.
    Some errors will be catched, but not all.
    :param content: The dictionary content used for execution of the program.
    :return: Either a log or nothing.
    """
    content = path_analyse(content)
    # Error if -i or -o missing, not fixed.

    filter_argument = get.filters(content['filters'])
    filtered_directory = content['output_dir']
    origin_directory = content['input_dir']
    log_file = content['log_file']

    if not os.path.exists(f"{filtered_directory}"):
        log(f'Creating directory {filtered_directory}...')
        os.makedirs(f"{filtered_directory}")

    gray_or_not = 0
    text_or_not = 30
    if 'grayscale' in filter_argument.keys():
        gray_or_not = 1

    if 'textcolor' in filter_argument.keys():
        text_or_not = 60

    video_size = this.fetch_video_size(origin_directory, 'pain.mp4')
    video_images_list = this.slice_video(origin_directory, 'pain.mp4')

    if filter_argument is not None:
        video_filter = this.video_apply_filters(video_images_list, filter_argument)
        this.rewrite_video(filtered_directory, video_filter, video_size, gray_or_not, text_or_not)
    else:
        this.rewrite_video(filtered_directory, video_images_list, video_size, gray_or_not, text_or_not)

<<<<<<< HEAD
                cv2.imwrite(to_directory_filter, image_read)
                log(f"Save result image to = {to_directory_filter}\n")
                """
                
                Put the filtered image to "output"
                """
=======
    if log_file == 'log':
        return throw_log()
>>>>>>> Christopher

    return
