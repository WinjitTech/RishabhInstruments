import cv2
import numpy as np


def zero_needle_position(iteration):
    try:
        # Todo: Read Image
        image = cv2.imread("MeterImages/cardinals.jpg", 0)
        if image is None:
            print "Process halting in Dilation. Image not loaded"
        # set kernel
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        #  TODO: Find corner of needle
        get_needle_position = cv2.goodFeaturesToTrack(dilation, 2, 0.1, 10)
        for corners in get_needle_position:
            needle_x, needle_y = corners.ravel()
        return needle_x, needle_y

    except Exception, e:
        print "Exception in Base Needle Detection Dilute Image:", str(e)
