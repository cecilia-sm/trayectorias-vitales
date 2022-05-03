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

# Read one frame to get the size of it
ret, frame = capture.read()
height, width = frame.shape[:2]
# Create the buffer where the tracks are going to be accumulated
buff = np.zeros((height, width, 3), np.uint8)
buff = cv.cvtColor(buff, cv.COLOR_BGR2HSV)
# Create the writer
writer = cv.VideoWriter(args.input + "_output.avi",
                        cv.VideoWriter_fourcc(*"MJPG"),
                        30,
                        (width, height)
                        )
# Initialize the amount of frames we want to wait for the video to stabilize
# before starting to accumulate the tracks
is_first_frames = 40
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    # Blur the frame
    # frame = cv.bilateralFilter(frame, 9, 75, 75)
    # frame = cv.blur(frame,(5,5))
    # update the background model
    fgMask = backSub.apply(frame)

    # Filter noise with morphological operators
    median = cv.medianBlur(fgMask, 5)
    kernel = np.ones((3,3),np.uint8)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
    filtered = cv.morphologyEx(median, cv.MORPH_OPEN, kernel)
    filtered = cv.morphologyEx(filtered, cv.MORPH_CLOSE, kernel)
    kernel = np.ones((5,5),np.uint8)
    filtered = cv.morphologyEx(filtered, cv.MORPH_OPEN, kernel)
    filtered = cv.morphologyEx(filtered, cv.MORPH_CLOSE, kernel)
    filtered = cv.morphologyEx(filtered, cv.MORPH_ERODE, kernel)

    # filtered = fgMask
    _, filtered = cv.threshold(filtered, 100, 255, cv.THRESH_BINARY)
    # Update buffer

    if is_first_frames>0:
        is_first_frames -= 1
    else:
        _, mask_buff = cv.threshold(buff[:, :, 0], 0, 1, cv.THRESH_BINARY)
        buff[:, :, 0] = cv.add(buff[:, :, 0], mask_buff)
        _, buff[:, :, 0] = cv.threshold(buff[:, :, 0], 120, 120, cv.THRESH_TRUNC)

        redImg = np.zeros(frame.shape, frame.dtype)
        redImg[:, :] = (1, 255, 255)
        # redImg = cv.cvtColor(redImg, cv.COLOR_BGR2HSV)
        # buff = cv.bitwise_or(buff, filtered)
        mask_inv = cv.bitwise_not(filtered)
        # Now black-out the area of logo in ROI
        buff = cv.bitwise_and(buff, buff, mask=mask_inv)
        red = cv.bitwise_and(redImg, redImg, mask=filtered)
        buff = cv.add(buff, red)

        # redMask = cv.bitwise_and(redImg, redImg, mask=buff)
        # masked = cv.addWeighted(redMask, 1, frame, 1, 0, frame)
        buff_smooth = cv.bilateralFilter(buff,9,75,75)
        blended = cv.addWeighted(frame, 0.5, cv.cvtColor(buff_smooth, cv.COLOR_HSV2BGR), 1.7, 0.0)
        #show the current frame and the fg masks
        cv.imshow('FG Mask', fgMask)
        cv.imshow('Median', median)
        cv.imshow('FG filtered Mask', filtered)
        cv.imshow('Frame', frame)
        cv.imshow('Masked', cv.cvtColor(buff, cv.COLOR_HSV2BGR))
        cv.imshow('Blended', blended)

        # Write the frame to the output video
        writer.write(blended)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

    # After we release our webcam, we also release the output
writer.release()