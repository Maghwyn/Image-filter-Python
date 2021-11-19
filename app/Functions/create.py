def gif(images_src, output_dir):
    frames = []
    for image in images_src:
        frames.append(image)

    frames[0].save(f'{output_dir}/new.gif', format='GIF', append_images=frames, save_all=True, duration=300, loop=0)
