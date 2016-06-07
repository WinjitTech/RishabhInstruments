import cv2
import numpy as np


def zero_needle_position(img_path, iteration):
    try:
        # Todo: Read Image
        image = cv2.imread(img_path+"\\MeterImages\\cardinals.jpg", 0)
        # # image = cv2.imread("MeterImages\cardinals.jpg", 0)
        # print ""
        # if image is None:
        #     # print "Process halting in Dilation. Image not loaded"
        #     return
        # # set kernel
        # kernel = np.ones((5, 5), np.uint8)
        # dilation = cv2.dilate(image, kernel, iterations=iteration)
        # #  TODO: Find corner of needle
        # get_needle_position = cv2.goodFeaturesToTrack(dilation, 2, 0.1, 10)
        # for corners in get_needle_position:
        #     needle_x, needle_y = corners.ravel()
        # return needle_x, needle_y
        cv2.rectangle(image, (0, 0), (100, 600), (166, 166, 166), -1)
        kernel = np.ones((5, 5), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        # ret, img = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
        # cv2.imshow("fd", dilation)
        corners = cv2.goodFeaturesToTrack(dilation, 2, 0.1, 10)
        # print "Corners", len(corners)
        cx = cy = 0
        for i in corners:
            x, y = i.ravel()
            cv2.circle(dilation, (x, y), 2, (0, 255, 0), -1)
            cx += x
            cy += y
            # print "Co-ordinates: ", x, y
        cx /= len(corners)
        cy /= len(corners)
        # cv2.circle(dilation, (int(cx), int(cy)), 4, (0, 255, 0), -1)
        # cv2.imshow("Initial_Needle", dilation)
        return cx, cy

    except Exception, e:
        # print "Exception in Base Needle Detection Dilute Image:", str(e)
        return
