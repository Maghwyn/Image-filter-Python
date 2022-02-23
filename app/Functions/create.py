def gif(images_src, output_dir):
    """
    Simple function creating a gif from some image.
    They will be used a frames and layered on top of each other.
    :param images_src: the image filtered or not, converted with cv2.
    :param output_dir: where the image will be saved.
    :return: none.
    """
    frames = []
    for image in images_src:
        frames.append(image)

    frames[0].save(f'{output_dir}/new.gif', format='GIF', append_images=frames, save_all=True, duration=300, loop=0)
