from app.filters_process import filters
from app.log.logger import transfer_log as log


def pipeline(filter_name, argument, image_read):
    """
    Calling a pipeline of filters using the the image, the filter_name and its argument.
    :param filter_name: string value that will be used to recognize which filter to use.
    :param argument: int value, or string depending on the filter.
    :param image_read: image converted to object image.
    :return: return the image with the filters.
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
