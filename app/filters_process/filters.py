import numpy
from cv2 import cv2
from PIL import Image, ImageDraw, ImageFont
from app.log.logger import transfer_log as log


class RgbToGray:
    """
    Declare a class named RgbToGray.
    This class will declare the image_path passed as an argument, then transform it into B & W.

    :def rgb_to_gray: apply a B&W filter on the class image.
    """

    def __init__(self, my_image):
        self.image = my_image

    def rbg_to_gray(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)


class CleanToBlur:
    """
    Declare a class named CleanToBlur.
    This class will declare the image_path passed as an argument, then blur it.

    :def clean_to_blur: apply a blurred filter on the class image.
    :-> blur_strength_x: apply a blur strength on the x axis of the class image.
    :-> blur_strength_y: apply a blur strength on the y axis of the class image.
    """

    def __init__(self, my_image):
        self.image = my_image

    def clean_to_blur(self, blur_strength_x, blur_strength_y):
        if int(blur_strength_x) < 0 or int(blur_strength_y) < 0:
            log('ValueError : The blur filter failed => Negative dimensions are not allowed.')
            return self.image

        if int(blur_strength_x) % 2 == 0 or int(blur_strength_y) % 2 == 0:
            log('ValueError : The blur filter failed => Parameters can not be even.')
            return self.image

        return cv2.GaussianBlur(self.image, (int(blur_strength_x), int(blur_strength_y)), 0)


class CleanToDilate:
    """
    Declare a class named CleanToDilate.
    This class will declare the image_path passed as an argument, then dilate it.

    :def clean_to_dilate: apply a dilated filter on the class image.
    :-> dilate_strength_x: apply a dilate strength on the x axis of the class image.
    :-> dilate_strength_y: apply a dilate strength on the y axis of the class image.
    :-> iterations: apply the dilate to x number of pixels.
    """

    def __init__(self, my_image):
        self.image = my_image

    def clean_to_dilate(self, dilate_strength_x, dilate_strength_y, iterations):
        if int(dilate_strength_x) < 0 or int(dilate_strength_y) < 0:
            log('ValueError : The dilate filter failed => Negative dimensions are not allowed.')
            return self.image

        kernel = numpy.ones((int(dilate_strength_x), int(dilate_strength_y)), numpy.uint8)
        return cv2.dilate(self.image, kernel, iterations=int(iterations))


class FilterZeTeam:

    def __init__(self, my_image, text_hex_value):
        self.image = my_image
        self.text_hex = text_hex_value

    def text_color(self):

        split_text_hex = []
        if '-' in self.text_hex:
            split_text_hex = self.text_hex.split('-')

        # font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 2

        text = split_text_hex[0]
        split_text_hex[1] = split_text_hex[1].lstrip('#')
        rgb = tuple(int(split_text_hex[1][i: i + 2], 16) for i in (0, 2, 4))
        cv2.putText(self.image, text, (30, 80), font, font_scale, rgb, 2, cv2.LINE_AA)

        return self.image
