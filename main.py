from app.CLI import terminal as core

content = core.initialisation()

if content['extension'] == "'image'":
    core.default_processing(content)

if content['extension'] == 'gif':
    core.gif_processing(content)

if content['extension'] == 'mp4':
    core.video_processing(content)
