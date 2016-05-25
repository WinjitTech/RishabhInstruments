import cv2
import math
import numpy as np


def get_needle_tip(top_x, base_y, iteration):
    try:
        image = cv2.imread("MeterImages/Needle.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        corners = cv2.goodFeaturesToTrack(dilation, 40, 0.1, 10)
        needle_len = []
        corner = 0
        for i in corners:
            x, y = i.ravel()

            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if 100 < n_lenght < 500:
                needle_len.append(n_lenght)
                corner += 1
        if not needle_len:
            return
        needle_len.sort(reverse=True)

        for i in corners:
            x, y = i.ravel()
            n_lenght = math.sqrt((x - top_x) ** 2 + (y - base_y) ** 2)
            if n_lenght == needle_len[0]:
                return x, y

    except Exception, e:
        # TODO: Call dilation again if Needle position in not found
        print "Dilation Exception", str(e)
