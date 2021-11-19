from app.filters_process import filters
from app.log.logger import transfer_log as log


def pipeline(filter_name, argument, image_read):
    """
    Calling a pipeline using the input and output path as well as the image that will be processed.
    :param filter_name:
    :param argument:
    :param image_read:
    :return:
    """

    if filter_name == 'grayscale':
        log("Applying a grayscale filter...")
        fetch_class = filters.RgbToGray(image_read)
        image_read = fetch_class.rbg_to_gray()

    if filter_name == 'blur':
        log("Applying a blur filter...")
        fetch_class = filters.CleanToBlur(image_read)
        image_read = fetch_class.clean_to_blur(argument, argument)

    if filter_name == 'dilate':
        log("Applying a dilate filter...")
        fetch_class = filters.CleanToDilate(image_read)
        image_read = fetch_class.clean_to_dilate(argument, argument, argument)

    if filter_name == 'textcolor':
        log("Applying a text filter...")
        fetch_class = filters.FilterZeTeam(image_read, argument)
        image_read = fetch_class.text_color()

    return image_read
