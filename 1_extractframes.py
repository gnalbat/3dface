import ffmpeg

filename = input("Enter video filename: ")

(ffmpeg.input(filename)
.output('out/%d.png',)
.run(capture_stdout=True, capture_stderr=True))