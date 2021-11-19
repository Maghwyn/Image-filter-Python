from cv2 import cv2
from app.filters_process.pipeline import pipeline as pip


def fetch_video_size(path, video_name):
    """
    This function will read a single frame of the video.mp4 and extract the frame dimension.
    :param path: The path directory of the selected file.
    :param video_name: The name of the selected file.
    :return: The dimension of the frame.
    """
    size = []
    video = cv2.VideoCapture(f'{path}/{video_name}')

    if video.isOpened():
        frame_available, frame = video.read()
        video_height, video_width, layers = frame.shape
        size.append(video_width)
        size.append(video_height)

    video.release()
    return size


def slice_video(path, vid_name):
    """
    This function will read the entire content of the video.mp4 and stock all its frame into a list.
    If the frame is not available from the video, the video will be closed.
    :param path: The path directory of the selected file.
    :param vid_name: The name of the selected file.
    :return: Return a list of all the frames inside the selected video.mp4.
    """
    images_list = []
    video = cv2.VideoCapture(f'{path}/{vid_name}')
    while video.isOpened():

        frame_available, frame = video.read()
        if not frame_available:
            break

        images_list.append(frame)

    video.release()

    return images_list


def video_apply_filters(images_list, filters):
    """
    This will simply add on each frames the filter desired.
    :param images_list: List of all frames.
    :param filters: List of all filters desired.
    :return: The list of all the frames filtered.
    """
    images_filtered = []
    for image in images_list:
        for filter_name, argument in filters.items():
            images_filtered.append(pip(filter_name, argument, image))

    return images_filtered


def rewrite_video(path, images_list, vid_size, is_gray, is_text):
    """
    The function will recreate the original video with the filtered frames.
    :param path: The desired output directory.
    :param images_list: The list of all the frames filtered.
    :param vid_size: The size of the video fetched from another function.
    :param is_gray: If the filter gray was applied, do something specific to avoid errors.
    :param is_text: If the filter textcolor was applied, do something specific to avoid errors.
    """
    size = (vid_size[0], vid_size[1])
    if is_gray == 1:
        video = cv2.VideoWriter(f'{path}/project.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size,
                                isColor=False)
    else:
        video = cv2.VideoWriter(f'{path}/project.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), is_text, size)

    for image in range(len(images_list)):
        video.write(images_list[image])

    video.release()
