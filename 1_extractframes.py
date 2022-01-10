import ffmpeg
from os import mkdir

filename = input("Enter video filename: ")

try:
    mkdir("out")
except Exception as e:
    pass

(ffmpeg.input(filename)
.output('out/%d.jpg',)
.run(capture_stdout=True, capture_stderr=True))