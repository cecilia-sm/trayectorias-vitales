'''

This perackground substraction based on OpenCV

Reference: https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html
'''

from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='videos/220425 ants-pinkwall.mp4')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()


###############################################################################

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

# read the input video or input images sequence
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

buff = capture.read()
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    # update the background model
    fgMask = backSub.apply(frame)

    cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    # Update buffer


    #show the current frame and the fg masks
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    kernel = np.ones((5,5),np.uint8)
    filtered = cv.morphologyEx(fgMask, cv.MORPH_OPEN, kernel)
    cv.imshow('FG filtered Mask', filtered)
    img = cv.merge((frame[:, :, 0] + filtered,
                   frame[:, :, 1] + filtered,
                   frame[:, :, 2] + filtered))
    # cv.imshow('FG filtered Mask', img)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break