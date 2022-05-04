'''

Color segmentation based on OpenCV

'''

from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='This program performs segmentation based on color. You can process both '
                                             'videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='videos/pajaros.mp4')
args = parser.parse_args()

max_value = 255
max_value_H = 360
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = 20

###############################################################################

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
writer_blended = cv.VideoWriter(args.input[0:-4] + "_output_color.avi",
                                cv.VideoWriter_fourcc(*"MJPG"),
                                30,
                                (width, height)
                                )
writer_mask = cv.VideoWriter(args.input[0:-4] + "_output_mask_color.avi",
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

    # Modify the area of the roi in case you want to process just a section of the image
    roi = frame[0: height, 0: width]
    # Transform from RGB to HSV
    frame_HSV = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    # Segment the image using thresholding in the HSV space
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    # Filter noise with morphological operators
    kernel = np.ones((1, 1), np.uint8)
    kernel2 = np.ones((6, 6), np.uint8)
    erosion = cv.erode(frame_threshold, kernel, iterations=1)
    dilation = cv.dilate(erosion, kernel2, iterations=1)

    # filtered = fgMask
    # _, filtered = cv.threshold(filtered, 100, 255, cv.THRESH_BINARY)

    # Update buffer
    if is_first_frames > 0:
        is_first_frames -= 1
    else:
        _, mask_buff = cv.threshold(buff[:, :, 0], 0, 1, cv.THRESH_BINARY)
        buff[:, :, 0] = cv.add(buff[:, :, 0], mask_buff)
        _, buff[:, :, 0] = cv.threshold(buff[:, :, 0], 120, 120, cv.THRESH_TRUNC)

        redImg = np.zeros(frame.shape, frame.dtype)
        redImg[:, :] = (1, 255, 255)
        # redImg = cv.cvtColor(redImg, cv.COLOR_BGR2HSV)
        # buff = cv.bitwise_or(buff, filtered)
        mask_inv = cv.bitwise_not(dilation)
        # Now black-out the area of logo in ROI
        buff = cv.bitwise_and(buff, buff, mask=mask_inv)
        red = cv.bitwise_and(redImg, redImg, mask=dilation)
        buff = cv.add(buff, red)

        # redMask = cv.bitwise_and(redImg, redImg, mask=buff)
        # masked = cv.addWeighted(redMask, 1, frame, 1, 0, frame)
        # buff_smooth = cv.blur(buff, (7, 7))
        buff_smooth = cv.bilateralFilter(buff, 15, 75, 75)
        blended = cv.addWeighted(frame, 0.5, cv.cvtColor(buff_smooth, cv.COLOR_HSV2BGR), 1.7, 0.0)
        #show the current frame and the fg masks
        cv.imshow('Mask HSV', frame_HSV)
        cv.imshow('frame_threshold', frame_threshold)
        cv.imshow('FG filtered Mask', dilation)
        cv.imshow('Frame', frame)
        cv.imshow('Masked', cv.cvtColor(buff, cv.COLOR_HSV2BGR))
        cv.imshow('Blended', blended)

        # Write the frame to the output video
        writer_blended.write(blended)
        writer_mask.write(cv.cvtColor(buff, cv.COLOR_HSV2BGR))

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

    # After we release our webcam, we also release the output
writer_blended.release()
writer_mask.release()