import cv2
import math
import numpy as np


# TODO: Alternet method to detect needle
def get_needle_tip(img_path, top_x, base_y, iteration):
    try:
        image = cv2.imread(img_path + "\\MeterImages\\Needle.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_OTSU)
        dilation = cv2.dilate(thresh, kernel, iterations=iteration)
        corners = cv2.goodFeaturesToTrack(dilation, 100, 0.1, 10)
        needle_len = []
        corner = 0
        for i in corners:
            x, y = i.ravel()
            cv2.circle(image, (x, y), 2, 255, -1)
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if n_lenght < 550:
                needle_len.append(n_lenght)
                corner += 1
        # cv2.imshow("new", image)
        if not needle_len:
            return
        needle_len.sort(reverse=True)
        for i in corners:
            x, y = i.ravel()
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if n_lenght == needle_len[0]:
                cv2.circle(dilation, (x, y), 10, (0, 0, 0), -1)
                # print "Needle length: ",n_lenght
                # cv2.imshow("Needle", dilation)
                return x, y
    except Exception, e:
        # TODO: Call dilation again if Needle position in not found
        # print "Dilation Exception", str(e)
        # print "error"
        return
