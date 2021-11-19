from cv2 import cv2
from app.filters_process.pipeline import pipeline as pip


def fetch_video_size(path, video_name):
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
    images_list = []
    video = cv2.VideoCapture(f'{path}/{vid_name}')
    while video.isOpened():

        frame_available, frame = video.read()
        if not frame_available:
            break

        images_list.append(frame)

    video.release()

    return images_list


def video_apply_filters(images_list, filters, strength):
    images_filtered = []
    for image in images_list:
        images_filtered.append(pip(filters, strength, image))

    return images_filtered


def rewrite_video(path, images_list, vid_size, is_gray):
    size = (vid_size[0], vid_size[1])
    if is_gray == 'grayscale':
        video = cv2.VideoWriter(f'{path}/project.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size, isColor=False)
    else:
        video = cv2.VideoWriter(f'{path}/project.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)

    for image in range(len(images_list)):
        video.write(images_list[image])

    video.release()


video_size = fetch_video_size('data/input', 'pain.mp4')
fetch_images = slice_video('data/input', 'pain.mp4')
video_filter = video_apply_filters(fetch_images, 'dilate', 12)
rewrite_video('data/hello', video_filter, video_size, 'dilate')