import cv2 as cv
from os import listdir, mkdir
from os.path import isfile, join
from natsort import natsorted
from shutil import copy, copyfile

def compare_histogram(image1_path, image2_path):
    src_image1 = cv.imread(image1_path)
    src_image2 = cv.imread(image2_path)

    if src_image1 is None or src_image2 is None:
        print('Could not open or find the images!')
        exit(0)

    hsv_image1 = cv.cvtColor(src_image1, cv.COLOR_BGR2HSV)
    hsv_image2 = cv.cvtColor(src_image2, cv.COLOR_BGR2HSV)
    
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # Hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # Concatenate lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]

    hist_image1 = cv.calcHist([hsv_image1], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_image1, hist_image1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    hist_image2 = cv.calcHist([hsv_image2], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_image2, hist_image2, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    
    return cv.compareHist(hist_image1, hist_image2, 0)


def variance_of_laplacian(image_path):
	# Compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
    image = cv.imread(image_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.Laplacian(gray, cv.CV_64F).var()


def remove_blurred(frames):
    vol_values = [variance_of_laplacian(frame) for frame in frames]
    threshold = max(vol_values)*0.15
    for i in range(len(vol_values)):
        if vol_values[i] < threshold:
            frames[i] = None
    print(vol_values)
    not_blurred = [x for x in frames if x is not None]
    return not_blurred


def remove_similar(frames):    
    final = []
    current, next = 0, 1
    final.append(frames[current])
    for i in range(len(frames)):
        for j in range(len(frames)):
            if j < current:
                continue
            correl = compare_histogram(frames[i],frames[j])
            print(i,j,correl)
            if correl < 0.95:
                final.append(frames[current])
                print("appended", frames[current])
                current = j
                break
            else:
                continue
        if i < current:
            continue
    return final

frames = natsorted([("./out/" + f) for f in listdir("./out") if isfile(join("./out", f))])
not_blurred = remove_blurred(frames)
final = remove_similar(not_blurred)

try:
    mkdir("preprocessed")
except Exception as e:
    pass

for i in final:
    copyfile(i, i.replace("./out/","./preprocessed/"))

